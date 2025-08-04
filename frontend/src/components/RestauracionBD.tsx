/**
 * 🔧 RESTAURACIÓN DE BASE DE DATOS - FRONTEND
 * ===========================================
 * 
 * Componente React para funciones avanzadas de restauración de BD.
 * Interfaz de usuario para SuperAdmin con operaciones críticas.
 * 
 * 📋 Responsable: Yael Contreras
 * 📅 Fecha: Agosto 2025
 * 🔢 Versión: 1.0
 * 
 * 🚀 Funcionalidades:
 * - Reiniciar BD a cero (mantener estructura)
 * - Cargar datos de demostración 
 * - Estado de la BD y estadísticas
 * - Confirmaciones de seguridad múltiples
 * 
 * 🔒 Seguridad: Solo accesible para SuperAdmin
 * ⚠️ PELIGRO: Operaciones irreversibles
 */

import React, { useState, useEffect } from 'react';
import { 
  obtenerEstadoBDRestauracion, 
  reiniciarBDCero, 
  cargarDatosDemo,
  type EstadoBDRestauracion,
  type ResultadoReiniciarBD,
  type ResultadoCargarDemo
} from '../services/adminBDService';
import '../css/RestauracionBD.css';

interface MensajeProps {
  texto: string;
  tipo: 'success' | 'error' | 'info' | 'warning';
}

const RestauracionBD: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [estadoBD, setEstadoBD] = useState<EstadoBDRestauracion | null>(null);
  const [mensaje, setMensaje] = useState<MensajeProps | null>(null);

  useEffect(() => {
    cargarEstadoBD();
  }, []);
  const cargarEstadoBD = async () => {
    try {
      setLoading(true);
      const data = await obtenerEstadoBDRestauracion();
      setEstadoBD(data);
    } catch (error: any) {
      console.error('Error:', error);
      mostrarMensaje('Error al cargar estado de BD', 'error');
    } finally {
      setLoading(false);
    }
  };

  const mostrarMensaje = (texto: string, tipo: MensajeProps['tipo']) => {
    setMensaje({ texto, tipo });
    setTimeout(() => setMensaje(null), 5000);
  };
  const handleReiniciarBD = async () => {
    // Primera confirmación
    const confirmacion1 = window.confirm(
      '⚠️ PELIGRO: ¿Está seguro de reiniciar la BD a cero?\n\n' +
      'Esta acción eliminará TODOS los datos manteniendo solo la estructura.\n' +
      'Solo se conservará el usuario SuperAdmin.\n\n' +
      '¿Desea continuar?'
    );

    if (!confirmacion1) return;    // Segunda confirmación con texto específico
    const confirmacion2 = window.prompt(
      '🔴 CONFIRMACIÓN FINAL:\n\n' +
      'Para proceder, escriba exactamente: CONFIRMO_REINICIAR_BD\n\n' +
      'Esta acción es IRREVERSIBLE:'
    );

    if (confirmacion2 !== 'CONFIRMO_REINICIAR_BD') {
      mostrarMensaje('Operación cancelada - texto incorrecto', 'info');
      return;
    }    try {
      setLoading(true);
      const data = await reiniciarBDCero(confirmacion2);
      
      mostrarMensaje(
        '✅ BD reiniciada exitosamente\n\n' +
        `📊 Tablas limpiadas: ${data.tablas_limpiadas?.length || 0}\n` +
        `🔄 Secuencias reiniciadas: ${data.secuencias_reiniciadas?.length || 0}\n\n` +
        '👤 Usuario SuperAdmin conservado\n' +
        '💡 Recomendación: Cargar datos demo para pruebas',
        'success'
      );
      await cargarEstadoBD();
    } catch (error: any) {
      console.error('Error:', error);
      mostrarMensaje(`❌ Error: ${error.message || 'Error desconocido'}`, 'error');
    } finally {
      setLoading(false);
    }
  };
  const handleCargarDatosDemo = async () => {
    const confirmacion = window.confirm(
      '📊 ¿Cargar datos de demostración?\n\n' +
      'Se creará:\n' +
      '• 1 empresa demo con estructura completa\n' +
      '• 3 usuarios de prueba\n' +
      '• Planes de suscripción\n' +
      '• 1 empleado de ejemplo\n\n' +
      'Esta operación es segura y no elimina datos existentes.'
    );

    if (!confirmacion) return;

    try {
      setLoading(true);
      const data = await cargarDatosDemo();
      
      mostrarMensaje(
        '✅ Datos demo cargados exitosamente\n\n' +
        `👥 Usuarios creados: ${data.usuarios_creados || 0}\n` +
        `🏢 Empresas: ${data.empresas_creadas || 0}\n` +
        `🏭 Plantas: ${data.plantas_creadas || 0}\n` +
        `📋 Departamentos: ${data.departamentos_creados || 0}\n` +
        `💼 Puestos: ${data.puestos_creados || 0}\n` +
        `👤 Empleados: ${data.empleados_creados || 0}\n\n` +
        '🎉 ¡Sistema listo para demostrar!',
        'success'
      );
      await cargarEstadoBD();
    } catch (error: any) {
      console.error('Error:', error);
      mostrarMensaje(`❌ Error: ${error.message || 'Error desconocido'}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="restauracion-bd">
      <div className="restauracion-header">
        <h2>🔧 Restauración de Base de Datos</h2>
        <p className="restauracion-subtitle">
          Funciones avanzadas para gestión completa de la base de datos
        </p>
        <button 
          onClick={cargarEstadoBD}
          className="btn-refresh"
          disabled={loading}
        >
          {loading ? '⏳ Cargando...' : '🔄 Actualizar Estado'}
        </button>
      </div>

      {mensaje && (
        <div className={`mensaje mensaje-${mensaje.tipo}`}>
          <div className="mensaje-content">
            {mensaje.texto.split('\n').map((linea, i) => (
              <div key={i}>{linea}</div>
            ))}
          </div>
          <button 
            onClick={() => setMensaje(null)}
            className="mensaje-cerrar"
          >
            ✕
          </button>
        </div>
      )}

      {/* Estado actual de la BD */}
      <div className="estado-bd-card">
        <h3>📊 Estado Actual de la Base de Datos</h3>
        {estadoBD ? (
          <div className="estado-content">
            <div className="estado-grid">
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.total_registros}</span>
                <span className="estado-label">Total Registros</span>
              </div>
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.empresas}</span>
                <span className="estado-label">Empresas</span>
              </div>
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.empleados}</span>
                <span className="estado-label">Empleados</span>
              </div>
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.usuarios}</span>
                <span className="estado-label">Usuarios</span>
              </div>
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.plantas}</span>
                <span className="estado-label">Plantas</span>
              </div>
              <div className="estado-item">
                <span className="estado-numero">{estadoBD.departamentos}</span>
                <span className="estado-label">Departamentos</span>
              </div>
            </div>
            
            <div className="estado-status">
              <div className={`bd-status ${estadoBD.bd_vacia ? 'vacia' : 'con-datos'}`}>
                {estadoBD.bd_vacia ? '🗃️ BD Vacía' : '📊 BD Con Datos'}
              </div>
              {estadoBD.fecha_ultimo_respaldo && (
                <div className="ultimo-respaldo">
                  📅 Último respaldo: {new Date(estadoBD.fecha_ultimo_respaldo).toLocaleString()}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="estado-loading">
            {loading ? '⏳ Cargando estado...' : '❌ Error al cargar estado'}
          </div>
        )}
      </div>

      {/* Funciones de restauración */}
      <div className="restauracion-functions">
        {/* Card 1: Reiniciar BD */}
        <div className="function-card danger-card">
          <div className="card-header">
            <div className="card-icon danger-icon">🗑️</div>
            <div className="card-title-group">
              <h3>Reiniciar BD a Cero</h3>
              <span className="danger-badge">PELIGROSO</span>
            </div>
          </div>
          
          <div className="card-body">
            <p className="card-description">
              Elimina TODOS los datos de la base de datos manteniendo solo la estructura de tablas.
              Solo se conserva el usuario SuperAdmin.
            </p>
            
            <div className="warning-list">
              <h4>⚠️ Esta operación:</h4>
              <ul>
                <li>Elimina todos los empleados</li>
                <li>Elimina todas las empresas</li>
                <li>Elimina todos los datos de evaluaciones</li>
                <li>Conserva solo el SuperAdmin</li>
                <li>Reinicia las secuencias a 1</li>
                <li><strong>ES IRREVERSIBLE</strong></li>
              </ul>
            </div>
          </div>
          
          <div className="card-footer">
            <button 
              onClick={handleReiniciarBD}
              className="btn btn-danger"
              disabled={loading}
            >
              {loading ? '⏳ Procesando...' : '🗑️ Reiniciar BD'}
            </button>
          </div>
        </div>

        {/* Card 2: Cargar Datos Demo */}
        <div className="function-card safe-card">
          <div className="card-header">
            <div className="card-icon safe-icon">📊</div>
            <div className="card-title-group">
              <h3>Cargar Datos Demo</h3>
              <span className="safe-badge">SEGURO</span>
            </div>
          </div>
          
          <div className="card-body">
            <p className="card-description">
              Carga datos de demostración mínimos para probar el sistema.
              No elimina datos existentes.
            </p>
            
            <div className="demo-list">
              <h4>📋 Se creará:</h4>
              <ul>
                <li>🏢 1 empresa demo completa</li>
                <li>👥 3 usuarios de prueba (admin_empresa, admin_planta)</li>
                <li>🏭 1 planta con 3 departamentos</li>
                <li>💼 3 puestos esenciales</li>
                <li>💳 3 planes de suscripción</li>
                <li>👤 1 empleado de ejemplo</li>
              </ul>
            </div>
          </div>
          
          <div className="card-footer">
            <button 
              onClick={handleCargarDatosDemo}
              className="btn btn-success"
              disabled={loading}
            >
              {loading ? '⏳ Cargando...' : '📊 Cargar Datos Demo'}
            </button>
          </div>
        </div>
      </div>

      {/* Información adicional */}
      <div className="info-adicional">
        <div className="info-card">
          <h3>💡 Recomendaciones</h3>
          <ul>
            <li><strong>Antes de reiniciar:</strong> Crear respaldo completo</li>
            <li><strong>Para pruebas:</strong> Usar datos demo después de reiniciar</li>
            <li><strong>Para producción:</strong> Verificar respaldos antes de operaciones críticas</li>
            <li><strong>Usuarios disponibles después de demo:</strong> superadmin, admin_empresa, admin_planta</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RestauracionBD;
