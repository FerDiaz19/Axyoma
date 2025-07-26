import React, { useState, useEffect } from 'react';
import { obtenerPlanes, iniciarPago, confirmarPagoTransferencia, PlanSuscripcion, DetallesTransferencia } from '../services/pagoService';
import '../css/SeleccionPlan.css';

declare const Stripe: any;

interface SeleccionPlanProps {
  onSuccess: () => void;
  stripePublicKey: string;
}

const SeleccionPlan: React.FC<SeleccionPlanProps> = ({ onSuccess, stripePublicKey }) => {
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<PlanSuscripcion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTransferencia, setShowTransferencia] = useState(false);
  const [detallesTransferencia, setDetallesTransferencia] = useState<DetallesTransferencia | null>(null);
  const [comprobante, setComprobante] = useState<File | null>(null);
  const [pagoId, setPagoId] = useState<number | null>(null);

  useEffect(() => {
    cargarPlanes();
  }, []);

  const cargarPlanes = async () => {
    try {
      const data = await obtenerPlanes();
      setPlanes(data);
    } catch (error) {
      setError('Error al cargar los planes disponibles');
    } finally {
      setLoading(false);
    }
  };

  const handlePlanSelect = (plan: PlanSuscripcion) => {
    setSelectedPlan(plan);
    setError(null);
  };

  const handlePagoStripe = async () => {
    if (!selectedPlan) {
      setError('Por favor selecciona un plan');
      return;
    }

    try {
      setLoading(true);
      const response = await iniciarPago(selectedPlan.plan_id, 'stripe');
      
      if (response.session_id) {
        const stripe = Stripe(stripePublicKey);
        const { error } = await stripe.redirectToCheckout({
          sessionId: response.session_id
        });

        if (error) {
          setError(error.message);
        }
      }
    } catch (error: any) {
      setError(error.message || 'Error al procesar el pago');
    } finally {
      setLoading(false);
    }
  };

  const handlePagoTransferencia = async () => {
    if (!selectedPlan) {
      setError('Por favor selecciona un plan');
      return;
    }

    try {
      setLoading(true);
      const response = await iniciarPago(selectedPlan.plan_id, 'transferencia');
      
      if (response.detalles_transferencia) {
        setDetallesTransferencia(response.detalles_transferencia);
        setPagoId(response.pago_id!);
        setShowTransferencia(true);
      }
    } catch (error: any) {
      setError(error.message || 'Error al generar la información de transferencia');
    } finally {
      setLoading(false);
    }
  };

  const handleComprobanteChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setComprobante(event.target.files[0]);
    }
  };

  const handleConfirmarTransferencia = async () => {
    if (!comprobante || !pagoId) {
      setError('Por favor sube el comprobante de pago');
      return;
    }

    try {
      setLoading(true);
      // Aquí deberías primero subir el comprobante a tu servidor o a un servicio de almacenamiento
      // y obtener la URL. Por ahora usaremos un placeholder
      const comprobanteUrl = 'URL_DEL_COMPROBANTE';
      
      await confirmarPagoTransferencia(pagoId, comprobanteUrl);
      onSuccess();
    } catch (error: any) {
      setError(error.message || 'Error al confirmar el pago');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando planes disponibles...</div>;
  }

  return (
    <div className="seleccion-plan">
      <h2>Selecciona tu Plan</h2>
      
      {error && <div className="error-message">{error}</div>}

      <div className="planes-grid">
        {planes.map(plan => (
          <div 
            key={plan.plan_id} 
            className={`plan-card ${selectedPlan?.plan_id === plan.plan_id ? 'selected' : ''}`}
            onClick={() => handlePlanSelect(plan)}
          >
            <h3>{plan.nombre}</h3>
            <div className="precio">${plan.precio}/mes</div>
            <div className="duracion">{plan.duracion} días</div>
            {plan.descripcion && <p>{plan.descripcion}</p>}
            {plan.caracteristicas && (
              <ul className="caracteristicas">
                {plan.caracteristicas.split('\n').map((caracteristica, index) => (
                  <li key={index}>{caracteristica}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      {selectedPlan && !showTransferencia && (
        <div className="metodos-pago">
          <h3>Selecciona el método de pago</h3>
          <button onClick={handlePagoStripe} disabled={loading}>
            Pagar con Tarjeta
          </button>
          <button onClick={handlePagoTransferencia} disabled={loading}>
            Pagar con Transferencia
          </button>
        </div>
      )}

      {showTransferencia && detallesTransferencia && (
        <div className="detalles-transferencia">
          <h3>Datos para la Transferencia</h3>
          <div className="datos-bancarios">
            <p><strong>Banco:</strong> {detallesTransferencia.banco}</p>
            <p><strong>Cuenta:</strong> {detallesTransferencia.cuenta}</p>
            <p><strong>CLABE:</strong> {detallesTransferencia.clabe}</p>
            <p><strong>Beneficiario:</strong> {detallesTransferencia.beneficiario}</p>
            <p><strong>Referencia:</strong> {detallesTransferencia.referencia}</p>
          </div>
          
          <div className="upload-comprobante">
            <h4>Subir Comprobante de Pago</h4>
            <input 
              type="file" 
              accept="image/*,.pdf" 
              onChange={handleComprobanteChange}
            />
            {comprobante && (
              <button 
                onClick={handleConfirmarTransferencia}
                disabled={loading}
              >
                Confirmar Pago
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SeleccionPlan;
