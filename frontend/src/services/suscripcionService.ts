// Servicio para gestión de suscripciones con estructura normalizada
import api from '../api';

// ===== TIPOS =====
export interface PlanSuscripcion {
  plan_id: number;
  nombre: string;
  descripcion?: string;
  duracion: number; // días
  precio: number;
  status: boolean;
}

export interface SuscripcionEmpresa {
  suscripcion_id: number;
  empresa_id: number;
  plan_id: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string; // 'activa', 'pendiente_pago', 'vencida', 'cancelada'
  status: boolean;
  fecha_creacion: string;
  fecha_actualizacion: string;
  // Datos relacionados
  empresa_nombre?: string;
  plan_nombre?: string;
  plan_precio?: number;
  plan_duracion?: number;
}

// ===== FUNCIONES =====

export interface Pago {
  pago_id: number;
  costo: number;
  monto_pago: number;
  fecha_pago: string;
  transaccion_id?: string;
  estado_pago: string; // 'pendiente', 'completado', 'fallido'
  suscripcion_id: number;
  // Datos relacionados
  empresa_nombre?: string;
  plan_nombre?: string;
}

// ===== FUNCIONES DE FORMATEO =====
export const formatearPrecio = (precio: number): string => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(precio);
};

export const formatearDuracion = (dias: number): string => {
  if (dias === 30) return '1 mes';
  if (dias === 90) return '3 meses';
  if (dias === 365) return '1 año';
  return `${dias} días`;
};

export const formatearFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// ===== FUNCIONES PRINCIPALES =====

export const listarPlanes = async (): Promise<PlanSuscripcion[]> => {
  try {
    console.log('🔄 Obteniendo planes de suscripción...');
    
    // Usar directamente la URL correcta del SubscriptionViewSet
   // const response = await api.get('/suscripciones/planes/');
   const response = await api.get('/suscripciones/listar_planes/'); 
   console.log('✅ Planes obtenidos:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener planes:', error);
    return [];
  }
};

export const obtenerSuscripciones = async (): Promise<SuscripcionEmpresa[]> => {
  try {
    console.log('🔄 Obteniendo suscripciones...');
    // Eliminar el '/api' redundante
    const response = await api.get('/suscripciones/listar/');
    console.log('✅ Suscripciones obtenidas:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener suscripciones:', error);
    return [];
  }
};

export const obtenerPagos = async (): Promise<Pago[]> => {
  try {
    console.log('🔄 Obteniendo pagos...');
    // Eliminar el '/api' redundante
    const response = await api.get('/suscripciones/pagos/');
    console.log('✅ Pagos obtenidos:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener pagos:', error);
    return [];
  }
};

export const crearSuscripcion = async (empresaId: number, planId: number): Promise<any> => {
  try {
    console.log(`🔄 Creando suscripción para empresa ${empresaId} con plan ${planId}...`);
    

    
    // Asegurar que los IDs sean números enteros válidos
 const dataRequest = {
      empresa_id: parseInt(String(empresaId)),
      plan_id: parseInt(String(planId))
    };
    
    console.log('📦 Datos a enviar:', JSON.stringify(dataRequest));
    
    // Realizar la solicitud con datos validados
     const response = await api.post('/suscripciones/crear_suscripcion/', dataRequest);
    
    console.log('✅ Suscripción creada exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error(`❌ Error al crear suscripción:`, error);
    
    // Información detallada del error
    if (error.response) {
      console.error('📝 Detalles del error:', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      });
    }

    throw error;
  }
};

export const procesarPago = async (suscripcionId: number, montoPago: number, transaccionId?: string): Promise<any> => {
  try {
    console.log(`🔄 Procesando pago para suscripción ${suscripcionId}...`);
    // Eliminar el '/api' redundante
    const response = await api.post('/suscripciones/pagar/', {
      suscripcion_id: suscripcionId,
      monto_pago: montoPago,
      transaccion_id: transaccionId
    });
    console.log('✅ Pago procesado:', response.data);
    return response.data;
  } catch (error) {
    console.error(`❌ Error al procesar pago:`, error);
    return null;
  }
};

export const crearPlan = async (planData: Omit<PlanSuscripcion, 'plan_id'>): Promise<PlanSuscripcion> => {
  try {
    console.log('🔄 Creando nuevo plan:', planData);
    const response = await api.post('/suscripciones/crear_plan/', planData);
    console.log('✅ Plan creado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al crear plan:', error);
    throw error;
  }
};

export const actualizarPlan = async (planId: number, planData: Partial<PlanSuscripcion>): Promise<PlanSuscripcion> => {
  try {
    console.log(`🔄 Actualizando plan ${planId}:`, planData);
    
    // Aseguramos que todos los datos estén en el formato correcto
    const datosActualizados = {
      plan_id: planId,
      nombre: planData.nombre,
      descripcion: planData.descripcion || "",
      duracion: planData.duracion,
      precio: planData.precio,
      status: planData.status !== undefined ? planData.status : true
    };
    
    // Intentamos con un endpoint alternativo "editar_plan"
    const response = await api.put(`/suscripciones/editar_plan/`, datosActualizados);
    console.log('✅ Plan actualizado:', response.data);
    return response.data;
  } catch (error) {
    console.error(`❌ Error al actualizar plan ${planId}:`, error);
    
    // Si falla, registramos más información para depuración
    console.error('Detalles completos del error:', error);
    throw error;
  }
};

export const eliminarPlan = async (planId: number): Promise<void> => {
  try {
    console.log(`🔄 Eliminando plan ${planId}...`);
    await api.delete(`/suscripciones/eliminar_plan/`, {
      data: { plan_id: planId }
    });
    console.log('✅ Plan eliminado');
  } catch (error) {
    console.error(`❌ Error al eliminar plan ${planId}:`, error);
    throw error;
  }
};

export const cambiarEstadoPlan = async (planId: number, nuevoEstado: boolean): Promise<void> => {
  try {
    console.log(`🔄 Cambiando estado del plan ${planId} a ${nuevoEstado}...`);
    await api.put(`/suscripciones/cambiar_estado_plan/`, {
      plan_id: planId,
      status: nuevoEstado
    });
    console.log('✅ Estado del plan actualizado');
  } catch (error) {
    console.error(`❌ Error al cambiar estado del plan ${planId}:`, error);
    throw error;
  }
};

// ===== FUNCIONES DE FLUJO INTEGRADO =====

export const suscribirseYPagar = async (empresaId: number, planId: number): Promise<{
  suscripcion: any;
  pago: any;
  redirectUrl?: string;
}> => {
  try {
    console.log(`🚀 Iniciando flujo completo de suscripción para empresa ${empresaId}, plan ${planId}`);
    
    // 1. Crear suscripción (esto cancelará automáticamente cualquier suscripción activa anterior)
    console.log('📝 Paso 1: Creando suscripción...');
    const suscripcionResult = await crearSuscripcion(empresaId, planId);
    const suscripcion = suscripcionResult.suscripcion;
    
    if (!suscripcion || !suscripcion.suscripcion_id) {
      throw new Error('No se pudo crear la suscripción');
    }
    
    // 2. Procesar pago automático
    console.log('💳 Paso 2: Procesando pago automático...');
    const montoPago = suscripcion.precio || suscripcion.plan_precio || 0;
    const transaccionId = `AUTO-${Date.now()}`;
    
    console.log(`💰 Monto del pago: $${montoPago}`);
    console.log(`🔗 Transacción ID: ${transaccionId}`);
    
    const pagoResult = await procesarPago(suscripcion.suscripcion_id, montoPago, transaccionId);
    
    console.log('🎉 Flujo completo exitoso!');
    
    // 3. Notificar actualización de suscripción
    localStorage.setItem('subscription_updated', 'true');
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'subscription_updated',
      newValue: 'true'
    }));
    
    return {
      suscripcion: suscripcion,
      pago: pagoResult.pago,
      redirectUrl: '/empresa-admin?refresh=true'
    };
    
  } catch (error) {
    console.error('❌ Error en flujo completo de suscripción:', error);
    throw error;
  }
};

export const suscribirseAPlan = async (planId: number): Promise<any> => {
  try {
    console.log(`🔄 Suscribiéndose al plan ${planId}...`);
    
    // Obtener empresa ID (simulado para testing)
    const empresaId = 1; // En producción vendría del usuario logueado
    
    const resultado = await suscribirseYPagar(empresaId, planId);
    
    console.log('✅ Suscripción completada:', resultado);
    return resultado;
    
  } catch (error) {
    console.error(`❌ Error al suscribirse al plan ${planId}:`, error);
    throw error;
  }
};

export const obtenerSuscripcionActual = async (): Promise<any> => {
  try {
    console.log('🔄 Obteniendo suscripción actual de la empresa...');
    // Eliminar el '/api' redundante
    const response = await api.get('/suscripciones/actual/');
    console.log('✅ Información de suscripción:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener suscripción actual:', error);
    return null;
  }
};

export const obtenerInfoSuscripcionEmpresa = async (empresaId: number): Promise<any> => {
  try {
    console.log(`🔄 Obteniendo información de suscripción para empresa ${empresaId}...`);
    const response = await api.get(`/suscripciones/info_suscripcion_empresa/?empresa_id=${empresaId}`);
    console.log('✅ Información de suscripción obtenida:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener información de suscripción:', error);
    throw error;
  }
};

// ===== FUNCIONES ADICIONALES PARA SUPERADMIN =====

export const listarSuscripciones = obtenerSuscripciones;
export const listarPagos = obtenerPagos;

export const editarPlan = async (planId: number, planData: Partial<PlanSuscripcion>): Promise<PlanSuscripcion> => {
  return await actualizarPlan(planId, planData);
};

export const renovarSuscripcion = async (empresaId: number, planId: number): Promise<any> => {
  return await crearSuscripcion(empresaId, planId);
};

export const suspenderSuscripcion = async (suscripcionId: number): Promise<void> => {
  try {
    console.log(`🔄 Suspendiendo suscripción ${suscripcionId}...`);
    await api.put(`/suscripciones/suspender_suscripcion/`, {
      suscripcion_id: suscripcionId
    });
    console.log('✅ Suscripción suspendida');
  } catch (error) {
    console.error(`❌ Error al suspender suscripción ${suscripcionId}:`, error);
    throw error;
  }
};

export const reactivarSuscripcion = async (suscripcionId: number): Promise<void> => {
  try {
    console.log(`🔄 Reactivando suscripción ${suscripcionId}...`);
    await api.put(`/suscripciones/reactivar_suscripcion/`, {
      suscripcion_id: suscripcionId
    });
    console.log('✅ Suscripción reactivada');
  } catch (error) {
    console.error(`❌ Error al reactivar suscripción ${suscripcionId}:`, error);
    throw error;
  }
};

export const getEstadoSuscripcionTexto = (estado: string): string => {
  switch (estado) {
    case 'activa': return 'Activa';
    case 'pendiente_pago': return 'Pendiente de Pago';
    case 'vencida': return 'Vencida';
    case 'cancelada': return 'Cancelada';
    case 'suspendida': return 'Suspendida';
    default: return 'Desconocido';
  }
};

export const getEstadoSuscripcionColor = (estado: string): string => {
  switch (estado) {
    case 'activa': return '#28a745';
    case 'pendiente_pago': return '#ffc107';
    case 'vencida': return '#dc3545';
    case 'cancelada': return '#6c757d';
    case 'suspendida': return '#fd7e14';
    default: return '#6c757d';
  }
};

export const getEstadoPagoTexto = (estado: string): string => {
  switch (estado) {
    case 'completado': return 'Completado';
    case 'pendiente': return 'Pendiente';
    case 'fallido': return 'Fallido';
    default: return 'Desconocido';
  }
};

// Exportación por defecto para compatibilidad
const suscripcionService = {
  listarPlanes,
  obtenerSuscripciones,
  obtenerPagos,
  crearSuscripcion,
  procesarPago,
  crearPlan,
  actualizarPlan,
  eliminarPlan,
  cambiarEstadoPlan,
  suscribirseYPagar,
  suscribirseAPlan,
  obtenerSuscripcionActual,
  obtenerInfoSuscripcionEmpresa,
  formatearPrecio,
  formatearDuracion,
  formatearFecha,
  listarSuscripciones,
  listarPagos,
  editarPlan,
  renovarSuscripcion,
  suspenderSuscripcion,
  reactivarSuscripcion,
  getEstadoSuscripcionTexto,
  getEstadoSuscripcionColor,
  getEstadoPagoTexto
};

export default suscripcionService;