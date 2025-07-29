import React, { useState, useEffect } from 'react';
import adminBDService from '../services/adminBDService';
import './RespaldoBD.css';

interface TablaSelectable {
  nombre: string;
  descripcion: string;
  seleccionada: boolean;
}

interface RespaldoParcialProps {
  className?: string;
}

const RespaldoParcial: React.FC<RespaldoParcialProps> = ({ className }) => {
  const [procesando, setProcesando] = useState(false);
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [tablas, setTablas] = useState<TablaSelectable[]>([]);
  const [ultimoRespaldo, setUltimoRespaldo] = useState<any>(null);
  const [cargandoTablas, setCargandoTablas] = useState(false);

  useEffect(() => {
    cargarTablasDisponibles();
  }, []);

  const cargarTablasDisponibles = async () => {
    try {
      setCargandoTablas(true);
      const datos = await adminBDService.listarTablasExportables();
      const tablasConSeleccion = datos.tablas_disponibles.map((tabla: any) => ({
        nombre: tabla.nombre,
        descripcion: tabla.descripcion,
        seleccionada: false
      }));
      setTablas(tablasConSeleccion);
    } catch (error) {
      console.error('Error al cargar tablas:', error);
      setMensaje('❌ Error al cargar tablas disponibles');
    } finally {
      setCargandoTablas(false);
    }
  };

  const toggleTabla = (nombreTabla: string) => {
    setTablas(tablas.map(tabla => 
      tabla.nombre === nombreTabla 
        ? { ...tabla, seleccionada: !tabla.seleccionada }
        : tabla
    ));
  };

  const seleccionarTodas = () => {
    const todasSeleccionadas = tablas.every(tabla => tabla.seleccionada);
    setTablas(tablas.map(tabla => ({ 
      ...tabla, 
      seleccionada: !todasSeleccionadas 
    })));
  };

  const handleCrearRespaldo = async () => {
    const tablasSeleccionadas = tablas.filter(tabla => tabla.seleccionada);
    
    if (tablasSeleccionadas.length === 0) {
      setMensaje('❌ Debe seleccionar al menos una tabla');
      setTimeout(() => setMensaje(null), 3000);
      return;
    }

    try {
      setProcesando(true);
      setMensaje(null);
      
      const nombresTablas = tablasSeleccionadas.map(tabla => tabla.nombre);
      const resultado = await adminBDService.crearRespaldoParcial(nombresTablas);
      
      setUltimoRespaldo(resultado);
      setMensaje(`✅ Respaldo parcial creado con ${nombresTablas.length} tablas`);
      
      // Limpiar mensaje después de 5 segundos
      setTimeout(() => setMensaje(null), 5000);
      
    } catch (error: any) {
      console.error('Error al crear respaldo:', error);
      setMensaje(`❌ Error: ${error.response?.data?.error || error.message || 'Error desconocido'}`);
      setTimeout(() => setMensaje(null), 7000);
    } finally {
      setProcesando(false);
    }
  };

  const handleDescargarRespaldo = async () => {
    if (!ultimoRespaldo?.archivo) return;
    
    try {
      setProcesando(true);
      const blob = await adminBDService.descargarRespaldo(ultimoRespaldo.archivo);
      adminBDService.descargarArchivo(blob, ultimoRespaldo.archivo);
      setMensaje('✅ Descarga iniciada');
      setTimeout(() => setMensaje(null), 3000);
    } catch (error: any) {
      setMensaje(`❌ Error al descargar: ${error.response?.data?.error || error.message}`);
      setTimeout(() => setMensaje(null), 5000);
    } finally {
      setProcesando(false);
    }
  };

  const formatearTamaño = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const tablasSeleccionadas = tablas.filter(tabla => tabla.seleccionada);

  return (
    <div className={`respaldo-parcial-card ${className || ''}`}>
      <div className="respaldo-header">
        <h3>📋 Respaldo Parcial de Tablas</h3>
        <p className="respaldo-descripcion">
          Selecciona las tablas específicas para crear un respaldo parcial en formato SQL.
        </p>
      </div>

      {cargandoTablas ? (
        <div className="loading-container">
          <span className="spinner"></span>
          Cargando tablas disponibles...
        </div>
      ) : (
        <>
          <div className="seleccion-tablas">
            <div className="seleccion-header">
              <h4>🔧 Seleccionar Tablas</h4>
              <button 
                onClick={seleccionarTodas}
                className="btn-toggle-all"
                disabled={procesando}
              >
                {tablas.every(tabla => tabla.seleccionada) ? 'Deseleccionar Todas' : 'Seleccionar Todas'}
              </button>
            </div>
            
            <div className="tablas-grid">
              {tablas.map((tabla) => (
                <div 
                  key={tabla.nombre} 
                  className={`tabla-item ${tabla.seleccionada ? 'seleccionada' : ''}`}
                  onClick={() => toggleTabla(tabla.nombre)}
                >
                  <div className="tabla-checkbox">
                    <input 
                      type="checkbox" 
                      checked={tabla.seleccionada}
                      onChange={() => toggleTabla(tabla.nombre)}
                    />
                  </div>
                  <div className="tabla-info">
                    <h5>{tabla.nombre}</h5>
                    <p>{tabla.descripcion}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="respaldo-actions">
            <div className="resumen-seleccion">
              <strong>Tablas seleccionadas: {tablasSeleccionadas.length}</strong>
              {tablasSeleccionadas.length > 0 && (
                <div className="tabla-nombres">
                  {tablasSeleccionadas.map(tabla => tabla.nombre).join(', ')}
                </div>
              )}
            </div>
            
            <button 
              onClick={handleCrearRespaldo}
              disabled={procesando || tablasSeleccionadas.length === 0}
              className={`respaldo-button primary ${procesando ? 'loading' : ''}`}
            >
              {procesando ? (
                <>
                  <span className="spinner"></span>
                  Creando respaldo...
                </>
              ) : (
                <>
                  📦 Crear Respaldo Parcial
                </>
              )}
            </button>
            
            {ultimoRespaldo && (
              <button 
                onClick={handleDescargarRespaldo}
                disabled={procesando}
                className="respaldo-button secondary"
              >
                💾 Descargar Último Respaldo
              </button>
            )}
          </div>

          {ultimoRespaldo && (
            <div className="respaldo-info">
              <h4>📋 Último Respaldo Creado</h4>
              <div className="respaldo-detalles">
                <div className="detalle-item">
                  <strong>Archivo:</strong> {ultimoRespaldo.archivo}
                </div>
                <div className="detalle-item">
                  <strong>Tamaño:</strong> {formatearTamaño(ultimoRespaldo.tamaño)}
                </div>
                <div className="detalle-item">
                  <strong>Tablas incluidas:</strong> {ultimoRespaldo.tablas?.join(', ')}
                </div>
                <div className="detalle-item">
                  <strong>Tipo:</strong> Respaldo Parcial (SQL)
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {mensaje && (
        <div className={`respaldo-mensaje ${mensaje.includes('❌') ? 'error' : 'success'}`}>
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default RespaldoParcial;
