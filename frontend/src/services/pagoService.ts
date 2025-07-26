import api from '../api';

export interface PlanSuscripcion {
  plan_id: number;
  nombre: string;
  descripcion?: string;
  precio: number;
  duracion: number;
  limite_empleados?: number;
  limite_plantas?: number;
  caracteristicas?: string;
}

export interface DetallesTransferencia {
  banco: string;
  cuenta: string;
  clabe: string;
  beneficiario: string;
  referencia: string;
}

export interface RespuestaPago {
  session_id?: string;
  url?: string;
  pago_id?: number;
  detalles_transferencia?: DetallesTransferencia;
}

export const obtenerPlanes = async (): Promise<PlanSuscripcion[]> => {
  const response = await api.get('/subscriptions/planes/');
  return response.data;
};

export const iniciarPago = async (plan_id: number, metodo_pago: 'stripe' | 'transferencia'): Promise<RespuestaPago> => {
  const response = await api.post('/subscriptions/iniciar_pago/', {
    plan_id,
    metodo_pago
  });
  return response.data;
};

export const confirmarPagoTransferencia = async (pago_id: number, comprobante: string): Promise<any> => {
  const response = await api.post('/subscriptions/confirmar_pago/', {
    pago_id,
    comprobante
  });
  return response.data;
};
