import React, { useState, useEffect } from 'react';
import {
  obtenerSuscripcionActual,
  listarPlanes,
  suscribirseAPlan,
  formatearPrecio,
  formatearDuracion,
  formatearFecha,
  type PlanSuscripcion,
  obtenerInfoSuscripcionEmpresa
} from '../services/suscripcionService';
import '../css/GestionSuscripcion.css';

interface GestionSuscripcionProps {
  empresaId: number;
}

const GestionSuscripcion: React.FC<GestionSuscripcionProps> = ({ empresaId }) => {
  const [loading, setLoading] = useState(true);
  const [suscripcionInfo, setSuscripcionInfo] = useState<any>(null);
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [mostrarPlanes, setMostrarPlanes] = useState(false);
  const [procesandoPlan, setProcesandoPlan] = useState<number | null>(null);

  useEffect(() => {
    cargarDatos();
  }, [empresaId]);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      // Usar obtenerSuscripcionActual y si no hay, mostrar el objeto completo recibido
      const infoSuscripcion = await obtenerSuscripcionActual(empresaId);
      // Si no hay suscripcion_id o estado, mostrar la info cruda del endpoint
      if (!infoSuscripcion || !infoSuscripcion.suscripcion_id || !infoSuscripcion.estado) {
        // Usa la función obtenerInfoSuscripcionEmpresa que ya hace el mapeo correcto
        try {
          const rawData = await obtenerInfoSuscripcionEmpresa(empresaId);
          setSuscripcionInfo(rawData);
        } catch (err) {
          setSuscripcionInfo({
            tiene_suscripcion: false,
            estado: 'sin_suscripcion',
            mensaje: 'No se pudo obtener información de suscripción (error de red o formato)'
          });
        }
      } else {
        setSuscripcionInfo(infoSuscripcion);
      }
      const planesData = await listarPlanes();
      setPlanes(planesData);
    } catch (error) {
      console.error('Error cargando datos:', error);
      setSuscripcionInfo({
        tiene_suscripcion: false,
        estado: 'sin_suscripcion',
        mensaje: 'Error al cargar información de suscripción'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSeleccionarPlan = async (planId: number) => {
    // Validación antes de enviar al backend
    if (!empresaId || !planId) {
      alert('Faltan datos para crear la suscripción. Verifica que la empresa y el plan sean válidos.');
      setProcesandoPlan(null);
      return;
    }
    try {
      setProcesandoPlan(planId);
      const resultado = await suscribirseAPlan(planId, empresaId);
      
      alert(`Suscripción exitosa`);
      
      await cargarDatos();
      setMostrarPlanes(false);
      
    } catch (error: any) {
      console.error('Error al suscribirse:', error);
      alert(error.message || 'Error al procesar la suscripción');
    } finally {
      setProcesandoPlan(null);
    }
  };

  if (loading) {
    return (
      <div className="gestion-suscripcion loading">
        <div className="loading-content">
          <h2>Cargando información de suscripción...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="gestion-suscripcion">
      <div className="suscripcion-header">
        <h2>Gestión de Suscripción</h2>
        <p>Administra tu plan de suscripción</p>
      </div>

      <div className="suscripcion-actual">
        <h3>Estado Actual</h3>
        {/* Mostrar mensaje claro si hay error o no hay suscripción */}
        {suscripcionInfo?.estado === 'sin_suscripcion' ? (
          <div className="sin-suscripcion">
            <h4>Sin Suscripción Activa</h4>
            <p>{suscripcionInfo?.mensaje || 'No tienes una suscripción activa.'}</p>
            <button 
              onClick={() => setMostrarPlanes(true)}
              className="btn-contratar"
            >
              Ver Planes Disponibles
            </button>
          </div>
        ) : suscripcionInfo?.tiene_suscripcion ? (
          <div className="suscripcion-activa">
            <div className="plan-info">
              <h4>Suscripción Activa</h4>
              <div className="plan-details">
                <div className="detail-item">
                  <strong>Plan:</strong> {suscripcionInfo.plan_nombre}
                </div>
                <div className="detail-item">
                  <strong>Precio:</strong> {formatearPrecio(suscripcionInfo.precio)}
                </div>
                <div className="detail-item">
                  <strong>Duración:</strong> {formatearDuracion(suscripcionInfo.duracion)}
                </div>
                <div className="detail-item">
                  <strong>Fecha de inicio:</strong> {formatearFecha(suscripcionInfo.fecha_inicio)}
                </div>
                <div className="detail-item">
                  <strong>Fecha de fin:</strong> {formatearFecha(suscripcionInfo.fecha_fin)}
                </div>
                <div className="detail-item">
                  <strong>Días restantes:</strong> 
                  <span className={`dias-restantes ${suscripcionInfo.esta_por_vencer ? 'warning' : 'active'}`}>
                    {suscripcionInfo.dias_restantes} días
                  </span>
                </div>
              </div>
            </div>
            
            {suscripcionInfo.esta_por_vencer && (
              <div className="alerta-vencimiento">
                <h4>Suscripción próxima a vencer</h4>
                <p>Tu suscripción vence en {suscripcionInfo.dias_restantes} días.</p>
                <button 
                  onClick={() => setMostrarPlanes(true)}
                  className="btn-renovar"
                >
                  Renovar Suscripción
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="sin-suscripcion">
            <h4>No se pudo obtener el estado de la suscripción</h4>
            <p>{suscripcionInfo?.mensaje || 'Intenta recargar la página o contactar soporte.'}</p>
          </div>
        )}
      </div>

      {!mostrarPlanes && suscripcionInfo?.tiene_suscripcion && (
        <div className="acciones-suscripcion">
          <button 
            onClick={() => setMostrarPlanes(true)}
            className="btn-secondary"
          >
            Ver Otros Planes
          </button>
        </div>
      )}

      {mostrarPlanes && (
        <div className="planes-disponibles">
          <div className="planes-header">
            <h3>Planes Disponibles</h3>
            <button 
              onClick={() => setMostrarPlanes(false)}
              className="btn-close"
            >
              Cerrar
            </button>
          </div>
          
          <div className="planes-grid">
            {planes.map((plan) => (
              <div key={plan.plan_id} className={`plan-card ${!plan.status ? 'disabled' : ''}`}>
                <div className="plan-header">
                  <h4>{plan.nombre}</h4>
                  <div className="plan-precio">
                    {formatearPrecio(plan.precio)}
                    <small>por {formatearDuracion(plan.duracion)}</small>
                  </div>
                </div>
                
                <div className="plan-body">
                  {plan.descripcion && (
                    <p className="plan-descripcion">{plan.descripcion}</p>
                  )}
                  
                  <div className="plan-features">
                    <div className="feature">
                      <strong>Duración:</strong> {formatearDuracion(plan.duracion)}
                    </div>
                    <div className="feature">
                      <strong>Precio:</strong> {formatearPrecio(plan.precio)}
                    </div>
                    <div className="feature">
                      <strong>Estado:</strong> 
                      <span className={plan.status ? 'active' : 'inactive'}>
                        {plan.status ? 'Disponible' : 'No disponible'}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="plan-footer">
                  {plan.status ? (
                    <button
                      onClick={() => handleSeleccionarPlan(plan.plan_id)}
                      disabled={procesandoPlan === plan.plan_id}
                      className="btn-seleccionar"
                    >
                      {procesandoPlan === plan.plan_id ? (
                        'Procesando...'
                      ) : (
                        'Seleccionar Plan'
                      )}
                    </button>
                  ) : (
                    <button disabled className="btn-disabled">
                      No Disponible
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
          
          {planes.length === 0 && (
            <div className="no-planes">
              <p>No hay planes disponibles en este momento.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GestionSuscripcion;
