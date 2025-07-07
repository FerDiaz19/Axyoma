import React, { useState, useEffect } from 'react';
import { listarPlanes, suscribirseAPlan, formatearPrecio, type PlanSuscripcion } from '../services/suscripcionService';
import '../css/PlanSelection.css';

interface PlanSelectionProps {
  empresaId: number;
  onPlanSelected: () => void;
  onSkip?: () => void;
}

const PlanSelection: React.FC<PlanSelectionProps> = ({ empresaId, onPlanSelected, onSkip }) => {
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [processingPayment, setProcessingPayment] = useState(false);

  useEffect(() => {
    cargarPlanes();
  }, []);

  const cargarPlanes = async () => {
    setLoading(true);
    try {
      const response = await listarPlanes();
      setPlanes(response.filter((plan: PlanSuscripcion) => plan.status));
    } catch (error) {
      console.error('Error cargando planes:', error);
      alert('Error al cargar los planes disponibles');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId: number) => {
    if (processingPayment) return;
    
    setProcessingPayment(true);
    try {
      const plan = planes.find(p => p.plan_id === planId);
      const confirmMessage = `¿Confirmar suscripción al plan "${plan?.nombre}"?\n\nPrecio: ${formatearPrecio(plan?.precio || 0)}\nDuración: ${plan?.duracion} días\n\nSe procesará el pago inmediatamente.`;
      
      if (window.confirm(confirmMessage)) {
        const result = await suscribirseAPlan(planId);
        
        let successMessage = '¡Suscripción activada exitosamente!';
        if (result.pago) {
          successMessage += `\n\nDetalles del pago:\n- Monto: ${formatearPrecio(parseFloat(result.pago.monto_pago))}\n- Transacción: ${result.pago.transaccion_id}\n- Estado: ${result.pago.estado_pago}`;
        }
        successMessage += '\n\nYa puedes acceder a todas las funcionalidades.';
        
        alert(successMessage);
        
        // Notificar que la suscripción fue actualizada y redirigir
        localStorage.setItem('subscription_updated', 'true');
        window.location.href = '/?refresh=true';
        onPlanSelected();
      }
    } catch (error: any) {
      console.error('Error procesando suscripción:', error);
      alert(error.message || 'Error al procesar la suscripción');
    } finally {
      setProcessingPayment(false);
    }
  };

  if (loading) {
    return (
      <div className="plan-selection-container">
        <div className="loading">🔄 Cargando planes disponibles...</div>
      </div>
    );
  }

  return (
    <div className="plan-selection-container">
      <div className="plan-selection-header">
        <h2>🎯 Selecciona tu Plan de Suscripción</h2>
        <p>Para completar el registro de tu empresa, selecciona el plan que mejor se adapte a tus necesidades.</p>
      </div>

      <div className="planes-grid">
        {planes.map((plan) => (
          <div 
            key={plan.plan_id} 
            className={`plan-card ${selectedPlan === plan.plan_id ? 'selected' : ''}`}
            onClick={() => setSelectedPlan(plan.plan_id)}
          >
            <div className="plan-header">
              <h3>{plan.nombre}</h3>
              <div className="plan-price">
                <span className="price">{formatearPrecio(plan.precio)}</span>
                <span className="period">/{plan.duracion} días</span>
              </div>
            </div>

            <div className="plan-description">
              <p>{plan.descripcion || 'Plan completo para tu empresa'}</p>
            </div>

            <div className="plan-duration">
              <div className="duration-item">
                <span className="icon">📅</span>
                <span>Duración: {plan.duracion} días</span>
              </div>
            </div>

            <button 
              className={`select-plan-btn ${selectedPlan === plan.plan_id ? 'selected' : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                handleSelectPlan(plan.plan_id);
              }}
              disabled={processingPayment}
            >
              {processingPayment && selectedPlan === plan.plan_id ? (
                <>🔄 Procesando...</>
              ) : (
                <>💳 Seleccionar Plan</>
              )}
            </button>
          </div>
        ))}
      </div>

      <div className="plan-selection-footer">
        <p className="payment-info">
          💳 <strong>Pago seguro:</strong> Tu suscripción se activará inmediatamente después del pago.
        </p>
        
        {onSkip && (
          <button 
            className="skip-btn"
            onClick={onSkip}
            disabled={processingPayment}
          >
            ⏭️ Omitir por ahora (funcionalidades limitadas)
          </button>
        )}
      </div>
    </div>
  );
};

export default PlanSelection;
