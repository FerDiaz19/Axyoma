// Servicio para gestión de suscripciones con estructura normalizada
import api from '../api';

// ===== TIPOS =====
export interface PlanSuscripcion {
  plan_id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  duracion: number;
  status: boolean;
}

export interface SuscripcionEmpresa {
  suscripcion_id: number;
  empresa_id: number;
  empresa_nombre: string;
  plan_id: number;
  plan_nombre: string;
  plan_precio: number;
  plan_duracion: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  status: boolean;
  dias_restantes?: number;  // ✅ Agregar esta propiedad
  esta_activa?: boolean;    // ✅ Agregar esta propiedad
  esta_por_vencer?: boolean; // ✅ Agregar esta propiedad
}

export interface Pago {
  pago_id: number;
  suscripcion_id: number;
  empresa_nombre: string;
  plan_nombre: string;
  costo: number;
  monto_pago: number;
  estado_pago: string;
  fecha_pago: string;
  fecha_vencimiento?: string;
  transaccion_id?: string;
  usuario?: string;
}

// ============= FUNCIONES DE UTILIDAD =============
export const formatearPrecio = (precio: number): string => {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'MXN'
  }).format(precio);
};

export const formatearDuracion = (dias: number): string => {
  if (dias === 30) return '1 mes';
  if (dias === 90) return '3 meses';
  if (dias === 180) return '6 meses';
  if (dias === 365) return '1 año';
  return `${dias} días`;
};

export const formatearFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString('es-MX');
};

export const getEstadoSuscripcionTexto = (estado: string): string => {
  switch (estado.toLowerCase()) {
    case 'activa':
      return '🟢 Activa';
    case 'vencida':
      return '🔴 Vencida';
    case 'suspendida':
      return '🟡 Suspendida';
    case 'cancelada':
      return '❌ Cancelada';
    default:
      return estado;
  }
};

export const getEstadoSuscripcionColor = (estado: string): string => {
  switch (estado.toLowerCase()) {
    case 'activa':
      return 'active';
    case 'vencida':
      return 'expired';
    case 'suspendida':
      return 'warning';
    case 'cancelada':
      return 'inactive';
    default:
      return 'inactive';
  }
};

export const getEstadoPagoTexto = (estado: string): string => {
  switch (estado.toLowerCase()) {
    case 'completado':
      return '✅ Completado';
    case 'pendiente':
      return '⏳ Pendiente';
    case 'fallido':
      return '❌ Fallido';
    case 'cancelado':
      return '🚫 Cancelado';
    default:
      return estado;
  }
};

// ============= FUNCIONES DE API =============
export const listarPlanes = async (): Promise<PlanSuscripcion[]> => {
  try {
    console.log('🔍 Obteniendo lista de planes...');
    const response = await api.get('/suscripciones/planes/');
    console.log('✅ Planes obtenidos:', response.data);
    
    if (Array.isArray(response.data)) {
      return response.data;
    } else {
      console.warn('⚠️ Formato de respuesta inesperado:', response.data);
      return [];
    }
  } catch (error) {
    console.error('❌ Error obteniendo planes:', error);
    throw error;
  }
};

export const listarSuscripciones = async (): Promise<SuscripcionEmpresa[]> => {
  try {
    console.log('🔍 Obteniendo lista de suscripciones...');
    const response = await api.get('subscriptions/suscripciones/');
    console.log('✅ Suscripciones obtenidas:', response.data);
    
    if (Array.isArray(response.data)) {
      return response.data;
    } else if (response.data && Array.isArray(response.data.suscripciones)) {
      return response.data.suscripciones;
    } else {
      console.warn('⚠️ Formato de respuesta inesperado:', response.data);
      return [];
    }
  } catch (error) {
    console.error('❌ Error obteniendo suscripciones:', error);
    throw error;
  }
};

export const listarPagos = async (): Promise<Pago[]> => {
  try {
    console.log('🔍 Obteniendo lista de pagos...');
    const response = await api.get('/subscriptions/pagos/');
    console.log('✅ Pagos obtenidos:', response.data);
    
    if (Array.isArray(response.data)) {
      return response.data;
    } else if (response.data && Array.isArray(response.data.pagos)) {
      return response.data.pagos;
    } else {
      console.warn('⚠️ Formato de respuesta inesperado para pagos:', response.data);
      return [];
    }
  } catch (error) {
    console.error('❌ Error obteniendo pagos:', error);
    throw error;
  }
};

export const crearPlan = async (planData: Omit<PlanSuscripcion, 'plan_id'>): Promise<PlanSuscripcion> => {
  try {
    console.log('🔄 Creando nuevo plan:', planData);
    const response = await api.post('/subscriptions/crear-plan/', planData);
    console.log('✅ Plan creado:', response.data);
    return response.data.plan;
  } catch (error) {
    console.error('❌ Error creando plan:', error);
    throw error;
  }
};

export const editarPlan = async (planId: number, planData: Partial<PlanSuscripcion>): Promise<any> => {
  try {
    console.log(`🔧 Editando plan ${planId}:`, planData);
    const response = await api.put('/subscriptions/editar-plan/', {
      plan_id: planId,
      ...planData
    });
    console.log('✅ Plan editado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error editando plan:', error);
    throw error;
  }
};

export const cambiarEstadoPlan = async (planId: number, nuevoEstado: boolean): Promise<any> => {
  try {
    console.log(`🔄 Cambiando estado del plan ${planId} a ${nuevoEstado}...`);
    const response = await api.put('/subscriptions/editar-plan/', {
      plan_id: planId,
      status: nuevoEstado
    });
    console.log('✅ Estado del plan cambiado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error cambiando estado del plan:', error);
    throw error;
  }
};

export const crearSuscripcion = async (empresaId: number, planId: number): Promise<any> => {
  try {
    console.log(`🔄 Creando suscripción para empresa ${empresaId} con plan ${planId}...`);
    const response = await api.post('/subscriptions/crear-suscripcion/', {
      empresa_id: empresaId,
      plan_id: planId
    });
    console.log('✅ Suscripción creada:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error creando suscripción:', error);
    throw error;
  }
};

export const renovarSuscripcion = async (empresaId: number, planId: number): Promise<any> => {
  try {
    console.log(`🔄 Renovando suscripción para empresa ${empresaId} con plan ${planId}...`);
    const response = await api.post('/subscriptions/crear-suscripcion/', {
      empresa_id: empresaId,
      plan_id: planId
    });
    console.log('✅ Suscripción renovada:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error renovando suscripción:', error);
    throw error;
  }
};

export const suspenderSuscripcion = async (suscripcionId: number): Promise<any> => {
  try {
    console.log(`🔄 Suspendiendo suscripción ${suscripcionId}...`);
    const response = await api.post('/subscriptions/suspender-suscripcion/', {
      suscripcion_id: suscripcionId
    });
    console.log('✅ Suscripción suspendida:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error suspendiendo suscripción:', error);
    throw error;
  }
};

export const reactivarSuscripcion = async (suscripcionId: number): Promise<any> => {
  try {
    console.log(`🔄 Reactivando suscripción ${suscripcionId}...`);
    const response = await api.post('/subscriptions/reactivar-suscripcion/', {
      suscripcion_id: suscripcionId
    });
    console.log('✅ Suscripción reactivada:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error reactivando suscripción:', error);
    throw error;
  }
};

export const procesarPago = async (suscripcionId: number, montoPago: number, transaccionId?: string): Promise<any> => {
  try {
    console.log(`🔄 Procesando pago para suscripción ${suscripcionId}...`);
    const response = await api.post('/subscriptions/procesar-pago/', {
      suscripcion_id: suscripcionId,
      monto_pago: montoPago,
      transaccion_id: transaccionId || `PAY-${Date.now()}`
    });
    console.log('✅ Pago procesado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error procesando pago:', error);
    throw error;
  }
};

export const obtenerInfoSuscripcionEmpresa = async (empresaId: number): Promise<any> => {
  try {
    console.log(`🔍 Obteniendo información de suscripción para empresa ${empresaId}...`);
    const response = await api.get(`/subscriptions/info-empresa/?empresa_id=${empresaId}`);
    console.log('✅ Información de suscripción obtenida:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error obteniendo información de suscripción:', error);
    throw error;
  }
};

// ============= FUNCIONES FALTANTES CORREGIDAS =============

// ✅ Función para obtener suscripción actual (SIN parámetros por defecto - usa empresaId de userData)
export const obtenerSuscripcionActual = async (empresaId?: number): Promise<SuscripcionEmpresa | null> => {
  try {
    // Si no se proporciona empresaId, intentar obtenerlo del contexto o localStorage
    let targetEmpresaId = empresaId;
    if (!targetEmpresaId) {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      targetEmpresaId = userData.empresa_id;
    }
    
    if (!targetEmpresaId) {
      console.warn('⚠️ No se pudo determinar el empresa_id para obtener suscripción actual');
      return null;
    }

    console.log(`🔍 Obteniendo suscripción actual para empresa ${targetEmpresaId}...`);
    const response = await api.get(`/subscriptions/info-empresa/?empresa_id=${targetEmpresaId}`);
    console.log('✅ Información de suscripción obtenida:', response.data);
    
    // Si el response contiene la información de suscripción, la retornamos
    if (response.data && response.data.tiene_suscripcion) {
      // Construir objeto SuscripcionEmpresa desde la respuesta
      const suscripcionData: SuscripcionEmpresa = {
        suscripcion_id: response.data.suscripcion_id || 0,
        empresa_id: targetEmpresaId,
        empresa_nombre: response.data.empresa_nombre || '',
        plan_id: response.data.plan_id || 0,
        plan_nombre: response.data.plan_nombre || '',
        plan_precio: response.data.precio || 0,
        plan_duracion: response.data.duracion || 0,
        fecha_inicio: response.data.fecha_inicio || '',
        fecha_fin: response.data.fecha_fin || '',
        estado: response.data.estado || 'Activa',
        status: response.data.esta_activa || false,
        dias_restantes: response.data.dias_restantes || 0,
        esta_activa: response.data.esta_activa || false,
        esta_por_vencer: response.data.esta_por_vencer || false
      };
      
      return suscripcionData;
    }
    
    return null;
  } catch (error) {
    console.error('❌ Error obteniendo suscripción actual:', error);
    return null;
  }
};

// ✅ Función para suscribirse a un plan (CON empresaId y planId como parámetros requeridos)
export const suscribirseAPlan = async (planId: number, empresaId?: number, datosPago?: any): Promise<any> => {
  try {
    // Si no se proporciona empresaId, intentar obtenerlo del contexto
    let targetEmpresaId = empresaId;
    if (!targetEmpresaId) {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      targetEmpresaId = userData.empresa_id;
    }
    
    if (!targetEmpresaId) {
      throw new Error('No se pudo determinar el empresa_id para la suscripción');
    }

    console.log(`🔄 Suscribiendo empresa ${targetEmpresaId} al plan ${planId}...`);
    
    // Primero crear la suscripción
    const suscripcion = await crearSuscripcion(targetEmpresaId, planId);
    
    // Si se proporcionan datos de pago, procesarlos
    if (datosPago && suscripcion.suscripcion_id) {
      const pago = await procesarPago(
        suscripcion.suscripcion_id, 
        datosPago.monto || datosPago.precio || 0,
        datosPago.transaccion_id
      );
      
      console.log('✅ Suscripción y pago completados:', { suscripcion, pago });
      return { suscripcion, pago };
    }
    
    console.log('✅ Suscripción creada (sin pago):', suscripcion);
    return { suscripcion };
  } catch (error) {
    console.error('❌ Error en suscribirse a plan:', error);
    throw error;
  }
};

// ✅ Función para procesar pago simple (CORREGIR parámetros)
export const procesarPagoSimple = async (datosPago: {
  empresa_id: number;
  plan_id: number;
  monto_pago: number;
  metodo_pago?: string;
  transaccion_id?: string;
}): Promise<any> => {
  try {
    console.log('🔄 Procesando pago simple:', datosPago);
    
    // Usar el endpoint de pago simple del backend
    const response = await api.post('/subscriptions/pago-simple/', {
      empresa_id: datosPago.empresa_id,
      plan_id: datosPago.plan_id,
      monto_pago: datosPago.monto_pago
    });
    
    console.log('✅ Pago simple procesado:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error procesando pago simple:', error);
    throw error;
  }
};

// ✅ Función para obtener información completa de suscripción por empresa
export const obtenerInfoCompleta = async (empresaId: number): Promise<{
  suscripcion: SuscripcionEmpresa | null;
  tiene_suscripcion: boolean;
  requiere_pago: boolean;
  acceso_reportes: boolean;
  mensaje?: string;
}> => {
  try {
    console.log(`🔍 Obteniendo información completa para empresa ${empresaId}...`);
    
    const response = await api.get(`/subscriptions/info-empresa/?empresa_id=${empresaId}`);
    const data = response.data;
    
    let suscripcion = null;
    if (data.tiene_suscripcion) {
      suscripcion = await obtenerSuscripcionActual(empresaId);
    }
    
    return {
      suscripcion,
      tiene_suscripcion: data.tiene_suscripcion || false,
      requiere_pago: data.requiere_pago || false,
      acceso_reportes: data.acceso_reportes || false,
      mensaje: data.mensaje
    };
  } catch (error) {
    console.error('❌ Error obteniendo información completa:', error);
    return {
      suscripcion: null,
      tiene_suscripcion: false,
      requiere_pago: true,
      acceso_reportes: false,
      mensaje: 'Error al obtener información de suscripción'
    };
  }
};

// ✅ Función para verificar estado de suscripción
export const verificarEstadoSuscripcion = async (empresaId: number): Promise<{
  activa: boolean;
  vencida: boolean;
  porVencer: boolean;
  diasRestantes: number;
  mensaje: string;
}> => {
  try {
    const info = await obtenerInfoCompleta(empresaId);
    
    if (!info.suscripcion) {
      return {
        activa: false,
        vencida: false,
        porVencer: false,
        diasRestantes: 0,
        mensaje: 'No hay suscripción activa'
      };
    }
    
    const diasRestantes = info.suscripcion.dias_restantes || 0;
    const activa = info.suscripcion.esta_activa || false;
    const vencida = diasRestantes <= 0 && !activa;
    const porVencer = activa && diasRestantes <= 7;
    
    let mensaje = '';
    if (vencida) {
      mensaje = 'Su suscripción ha vencido. Renueve para continuar.';
    } else if (porVencer) {
      mensaje = `Su suscripción vence en ${diasRestantes} día(s).`;
    } else if (activa) {
      mensaje = `Suscripción activa. ${diasRestantes} días restantes.`;
    }
    
    return {
      activa,
      vencida,
      porVencer,
      diasRestantes,
      mensaje
    };
  } catch (error) {
    console.error('❌ Error verificando estado de suscripción:', error);
    return {
      activa: false,
      vencida: true,
      porVencer: false,
      diasRestantes: 0,
      mensaje: 'Error al verificar suscripción'
    };
  }
};

// ✅ Función combinada para suscribirse y pagar (RESTAURADA)
export const suscribirseYPagar = async (empresaId: number, planId: number, datosPago: any): Promise<any> => {
  try {
    console.log(`🔄 Procesando suscripción y pago para empresa ${empresaId}...`);
    
    // Primero crear la suscripción
    const suscripcion = await crearSuscripcion(empresaId, planId);
    
    // Luego procesar el pago
    const pago = await procesarPago(suscripcion.suscripcion_id, datosPago.monto, datosPago.transaccion_id);
    
    console.log('✅ Suscripción y pago completados:', { suscripcion, pago });
    return { suscripcion, pago };
  } catch (error) {
    console.error('❌ Error en suscripción y pago:', error);
    throw error;
  }
};

// ============= ALIASES PARA COMPATIBILIDAD =============
export const obtenerSuscripciones = listarSuscripciones;
export const obtenerPagos = listarPagos;

// ============= EXPORT POR DEFECTO SIN DUPLICACIONES =============
export default {
  // Planes
  listarPlanes,
  crearPlan,
  editarPlan,
  cambiarEstadoPlan,
  
  // Suscripciones
  listarSuscripciones,
  obtenerSuscripciones,
  crearSuscripcion,
  renovarSuscripcion,
  suspenderSuscripcion,
  reactivarSuscripcion,
  obtenerInfoSuscripcionEmpresa,
  obtenerSuscripcionActual,        // ✅ Agregar
  suscribirseAPlan,                // ✅ Agregar
  obtenerInfoCompleta,             // ✅ Agregar
  verificarEstadoSuscripcion,      // ✅ Agregar
  
  // Pagos
  listarPagos,
  obtenerPagos,
  procesarPago,
  procesarPagoSimple,              // ✅ Agregar
  suscribirseYPagar,               // ✅ Restaurar
  
  // Utilidades
  formatearPrecio,
  formatearDuracion,
  formatearFecha,
  getEstadoSuscripcionTexto,
  getEstadoSuscripcionColor,
  getEstadoPagoTexto
};