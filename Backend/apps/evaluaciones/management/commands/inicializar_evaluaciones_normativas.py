from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.evaluaciones.models import EvaluacionCompleta, Pregunta, TipoEvaluacion, EvaluacionPregunta
from apps.users.models import Empresa
from django.db import transaction
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Inicializa las evaluaciones normativas oficiales (NOM-035, NOM-030, 360)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando inicialización de evaluaciones normativas...'))
        
        try:
            with transaction.atomic():
                # Crear o obtener usuario sistema
                usuario_sistema = self.crear_usuario_sistema()
                
                # Crear tipos de evaluación
                self.crear_tipos_evaluacion()
                
                # Crear evaluaciones normativas
                evaluaciones_creadas = 0
                for tipo_nombre in ['NOM-035', 'NOM-030', '360']:
                    if self.crear_evaluacion_normativa(usuario_sistema, tipo_nombre):
                        evaluaciones_creadas += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {evaluaciones_creadas} evaluaciones normativas inicializadas')
                )
                
                # Mostrar resumen
                self.mostrar_resumen()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante la inicialización: {str(e)}')
            )
            raise

    def crear_usuario_sistema(self):
        """Crea o obtiene el usuario sistema para evaluaciones oficiales"""
        usuario_sistema, created = User.objects.get_or_create(
            username='sistema',
            defaults={
                'email': 'sistema@axyoma.com',
                'first_name': 'Sistema',
                'last_name': 'Axyoma',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            usuario_sistema.set_password('sistema123')
            usuario_sistema.save()
            self.stdout.write(f"✅ Usuario sistema creado: {usuario_sistema.username}")
        
        return usuario_sistema

    def crear_tipos_evaluacion(self):
        """Crea los tipos de evaluación normativa"""
        tipos = [
            {
                'nombre': 'NOM-035',
                'descripcion': 'Evaluación de factores de riesgo psicosocial en el trabajo según NOM-035-STPS-2018'
            },
            {
                'nombre': 'NOM-030', 
                'descripcion': 'Evaluación de servicios preventivos de seguridad y salud en el trabajo según NOM-030-STPS-2009'
            },
            {
                'nombre': '360',
                'descripcion': 'Evaluación 360 grados para competencias laborales y desempeño'
            }
        ]
        
        for tipo_data in tipos:
            tipo, created = TipoEvaluacion.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults={
                    'descripcion': tipo_data['descripcion'],
                    'normativa_oficial': True,
                    'activo': True
                }
            )
            if created:
                self.stdout.write(f"✅ Tipo de evaluación creado: {tipo.nombre}")

    def crear_evaluacion_normativa(self, usuario_sistema, tipo_nombre):
        """Crea una evaluación normativa específica"""
        
        # Obtener el tipo de evaluación
        try:
            tipo_evaluacion = TipoEvaluacion.objects.get(nombre=tipo_nombre)
        except TipoEvaluacion.DoesNotExist:
            self.stdout.write(f"❌ Tipo de evaluación '{tipo_nombre}' no encontrado")
            return False
        
        # Verificar si ya existe una evaluación normativa de este tipo
        if EvaluacionCompleta.objects.filter(
            titulo__icontains=tipo_nombre,
            empresa__isnull=True  # Evaluaciones normativas no tienen empresa
        ).exists():
            self.stdout.write(f"⚠️  Evaluación normativa '{tipo_nombre}' ya existe")
            return False
        
        # Datos específicos por tipo
        datos_evaluacion = self.obtener_datos_evaluacion(tipo_nombre)
        
        # Crear la evaluación
        evaluacion = EvaluacionCompleta.objects.create(
            titulo=datos_evaluacion['titulo'],
            descripcion=datos_evaluacion['descripcion'],
            tipo_evaluacion=tipo_evaluacion,
            empresa=None,  # Evaluaciones normativas no pertenecen a empresas
            estado='activa',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(days=365),  # Válida por 1 año
            es_anonima=True,
            creada_por=usuario_sistema
        )
        
        # Crear las preguntas
        for orden, pregunta_data in enumerate(datos_evaluacion['preguntas'], 1):
            pregunta = Pregunta.objects.create(
                tipo_evaluacion=tipo_evaluacion,
                empresa=None,  # Pregunta normativa
                texto_pregunta=pregunta_data['texto'],
                tipo_respuesta=pregunta_data['tipo'],
                opciones_respuesta=pregunta_data.get('opciones', []),
                es_obligatoria=pregunta_data.get('obligatoria', True),
                orden=orden,
                creada_por=usuario_sistema
            )
            
            # Relacionar pregunta con evaluación
            EvaluacionPregunta.objects.create(
                evaluacion=evaluacion,
                pregunta=pregunta,
                orden=orden,
                es_obligatoria=pregunta_data.get('obligatoria', True)
            )
        
        self.stdout.write(f"✅ Evaluación normativa '{datos_evaluacion['titulo']}' creada exitosamente")
        return True

    def obtener_datos_evaluacion(self, tipo_nombre):
        """Obtiene los datos específicos para cada tipo de evaluación"""
        
        if tipo_nombre == 'NOM-035':
            return {
                'titulo': 'NOM-035 - Evaluación de Riesgos Psicosociales',
                'descripcion': 'Evaluación oficial para identificar los factores de riesgo psicosocial en el trabajo según la NOM-035-STPS-2018.',
                'preguntas': [
                    {
                        'texto': '¿Con qué frecuencia se siente estresado en su trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Nunca', 'Raramente', 'Algunas veces', 'Frecuentemente', 'Siempre'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Considera que su carga de trabajo es excesiva?',
                        'tipo': 'multiple',
                        'opciones': ['Totalmente en desacuerdo', 'En desacuerdo', 'Neutral', 'De acuerdo', 'Totalmente de acuerdo'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Recibe apoyo adecuado de su supervisor inmediato?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Frecuentemente', 'Algunas veces', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Tiene claridad sobre las tareas y responsabilidades de su puesto?',
                        'tipo': 'multiple',
                        'opciones': ['Muy claro', 'Claro', 'Moderadamente claro', 'Poco claro', 'Nada claro'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Cómo califica la comunicación en su área de trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Excelente', 'Buena', 'Regular', 'Mala', 'Muy mala'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Se siente reconocido por el trabajo que realiza?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Frecuentemente', 'Algunas veces', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Considera que puede equilibrar su vida laboral y personal?',
                        'tipo': 'multiple',
                        'opciones': ['Totalmente', 'Mayormente', 'Moderadamente', 'Poco', 'Nada'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Ha experimentado violencia laboral o acoso en su trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Nunca', 'Muy pocas veces', 'Algunas veces', 'Frecuentemente', 'Muy frecuentemente'],
                        'obligatoria': True
                    },
                    {
                        'texto': 'Describa algún factor de riesgo psicosocial específico en su área de trabajo:',
                        'tipo': 'texto',
                        'obligatoria': False
                    },
                    {
                        'texto': '¿Qué sugerencias tiene para mejorar el ambiente psicosocial en su trabajo?',
                        'tipo': 'texto',
                        'obligatoria': False
                    }
                ]
            }
        
        elif tipo_nombre == 'NOM-030':
            return {
                'titulo': 'NOM-030 - Evaluación de Servicios Preventivos de Seguridad',
                'descripcion': 'Evaluación oficial para servicios preventivos de seguridad y salud en el trabajo según la NOM-030-STPS-2009.',
                'preguntas': [
                    {
                        'texto': '¿Conoce los procedimientos de seguridad de su área de trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Muy bien', 'Bien', 'Moderadamente', 'Poco', 'Nada'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Cuenta con el equipo de protección personal necesario?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Frecuentemente', 'Algunas veces', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Ha recibido capacitación en seguridad y salud en el trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Sí, frecuentemente', 'Sí, ocasionalmente', 'Solo al ingresar', 'Muy poca', 'No he recibido'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Considera que su lugar de trabajo es seguro?',
                        'tipo': 'multiple',
                        'opciones': ['Muy seguro', 'Seguro', 'Moderadamente seguro', 'Poco seguro', 'Inseguro'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Existe un comité de seguridad e higiene en su empresa?',
                        'tipo': 'multiple',
                        'opciones': ['Sí, muy activo', 'Sí, moderadamente activo', 'Sí, poco activo', 'Sí, pero inactivo', 'No existe'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Se realizan inspecciones de seguridad periódicas?',
                        'tipo': 'multiple',
                        'opciones': ['Muy frecuentemente', 'Frecuentemente', 'Ocasionalmente', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Sabe cómo reportar incidentes o condiciones inseguras?',
                        'tipo': 'multiple',
                        'opciones': ['Perfectamente', 'Bien', 'Moderadamente', 'Poco', 'No sé'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Ha presenciado accidentes de trabajo en su área?',
                        'tipo': 'multiple',
                        'opciones': ['Nunca', 'Muy pocas veces', 'Algunas veces', 'Frecuentemente', 'Muy frecuentemente'],
                        'obligatoria': True
                    },
                    {
                        'texto': 'Describa algún riesgo de seguridad específico en su área de trabajo:',
                        'tipo': 'texto',
                        'obligatoria': False
                    },
                    {
                        'texto': '¿Qué mejoras sugiere para la seguridad en su lugar de trabajo?',
                        'tipo': 'texto',
                        'obligatoria': False
                    }
                ]
            }
        
        elif tipo_nombre == '360':
            return {
                'titulo': 'Evaluación 360 Grados - Competencias Laborales',
                'descripcion': 'Evaluación integral de competencias laborales desde múltiples perspectivas (supervisor, pares, subordinados).',
                'preguntas': [
                    {
                        'texto': '¿Cómo califica la comunicación del evaluado?',
                        'tipo': 'multiple',
                        'opciones': ['Excelente', 'Muy buena', 'Buena', 'Regular', 'Deficiente'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Demuestra liderazgo en su trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Frecuentemente', 'Algunas veces', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Cómo evalúa su capacidad de trabajo en equipo?',
                        'tipo': 'multiple',
                        'opciones': ['Excelente', 'Muy buena', 'Buena', 'Regular', 'Deficiente'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Cumple con los plazos y compromisos establecidos?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Casi siempre', 'Frecuentemente', 'Ocasionalmente', 'Raramente'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Demuestra iniciativa y proactividad?',
                        'tipo': 'multiple',
                        'opciones': ['Muy alta', 'Alta', 'Moderada', 'Baja', 'Muy baja'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Cómo maneja los conflictos y situaciones difíciles?',
                        'tipo': 'multiple',
                        'opciones': ['Excelente', 'Muy bien', 'Bien', 'Regular', 'Deficiente'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Busca continuamente mejorar sus habilidades y conocimientos?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Frecuentemente', 'Algunas veces', 'Raramente', 'Nunca'],
                        'obligatoria': True
                    },
                    {
                        'texto': '¿Demuestra ética y profesionalismo en su trabajo?',
                        'tipo': 'multiple',
                        'opciones': ['Siempre', 'Casi siempre', 'Frecuentemente', 'Ocasionalmente', 'Raramente'],
                        'obligatoria': True
                    },
                    {
                        'texto': 'Mencione las principales fortalezas del evaluado:',
                        'tipo': 'texto',
                        'obligatoria': False
                    },
                    {
                        'texto': '¿Qué áreas de mejora sugiere para el evaluado?',
                        'tipo': 'texto',
                        'obligatoria': False
                    }
                ]
            }

    def mostrar_resumen(self):
        """Muestra un resumen de las evaluaciones normativas"""
        self.stdout.write("\n📊 Resumen de evaluaciones normativas:")
        evaluaciones_normativas = EvaluacionCompleta.objects.filter(empresa__isnull=True)
        for evaluacion in evaluaciones_normativas:
            total_preguntas = EvaluacionPregunta.objects.filter(evaluacion=evaluacion).count()
            self.stdout.write(f"   - {evaluacion.titulo} ({total_preguntas} preguntas)")
