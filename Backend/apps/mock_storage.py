# Sistema de almacenamiento mock en memoria para suscripciones y pagos
# Este módulo mantiene datos simulados entre endpoints hasta que se use la DB real

from datetime import datetime, timedelta
from django.utils import timezone
import uuid
import json
import os
from pathlib import Path

class MockStorage:
    """Almacenamiento en memoria para datos de suscripciones y pagos con persistencia en archivo"""
    
    def __init__(self):
        self.storage_file = Path(__file__).parent / 'mock_data.json'
        self.load_from_file()
    
    def save_to_file(self):
        """Guarda los datos actuales en un archivo JSON"""
        try:
            data = {
                'planes_adicionales': self.planes_adicionales,
                'next_plan_id': self.next_plan_id,
                'suscripciones': self.suscripciones,
                'next_suscripcion_id': self.next_suscripcion_id,
                'pagos': self.pagos,
                'next_pago_id': self.next_pago_id,
                'empresa_suscripcion_map': self.empresa_suscripcion_map,
                'timestamp': timezone.now().isoformat()
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving mock data: {e}")
    
    def load_from_file(self):
        """Carga los datos desde el archivo JSON o inicializa valores por defecto"""
        try:
            if self.storage_file.exists():
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.planes_adicionales = data.get('planes_adicionales', {})
                # Convertir keys a int para planes_adicionales
                self.planes_adicionales = {int(k): v for k, v in self.planes_adicionales.items()}
                
                self.next_plan_id = data.get('next_plan_id', 4)
                self.suscripciones = data.get('suscripciones', {})
                # Convertir keys a int para suscripciones
                self.suscripciones = {int(k): v for k, v in self.suscripciones.items()}
                
                self.next_suscripcion_id = data.get('next_suscripcion_id', 1)
                self.pagos = data.get('pagos', {})
                # Convertir keys a int para pagos
                self.pagos = {int(k): v for k, v in self.pagos.items()}
                
                self.next_pago_id = data.get('next_pago_id', 1)
                self.empresa_suscripcion_map = data.get('empresa_suscripcion_map', {})
                # Convertir keys a int para empresa_suscripcion_map
                self.empresa_suscripcion_map = {int(k): v for k, v in self.empresa_suscripcion_map.items()}
                
                print(f"Mock data loaded from file. Suscripciones: {len(self.suscripciones)}, Pagos: {len(self.pagos)}")
            else:
                self.reset_data()
        except Exception as e:
            print(f"Error loading mock data: {e}")
            self.reset_data()
        
        # Siempre inicializar planes base
        self.planes_base = {
            1: {
                'plan_id': 1,
                'nombre': 'Plan Básico (1 Mes)',
                'descripcion': 'Plan mensual con funcionalidades básicas',
                'duracion': 30,
                'precio': 299.00,
                'status': True
            },
            2: {
                'plan_id': 2,
                'nombre': 'Plan Profesional (3 Meses)',
                'descripcion': 'Plan trimestral con descuento y funcionalidades avanzadas',
                'duracion': 90,
                'precio': 799.00,
                'status': True
            },
            3: {
                'plan_id': 3,
                'nombre': 'Plan Anual',
                'descripcion': 'Plan anual con máximo descuento y todas las funcionalidades',
                'duracion': 365,
                'precio': 2999.00,
                'status': True
            }
        }
    
    def reset_data(self):
        """Reinicia todos los datos a los valores base"""
        # Planes adicionales creados por admin
        self.planes_adicionales = {}
        self.next_plan_id = 4
        
        # Suscripciones creadas
        self.suscripciones = {}
        self.next_suscripcion_id = 1
        
        # Pagos realizados
        self.pagos = {}
        self.next_pago_id = 1
        
        # Mapeo de empresa_id -> suscripcion_id para búsquedas rápidas
        self.empresa_suscripcion_map = {}
    
    def get_planes(self):
        """Obtiene todos los planes disponibles (base + adicionales)"""
        all_planes = {}
        all_planes.update(self.planes_base)
        all_planes.update(self.planes_adicionales)
        return list(all_planes.values())
    
    def get_plan_by_id(self, plan_id):
        """Obtiene un plan específico por ID"""
        if plan_id in self.planes_base:
            return self.planes_base[plan_id]
        elif plan_id in self.planes_adicionales:
            return self.planes_adicionales[plan_id]
        return None
    
    def crear_plan(self, nombre, descripcion, precio, duracion):
        """Crea un nuevo plan adicional"""
        plan_id = self.next_plan_id
        self.next_plan_id += 1
        
        nuevo_plan = {
            'plan_id': plan_id,
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': float(precio),
            'duracion': int(duracion),
            'status': True
        }
        
        self.planes_adicionales[plan_id] = nuevo_plan
        self.save_to_file()  # Guardar cambios
        return nuevo_plan
    
    def editar_plan(self, plan_id, nombre=None, descripcion=None, precio=None, duracion=None, status=None):
        """Edita un plan existente"""
        plan = None
        storage_dict = None
        
        if plan_id in self.planes_base:
            plan = self.planes_base[plan_id]
            storage_dict = self.planes_base
        elif plan_id in self.planes_adicionales:
            plan = self.planes_adicionales[plan_id]
            storage_dict = self.planes_adicionales
        
        if not plan:
            return None
        
        # Actualizar campos si se proporcionan
        if nombre is not None:
            plan['nombre'] = nombre
        if descripcion is not None:
            plan['descripcion'] = descripcion
        if precio is not None:
            plan['precio'] = float(precio)
        if duracion is not None:
            plan['duracion'] = int(duracion)
        if status is not None:
            plan['status'] = bool(status)
        
        storage_dict[plan_id] = plan
        self.save_to_file()  # Guardar cambios
        return plan
    
    def crear_suscripcion(self, empresa_id, plan_id):
        """Crea una nueva suscripción"""
        plan = self.get_plan_by_id(plan_id)
        if not plan:
            return None
        
        suscripcion_id = self.next_suscripcion_id
        self.next_suscripcion_id += 1
        
        # Cancelar suscripción anterior si existe
        if empresa_id in self.empresa_suscripcion_map:
            old_suscripcion_id = self.empresa_suscripcion_map[empresa_id]
            if old_suscripcion_id in self.suscripciones:
                self.suscripciones[old_suscripcion_id]['status'] = False
                self.suscripciones[old_suscripcion_id]['estado'] = 'cancelada'
        
        # Crear nueva suscripción
        ahora = timezone.now()
        fecha_fin = ahora + timedelta(days=plan['duracion'])
        
        nueva_suscripcion = {
            'suscripcion_id': suscripcion_id,
            'empresa_id': empresa_id,
            'plan_id': plan_id,
            'fecha_inicio': ahora.strftime('%Y-%m-%d'),
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
            'estado': 'pendiente_pago',  # Inicial
            'status': True,
            'fecha_creacion': ahora.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_actualizacion': ahora.strftime('%Y-%m-%d %H:%M:%S'),
            'empresa_nombre': f'Empresa {empresa_id}',  # Mock
            'plan_nombre': plan['nombre'],
            'plan_precio': str(plan['precio']),
            'plan_duracion': plan['duracion'],
        }
        
        self.suscripciones[suscripcion_id] = nueva_suscripcion
        self.empresa_suscripcion_map[empresa_id] = suscripcion_id
        self.save_to_file()  # Guardar cambios
        
        return nueva_suscripcion
    
    def get_suscripciones(self):
        """Obtiene todas las suscripciones"""
        return list(self.suscripciones.values())
    
    def get_suscripcion_by_empresa(self, empresa_id):
        """Obtiene la suscripción activa más reciente de una empresa"""
        # Buscar todas las suscripciones de la empresa
        suscripciones_empresa = []
        for susc in self.suscripciones.values():
            if susc['empresa_id'] == empresa_id:
                suscripciones_empresa.append(susc)
        
        if not suscripciones_empresa:
            return None
        
        # Buscar suscripción activa más reciente
        suscripciones_activas = [s for s in suscripciones_empresa if s['estado'] == 'activa' and s['status']]
        if suscripciones_activas:
            # Ordenar por fecha de creación (más reciente primero)
            suscripciones_activas.sort(key=lambda x: x['fecha_creacion'], reverse=True)
            return suscripciones_activas[0]
        
        # Si no hay activas, devolver la más reciente
        suscripciones_empresa.sort(key=lambda x: x['fecha_creacion'], reverse=True)
        return suscripciones_empresa[0]
    
    def crear_pago(self, suscripcion_id, monto_pago, transaccion_id=None):
        """Crea un nuevo pago y actualiza el estado de la suscripción"""
        if suscripcion_id not in self.suscripciones:
            return None
        
        suscripcion = self.suscripciones[suscripcion_id]
        pago_id = self.next_pago_id
        self.next_pago_id += 1
        
        if not transaccion_id:
            transaccion_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
        
        ahora = timezone.now()
        
        nuevo_pago = {
            'pago_id': pago_id,
            'costo': suscripcion['plan_precio'],
            'monto_pago': str(float(monto_pago)),
            'fecha_pago': ahora.strftime('%Y-%m-%d'),
            'transaccion_id': transaccion_id,
            'estado_pago': 'completado',
            'suscripcion_id': suscripcion_id,
            'empresa_nombre': suscripcion['empresa_nombre'],
            'plan_nombre': suscripcion['plan_nombre'],
        }
        
        self.pagos[pago_id] = nuevo_pago
        
        # Actualizar estado de suscripción a activa
        self.suscripciones[suscripcion_id]['estado'] = 'activa'
        self.suscripciones[suscripcion_id]['fecha_actualizacion'] = ahora.strftime('%Y-%m-%d %H:%M:%S')
        
        self.save_to_file()  # Guardar cambios
        return nuevo_pago
    
    def get_pagos(self):
        """Obtiene todos los pagos"""
        return list(self.pagos.values())
    
    def get_subscription_info(self, empresa_id):
        """Obtiene información de suscripción para una empresa específica"""
        suscripcion = self.get_suscripcion_by_empresa(empresa_id)
        
        if not suscripcion:
            return {
                'tiene_suscripcion': False,
                'estado': 'sin_suscripcion',
                'mensaje': 'La empresa no tiene una suscripción activa',
                'requiere_pago': True
            }
        
        if suscripcion['estado'] == 'pendiente_pago':
            return {
                'tiene_suscripcion': False,
                'estado': 'pendiente_pago',
                'mensaje': 'La empresa tiene una suscripción pendiente de pago',
                'requiere_pago': True,
                'suscripcion': suscripcion
            }
        
        if suscripcion['estado'] == 'activa':
            # Verificar si ha vencido
            from datetime import datetime
            fecha_fin = datetime.strptime(suscripcion['fecha_fin'], '%Y-%m-%d').date()
            hoy = timezone.now().date()
            dias_restantes = (fecha_fin - hoy).days
            
            if dias_restantes < 0:
                # Actualizar estado a vencida automáticamente
                self.suscripciones[self.empresa_suscripcion_map[empresa_id]]['estado'] = 'vencida'
                self.save_to_file()
                
                return {
                    'tiene_suscripcion': False,
                    'estado': 'vencida',
                    'fecha_vencimiento': suscripcion['fecha_fin'],
                    'dias_vencida': abs(dias_restantes),
                    'mensaje': f'La suscripción venció hace {abs(dias_restantes)} días',
                    'requiere_pago': True,
                    'suscripcion': suscripcion
                }
            elif dias_restantes <= 7:
                return {
                    'tiene_suscripcion': True,
                    'estado': 'por_vencer',
                    'dias_restantes': dias_restantes,
                    'fecha_vencimiento': suscripcion['fecha_fin'],
                    'mensaje': f'La suscripción vence en {dias_restantes} días',
                    'requiere_renovacion': True,
                    'suscripcion': suscripcion
                }
            
            return {
                'tiene_suscripcion': True,
                'estado': 'activa',
                'dias_restantes': dias_restantes,
                'fecha_vencimiento': suscripcion['fecha_fin'],
                'mensaje': f'Suscripción activa. {dias_restantes} días restantes',
                'requiere_pago': False,
                'suscripcion': suscripcion
            }
        
        return {
            'tiene_suscripcion': False,
            'estado': suscripcion['estado'],
            'mensaje': f'Suscripción en estado: {suscripcion["estado"]}',
            'requiere_pago': True,
            'suscripcion': suscripcion
        }

# Instancia global para mantener datos entre requests
mock_storage = MockStorage()
