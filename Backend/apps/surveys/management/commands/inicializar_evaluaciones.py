from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.surveys.models import Evaluacion, PreguntaEvaluacion
from django.db import transaction

class Command(BaseCommand):
    help = 'Inicializa las evaluaciones oficiales base (NOM-035, NOM-030, 360)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando inicialización de evaluaciones oficiales...'))
        
        try:
            with transaction.atomic():
                # Crear o obtener usuario sistema
                usuario_sistema = self.crear_usuario_sistema()
                
                # Crear evaluaciones oficiales
                evaluaciones_oficiales = [
                    self.crear_evaluacion_nom035(),
                    self.crear_evaluacion_nom030(),
                    self.crear_evaluacion_360()
                ]
                
                evaluaciones_creadas = 0
                for evaluacion_data in evaluaciones_oficiales:
                    if self.crear_evaluacion_oficial(usuario_sistema, evaluacion_data):
                        evaluaciones_creadas += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {evaluaciones_creadas} evaluaciones oficiales inicializadas')
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

    def crear_evaluacion_nom035(self):
        """Datos para la evaluación NOM-035"""
        return {
            'titulo': 'NOM-035 - Evaluación de Riesgos Psicosociales',
            'descripcion': 'Evaluación oficial para identificar los factores de riesgo psicosocial en el trabajo según la NOM-035-STPS-2018.',
            'instrucciones': '''
Esta evaluación está diseñada para identificar y evaluar los factores de riesgo psicosocial en el trabajo.

INSTRUCCIONES:
- Lea cuidadosamente cada pregunta
- Responda de manera honesta y reflexiva
- No hay respuestas correctas o incorrectas
- La información es confidencial
- Complete todas las preguntas
            '''.strip(),
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

    def crear_evaluacion_nom030(self):
        """Datos para la evaluación NOM-030"""
        return {
            'titulo': 'NOM-030 - Evaluación de Servicios Preventivos de Seguridad',
            'descripcion': 'Evaluación oficial para servicios preventivos de seguridad y salud en el trabajo según la NOM-030-STPS-2009.',
            'instrucciones': '''
Esta evaluación está diseñada para evaluar los servicios preventivos de seguridad y salud en el trabajo.

INSTRUCCIONES:
- Responda basándose en su experiencia laboral actual
- Evalúe las condiciones de seguridad en su área de trabajo
- La información es confidencial
- Complete todas las preguntas obligatorias
            '''.strip(),
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

    def crear_evaluacion_360(self):
        """Datos para la evaluación 360 grados"""
        return {
            'titulo': 'Evaluación 360 Grados - Competencias Laborales',
            'descripcion': 'Evaluación integral de competencias laborales desde múltiples perspectivas (supervisor, pares, subordinados).',
            'instrucciones': '''
Esta evaluación está diseñada para obtener una visión integral de las competencias laborales desde diferentes perspectivas.

INSTRUCCIONES:
- Evalúe de manera objetiva y constructiva
- Base sus respuestas en comportamientos observables
- Sea honesto y profesional en sus evaluaciones
- La información es confidencial
- Complete todas las preguntas obligatorias
            '''.strip(),
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

    def crear_evaluacion_oficial(self, usuario_sistema, datos_evaluacion):
        """Crea una evaluación oficial con sus preguntas"""
        
        # Verificar si ya existe
        if Evaluacion.objects.filter(titulo=datos_evaluacion['titulo'], tipo='normativa').exists():
            self.stdout.write(f"⚠️  La evaluación '{datos_evaluacion['titulo']}' ya existe")
            return False
        
        # Crear la evaluación
        evaluacion = Evaluacion.objects.create(
            titulo=datos_evaluacion['titulo'],
            descripcion=datos_evaluacion['descripcion'],
            tipo='normativa',  # Evaluación oficial
            estado='activa',
            creado_por=usuario_sistema,
            instrucciones=datos_evaluacion['instrucciones'],
            tiempo_limite=None,  # Sin tiempo límite para evaluaciones oficiales
            empresa=None,  # Evaluaciones oficiales no pertenecen a empresas específicas
            planta=None
        )
        
        # Crear las preguntas
        for orden, pregunta_data in enumerate(datos_evaluacion['preguntas'], 1):
            PreguntaEvaluacion.objects.create(
                evaluacion=evaluacion,
                texto=pregunta_data['texto'],
                tipo=pregunta_data['tipo'],
                opciones=pregunta_data.get('opciones', []),
                es_requerida=pregunta_data.get('obligatoria', True),
                orden=orden
            )
        
        self.stdout.write(f"✅ Evaluación '{datos_evaluacion['titulo']}' creada exitosamente")
        return True

    def mostrar_resumen(self):
        """Muestra un resumen de las evaluaciones oficiales"""
        self.stdout.write("\n📊 Resumen de evaluaciones oficiales:")
        for evaluacion in Evaluacion.objects.filter(tipo='normativa'):
            self.stdout.write(f"   - {evaluacion.titulo} ({evaluacion.preguntas.count()} preguntas)")
