import React, { useState, useEffect } from 'react';
import { obtenerSuscripcionActual, listarPlanes, type PlanSuscripcion } from '../services/suscripcionService';
import '../css/GestionSuscripcion.css';

interface GestionSuscripcionProps {
  empresaId: number;
}

const GestionSuscripcion: React.FC<GestionSuscripcionProps> = ({ empresaId }) => {
  console.log('Renderizando GestionSuscripcion con empresaId:', empresaId);
  const [suscripcion, setSuscripcion] = useState<any>(null);
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showPlanes, setShowPlanes] = useState(false);

useEffect(() => {
  if (empresaId) {
    cargarDatos();
  }
}, [empresaId]);

  const cargarDatos = async () => {
    console.log('Iniciando carga de datos...');
    try {
      if (!empresaId) {
        throw new Error('ID de empresa no válido');
      }
      const [suscripcionData, planesData] = await Promise.all([
        obtenerSuscripcionActual(),
        listarPlanes()
      ]);
      console.log('Datos recibidos:', { suscripcionData, planesData });
      setSuscripcion(suscripcionData);
      setPlanes(planesData);
    } catch (error: any) {
      console.error('Error cargando datos de suscripción:', error);
      setError(error.message || 'No se pudo cargar la información de suscripción');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="gestion-suscripcion">
        <div className="loading">Cargando información de suscripción...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="gestion-suscripcion">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  // Función para renderizar la lista de planes disponibles
  const renderPlanes = () => {
    return (
      <div className="planes-disponibles">
        <h3>Planes Disponibles</h3>
        <div className="planes-grid">
          {planes.map(plan => (
            <div key={plan.plan_id} className="plan-card">
              <h4>{plan.nombre}</h4>
              <p>{plan.descripcion}</p>
              <div className="plan-precio">
                Precio: ${plan.precio}
              </div>
              <div className="plan-duracion">
                Duración: {plan.duracion} días
              </div>
              <button 
                className="seleccionar-plan-btn"
                onClick={() => setShowPlanes(false)}
              >
                Seleccionar Plan
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="gestion-suscripcion">
      <div className="header-section">
        <h2>💎 Suscripción Actual</h2>
      </div>

      {showPlanes ? (
        renderPlanes()
      ) : suscripcion ? (
        <div className="suscripcion-info">
          <div className="plan-actual">
            <div className="plan-header">
              <h3>{suscripcion.plan_nombre}</h3>
              <span className={`estado ${suscripcion.estado.toLowerCase()}`}>
                {suscripcion.estado}
              </span>
            </div>
            
            <div className="plan-detalles">
              <div className="detalle">
                <span className="label">Fecha de inicio:</span>
                <span className="valor">{new Date(suscripcion.fecha_inicio).toLocaleDateString()}</span>
              </div>
              <div className="detalle">
                <span className="label">Fecha de vencimiento:</span>
                <span className="valor">{new Date(suscripcion.fecha_fin).toLocaleDateString()}</span>
              </div>
              <div className="detalle">
                <span className="label">Días restantes:</span>
                <span className="valor">{suscripcion.dias_restantes} días</span>
              </div>
            </div>

            {suscripcion.esta_por_vencer && (
              <div className="alerta-vencimiento">
                ⚠️ Tu suscripción está por vencer. Renueva ahora para mantener todas las funcionalidades.
              </div>
            )}
          </div>

          <div className="funcionalidades">
            <h4>Funcionalidades Incluidas</h4>
            <ul>
              <li>✅ Gestión ilimitada de empleados</li>
              <li>✅ Todas las herramientas de evaluación</li>
              <li>✅ Reportes avanzados</li>
              <li>✅ Soporte prioritario</li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="sin-suscripcion">
          <div className="mensaje-principal">
            <h3>⚠️ No tienes un plan activo</h3>
            <p>Algunas funcionalidades están restringidas. Activa un plan para acceder a todas las características.</p>
          </div>

          <div className="funcionalidades-restringidas">
            <h4>Funcionalidades Restringidas</h4>
            <ul>
              <li>❌ Límite de 5 empleados</li>
              <li>❌ Evaluaciones básicas únicamente</li>
              <li>❌ Sin acceso a reportes avanzados</li>
              <li>❌ Soporte limitado</li>
            </ul>
          </div>

          <button className="activar-plan-btn" onClick={() => setShowPlanes(true)}>
            💎 Activar Plan Ahora
          </button>
        </div>
      )}
    </div>
  );
};

export default GestionSuscripcion;
