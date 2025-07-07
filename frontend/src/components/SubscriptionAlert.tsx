import React, { useState } from 'react';
import PlanSelection from './PlanSelection';
import '../css/SubscriptionAlert.css';

interface SubscriptionAlertProps {
  empresaId: number;
  empresaNombre: string;
  tipoAlerta: 'sin_suscripcion' | 'vencida' | 'por_vencer';
  diasRestantes?: number;
  onSubscriptionUpdated: () => void;
  onContinueWithLimitations?: () => void;
}

const SubscriptionAlert: React.FC<SubscriptionAlertProps> = ({
  empresaId,
  empresaNombre,
  tipoAlerta,
  diasRestantes,
  onSubscriptionUpdated,
  onContinueWithLimitations
}) => {
  const [showPlanSelection, setShowPlanSelection] = useState(false);

  const getAlertInfo = () => {
    switch (tipoAlerta) {
      case 'sin_suscripcion':
        return {
          icon: '⚠️',
          title: 'Suscripción Requerida',
          message: `La empresa "${empresaNombre}" no tiene una suscripción activa.`,
          description: 'Para acceder a todas las funcionalidades del sistema, necesitas activar una suscripción.',
          buttonText: '💳 Activar Suscripción',
          alertClass: 'warning'
        };
      case 'vencida':
        return {
          icon: '🚫',
          title: 'Suscripción Vencida',
          message: `La suscripción de "${empresaNombre}" ha vencido.`,
          description: 'Tu acceso está limitado. Renueva tu suscripción para continuar usando todas las funcionalidades.',
          buttonText: '🔄 Renovar Suscripción',
          alertClass: 'danger'
        };
      case 'por_vencer':
        return {
          icon: '⏰',
          title: 'Suscripción por Vencer',
          message: `La suscripción de "${empresaNombre}" vence en ${diasRestantes} día(s).`,
          description: 'Renueva tu suscripción antes de que venza para evitar interrupciones en el servicio.',
          buttonText: '🔄 Renovar Ahora',
          alertClass: 'warning'
        };
      default:
        return {
          icon: '❓',
          title: 'Estado Desconocido',
          message: 'Estado de suscripción no reconocido.',
          description: 'Contacta con soporte técnico.',
          buttonText: 'Contactar Soporte',
          alertClass: 'info'
        };
    }
  };

  const alertInfo = getAlertInfo();

  const getFunctionalityStatus = () => {
    const baseFeatures = [
      { name: '👥 Gestión de Usuarios', available: true },
      { name: '🏭 Gestión de Plantas', available: true },
      { name: '🏢 Gestión de Departamentos', available: true },
      { name: '💼 Gestión de Puestos', available: true },
      { name: '👤 Gestión de Empleados', available: true },
    ];

    const premiumFeatures = [
      { name: '📊 Reportes Avanzados', available: false },
      { name: '📝 Sistema de Evaluaciones', available: false },
      { name: '📈 Análisis y Métricas', available: false },
      { name: '🔔 Notificaciones Avanzadas', available: false },
    ];

    return { baseFeatures, premiumFeatures };
  };

  const { baseFeatures, premiumFeatures } = getFunctionalityStatus();

  if (showPlanSelection) {
    return (
      <PlanSelection
        empresaId={empresaId}
        onPlanSelected={() => {
          setShowPlanSelection(false);
          onSubscriptionUpdated();
        }}
        onSkip={() => {
          setShowPlanSelection(false);
          if (onContinueWithLimitations) {
            onContinueWithLimitations();
          }
        }}
      />
    );
  }

  return (
    <div className="subscription-alert-overlay">
      <div className="subscription-alert-container">
        <div className={`subscription-alert ${alertInfo.alertClass}`}>
          <div className="alert-header">
            <div className="alert-icon">{alertInfo.icon}</div>
            <h2>{alertInfo.title}</h2>
          </div>

          <div className="alert-content">
            <p className="alert-message">{alertInfo.message}</p>
            <p className="alert-description">{alertInfo.description}</p>

            <div className="functionality-status">
              <h3>📋 Estado de Funcionalidades</h3>
              
              <div className="features-section">
                <h4>✅ Funcionalidades Disponibles</h4>
                <ul className="features-list available">
                  {baseFeatures.map((feature, index) => (
                    <li key={index} className="feature-item">
                      <span className="feature-icon">✅</span>
                      <span>{feature.name}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="features-section">
                <h4>🚫 Funcionalidades Restringidas</h4>
                <ul className="features-list restricted">
                  {premiumFeatures.map((feature, index) => (
                    <li key={index} className="feature-item">
                      <span className="feature-icon">🚫</span>
                      <span>{feature.name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          <div className="alert-actions">
            <button 
              className="btn-primary subscription-btn"
              onClick={() => setShowPlanSelection(true)}
            >
              {alertInfo.buttonText}
            </button>

            {onContinueWithLimitations && (
              <button 
                className="btn-secondary continue-btn"
                onClick={onContinueWithLimitations}
              >
                ⏭️ Continuar con Limitaciones
              </button>
            )}
          </div>

          <div className="alert-footer">
            <p className="support-info">
              💡 <strong>¿Necesitas una suscripción?</strong> Activa tu plan ahora para acceder a todas las funcionalidades premium del sistema.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionAlert;
