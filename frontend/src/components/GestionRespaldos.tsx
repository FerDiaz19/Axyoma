import React, { useState, useEffect } from 'react';
import respaldosService, { RespaldoMetadata, InfoSistemaRespaldos } from '../services/respaldosService';

interface GestionRespaldosProps {
  className?: string;
}

const GestionRespaldos: React.FC<GestionRespaldosProps> = ({ className = '' }) => {
  const [respaldos, setRespaldos] = useState<RespaldoMetadata[]>([]);
  const [infoSistema, setInfoSistema] = useState<InfoSistemaRespaldos | null>(null);
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [vistaActual, setVistaActual] = useState<'lista' | 'crear' | 'info'>('lista');

  // Estados para crear respaldos
  const [tipoRespaldo, setTipoRespaldo] = useState<'tablas' | 'completo'>('tablas');
  const [tablasSeleccionadas, setTablasSeleccionadas] = useState<string[]>([]);
  const [incluirDatos, setIncluirDatos] = useState(true);
  const [descripcion, setDescripcion] = useState('');

  const tablasDisponibles = respaldosService.getTablasDisponibles();

  useEffect(() => {
    const cargarDatosIniciales = async () => {
      try {
        setLoading(true);
        const [respaldosData, infoData] = await Promise.all([
          respaldosService.listarRespaldos(),
          respaldosService.obtenerInfoSistema()
        ]);
        setRespaldos(respaldosData);
        setInfoSistema(infoData);
      } catch (error: any) {
        mostrarMensaje(`❌ Error: ${error.message}`, 'error');
      } finally {
        setLoading(false);
      }
    };

    cargarDatosIniciales();
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const [respaldosData, infoData] = await Promise.all([
        respaldosService.listarRespaldos(),
        respaldosService.obtenerInfoSistema()
      ]);
      setRespaldos(respaldosData);
      setInfoSistema(infoData);
    } catch (error: any) {
      mostrarMensaje(`❌ Error: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const mostrarMensaje = (texto: string, tipo: 'success' | 'error' = 'success') => {
    setMensaje(texto);
    setTimeout(() => setMensaje(null), 5000);
  };

  const handleCrearRespaldo = async () => {
    try {
      setLoading(true);
      
      if (tipoRespaldo === 'tablas') {
        if (tablasSeleccionadas.length === 0) {
          mostrarMensaje('❌ Debe seleccionar al menos una tabla', 'error');
          return;
        }
        
        const resultado = await respaldosService.crearRespaldoTablas({
          tablas: tablasSeleccionadas,
          incluir_datos: incluirDatos,
          descripcion: descripcion
        });
        
        mostrarMensaje(`✅ Respaldo de tablas creado: ${resultado.archivo}`);
      } else {
        const resultado = await respaldosService.crearRespaldoCompleto({
          incluir_datos: incluirDatos,
          descripcion: descripcion
        });
        
        mostrarMensaje(`✅ Respaldo completo creado: ${resultado.archivo}`);
      }
      
      // Limpiar formulario y recargar datos
      setTablasSeleccionadas([]);
      setDescripcion('');
      setVistaActual('lista');
      await cargarDatos();
      
    } catch (error: any) {
      mostrarMensaje(`❌ Error: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDescargar = async (archivo: string) => {
    try {
      await respaldosService.descargarRespaldo(archivo);
      mostrarMensaje(`✅ Descargando: ${archivo}`);
    } catch (error: any) {
      mostrarMensaje(`❌ Error al descargar: ${error.message}`, 'error');
    }
  };

  const handleEliminar = async (archivo: string) => {
    if (!window.confirm(`¿Está seguro de eliminar el respaldo ${archivo}?`)) {
      return;
    }
    
    try {
      await respaldosService.eliminarRespaldo(archivo);
      mostrarMensaje(`✅ Respaldo eliminado: ${archivo}`);
      await cargarDatos();
    } catch (error: any) {
      mostrarMensaje(`❌ Error al eliminar: ${error.message}`, 'error');
    }
  };

  const handleRestaurar = async (archivo: string) => {
    const confirmacion = window.prompt(
      `⚠️ ADVERTENCIA: La restauración puede sobrescribir datos existentes.\n\n` +
      `Para confirmar, escriba exactamente: CONFIRMAR RESTAURACION`
    );
    
    if (confirmacion !== 'CONFIRMAR RESTAURACION') {
      mostrarMensaje('❌ Restauración cancelada', 'error');
      return;
    }
    
    try {
      setLoading(true);
      const resultado = await respaldosService.restaurarRespaldo({
        archivo: archivo,
        confirmar: true,
        modo: 'replace'
      });
      
      mostrarMensaje(`✅ Restauración completada desde: ${archivo}`);
      console.log('Resultado de restauración:', resultado);
      
    } catch (error: any) {
      mostrarMensaje(`❌ Error en restauración: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTabla = (tabla: string) => {
    setTablasSeleccionadas(prev => 
      prev.includes(tabla) 
        ? prev.filter(t => t !== tabla)
        : [...prev, tabla]
    );
  };

  const renderVistaLista = () => (
    <div className="respaldos-lista">
      <div className="respaldos-header">
        <h3>📦 Respaldos Disponibles ({respaldos.length})</h3>
        <div className="respaldos-acciones">
          <button 
            onClick={() => setVistaActual('crear')}
            className="btn btn-primary"
            disabled={loading}
          >
            ➕ Crear Respaldo
          </button>
          <button 
            onClick={() => setVistaActual('info')}
            className="btn btn-secondary"
          >
            ℹ️ Info Sistema
          </button>
          <button 
            onClick={cargarDatos}
            className="btn btn-secondary"
            disabled={loading}
          >
            🔄 Actualizar
          </button>
        </div>
      </div>

      {respaldos.length === 0 ? (
        <div className="respaldos-vacio">
          <p>📭 No hay respaldos disponibles</p>
          <button 
            onClick={() => setVistaActual('crear')}
            className="btn btn-primary"
          >
            Crear primer respaldo
          </button>
        </div>
      ) : (
        <div className="respaldos-grid">
          {respaldos.map((respaldo, index) => (
            <div key={index} className="respaldo-card">
              <div className="respaldo-header">
                <h4>📄 {respaldo.archivo}</h4>
                <span className={`respaldo-tipo ${respaldo.tipo}`}>
                  {respaldo.tipo === 'bd_completa' ? '🗄️ BD Completa' : '📊 Tablas'}
                </span>
              </div>
              
              <div className="respaldo-info">
                <p><strong>📅 Fecha:</strong> {respaldosService.formatearFecha(respaldo.fecha_creacion)}</p>
                <p><strong>💾 Tamaño:</strong> {respaldosService.formatearTamaño(respaldo.tamaño_bytes)}</p>
                <p><strong>👤 Usuario:</strong> {respaldo.usuario}</p>
                <p><strong>📊 Datos:</strong> {respaldo.incluir_datos ? 'Incluidos' : 'Solo estructura'}</p>
                
                {respaldo.descripcion && (
                  <p><strong>📝 Descripción:</strong> {respaldo.descripcion}</p>
                )}
                
                {respaldo.tablas && (
                  <p><strong>🏷️ Tablas:</strong> {respaldo.tablas.join(', ')}</p>
                )}
              </div>
              
              <div className="respaldo-acciones">
                <button 
                  onClick={() => handleDescargar(respaldo.archivo)}
                  className="btn btn-sm btn-secondary"
                  title="Descargar respaldo"
                >
                  ⬇️ Descargar
                </button>
                <button 
                  onClick={() => handleRestaurar(respaldo.archivo)}
                  className="btn btn-sm btn-warning"
                  title="Restaurar respaldo"
                  disabled={loading}
                >
                  🔄 Restaurar
                </button>
                <button 
                  onClick={() => handleEliminar(respaldo.archivo)}
                  className="btn btn-sm btn-danger"
                  title="Eliminar respaldo"
                >
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  const renderVistaCrear = () => (
    <div className="crear-respaldo">
      <div className="crear-header">
        <h3>➕ Crear Nuevo Respaldo</h3>
        <button 
          onClick={() => setVistaActual('lista')}
          className="btn btn-secondary"
        >
          ← Volver
        </button>
      </div>

      <div className="crear-form">
        <div className="form-group">
          <label>📊 Tipo de Respaldo:</label>
          <div className="radio-group">
            <label>
              <input 
                type="radio" 
                value="tablas"
                checked={tipoRespaldo === 'tablas'}
                onChange={(e) => setTipoRespaldo(e.target.value as 'tablas')}
              />
              📋 Tablas Específicas
            </label>
            <label>
              <input 
                type="radio" 
                value="completo"
                checked={tipoRespaldo === 'completo'}
                onChange={(e) => setTipoRespaldo(e.target.value as 'completo')}
              />
              🗄️ Base de Datos Completa
            </label>
          </div>
        </div>

        {tipoRespaldo === 'tablas' && (
          <div className="form-group">
            <label>🏷️ Seleccionar Tablas:</label>
            <div className="tablas-grid">
              {tablasDisponibles.map(tabla => (
                <label key={tabla} className="tabla-checkbox">
                  <input 
                    type="checkbox"
                    checked={tablasSeleccionadas.includes(tabla)}
                    onChange={() => handleToggleTabla(tabla)}
                  />
                  {tabla}
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="form-group">
          <label>
            <input 
              type="checkbox"
              checked={incluirDatos}
              onChange={(e) => setIncluirDatos(e.target.checked)}
            />
            💾 Incluir datos (no solo estructura)
          </label>
        </div>

        <div className="form-group">
          <label>📝 Descripción (opcional):</label>
          <textarea 
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            placeholder="Describe el propósito de este respaldo..."
            rows={3}
          />
        </div>

        <div className="form-actions">
          <button 
            onClick={handleCrearRespaldo}
            className="btn btn-primary"
            disabled={loading || (tipoRespaldo === 'tablas' && tablasSeleccionadas.length === 0)}
          >
            {loading ? '⏳ Creando...' : '💾 Crear Respaldo'}
          </button>
        </div>
      </div>
    </div>
  );

  const renderVistaInfo = () => (
    <div className="sistema-info">
      <div className="info-header">
        <h3>ℹ️ Información del Sistema</h3>
        <button 
          onClick={() => setVistaActual('lista')}
          className="btn btn-secondary"
        >
          ← Volver
        </button>
      </div>

      {infoSistema && (
        <div className="info-content">
          <div className="info-section">
            <h4>🗄️ Base de Datos</h4>
            <p><strong>Nombre:</strong> {infoSistema.base_datos}</p>
            <p><strong>Servidor:</strong> {infoSistema.host}:{infoSistema.puerto}</p>
          </div>

          <div className="info-section">
            <h4>📁 Respaldos</h4>
            <p><strong>Directorio:</strong> {infoSistema.directorio_respaldos}</p>
            <p><strong>Cantidad:</strong> {infoSistema.cantidad_respaldos}</p>
            <p><strong>Espacio usado:</strong> {infoSistema.espacio_usado_mb} MB</p>
          </div>

          <div className="info-section">
            <h4>🔧 Herramientas</h4>
            <p><strong>pg_dump:</strong> {infoSistema.herramientas_disponibles.pg_dump ? '✅ Disponible' : '❌ No disponible'}</p>
            <p><strong>psql:</strong> {infoSistema.herramientas_disponibles.psql ? '✅ Disponible' : '❌ No disponible'}</p>
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className={`gestion-respaldos ${className}`}>
      <div className="respaldos-container">
        <h2>🛠️ Gestión de Respaldos y Restauración</h2>
        
        {mensaje && (
          <div className={`mensaje ${mensaje.startsWith('✅') ? 'success' : 'error'}`}>
            {mensaje}
          </div>
        )}

        {loading && (
          <div className="loading-overlay">
            <div className="loading-spinner">⏳ Procesando...</div>
          </div>
        )}

        {vistaActual === 'lista' && renderVistaLista()}
        {vistaActual === 'crear' && renderVistaCrear()}
        {vistaActual === 'info' && renderVistaInfo()}
      </div>
    </div>
  );
};

export default GestionRespaldos;
