import React, { useState, useEffect } from 'react';
import { listarPlanes, suscribirseAPlan, formatearPrecio, type PlanSuscripcion } from '../services/suscripcionService';
import '../css/PlanSelection.css';

interface PlanSelectionProps {
  empresaId?: number;
  onPlanSelected: () => void;
  onSkip?: () => void;
}

const PlanSelection: React.FC<PlanSelectionProps> = ({ empresaId: propEmpresaId, onPlanSelected, onSkip }) => {
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [processingPayment, setProcessingPayment] = useState(false);
  
  // Obtener empresaId de props o localStorage
  const getEmpresaId = (): number | undefined => {
    if (propEmpresaId) return propEmpresaId;
    
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    return userData.empresa_id;
  };
  
  const empresaId = getEmpresaId();

  console.log(`🏢 PlanSelection inicializado para empresa ID: ${empresaId}`);

  useEffect(() => {
    cargarPlanes();
  }, []);

  const cargarPlanes = async () => {
    setLoading(true);
    try {
      const response = await listarPlanes();
      console.log('📋 Planes cargados:', response);
      
      if (Array.isArray(response)) {
        const planesActivos = response.filter((plan: PlanSuscripcion) => plan.status !== false);
        setPlanes(planesActivos);
      } else {
        console.error('❌ La respuesta no es un array:', response);
        setPlanes([]);
      }
    } catch (error) {
      console.error('❌ Error cargando planes:', error);
      alert('Error al cargar los planes disponibles');
      setPlanes([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId: number) => {
    if (processingPayment) return;
    
    if (!empresaId) {
      alert('Error: No se pudo identificar la empresa. Por favor, inicia sesión nuevamente.');
      return;
    }
    
    setProcessingPayment(true);
    try {
      const plan = planes.find(p => p.plan_id === planId);
      const confirmMessage = `¿Confirmar suscripción al plan "${plan?.nombre}"?\n\nPrecio: ${formatearPrecio(plan?.precio || 0)}\nDuración: ${plan?.duracion} días\n\nSe procesará el pago inmediatamente.`;
      
      if (window.confirm(confirmMessage)) {
        console.log(`🎯 Suscribiendo empresa ${empresaId} al plan ${planId}`);
        const result = await suscribirseAPlan(planId, empresaId);
        
        let successMessage = '¡Suscripción activada exitosamente!';
        if (result.pago) {
          const monto = result.pago.monto_pago || result.pago.costo || 0;
          const transaccion = result.pago.transaccion_id || 'N/A';
          const estado = result.pago.estado_pago || 'completado';
          successMessage += `\n\nDetalles del pago:\n- Monto: ${formatearPrecio(monto)}\n- Transacción: ${transaccion}\n- Estado: ${estado}`;
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

  if (!empresaId) {
    return (
      <div className="plan-selection-container">
        <div className="plan-selection-header">
          <h2>⚠️ Error de Empresa</h2>
          <p>No se pudo identificar la empresa. Por favor, regresa al registro o inicia sesión.</p>
        </div>
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button 
            onClick={() => window.location.href = '/registro'}
            className="skip-btn"
          >
            Regresar al Registro
          </button>
        </div>
      </div>
    );
  }

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
        {planes.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px', 
            background: '#f9f9f9', 
            borderRadius: '10px',
            color: '#666'
          }}>
            <h3>😔 No hay planes disponibles</h3>
            <p>Por favor, contacta con soporte técnico.</p>
            <button onClick={cargarPlanes} style={{ marginTop: '10px' }}>
              🔄 Reintentar cargar planes
            </button>
          </div>
        ) : (
          planes.map((plan) => (
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
          ))
        )}
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
