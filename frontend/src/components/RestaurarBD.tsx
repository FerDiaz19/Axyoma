import React, { useState, useRef } from 'react';
import adminBDService from '../services/adminBDService';
import './RespaldoBD.css';

interface RestaurarBDProps {
  className?: string;
}

const RestaurarBD: React.FC<RestaurarBDProps> = ({ className }) => {
  const [procesando, setProcesando] = useState(false);
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [archivoSeleccionado, setArchivoSeleccionado] = useState<File | null>(null);
  const [mostrarConfirmacion, setMostrarConfirmacion] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSeleccionarArchivo = (event: React.ChangeEvent<HTMLInputElement>) => {
    const archivo = event.target.files?.[0];
    if (archivo) {
      // Verificar que sea un archivo SQL
      if (!archivo.name.toLowerCase().endsWith('.sql')) {
        setMensaje('❌ Por favor seleccione un archivo SQL válido');
        setTimeout(() => setMensaje(null), 3000);
        return;
      }
      setArchivoSeleccionado(archivo);
      setMensaje(null);
    }
  };

  const handleIniciarRestauracion = () => {
    if (!archivoSeleccionado) {
      setMensaje('❌ Debe seleccionar un archivo SQL');
      setTimeout(() => setMensaje(null), 3000);
      return;
    }
    setMostrarConfirmacion(true);
  };

  const handleConfirmarRestauracion = async () => {
    if (!archivoSeleccionado) return;

    try {
      setProcesando(true);
      setMostrarConfirmacion(false);
      setMensaje('🔄 Restaurando base de datos... Esta operación puede tomar varios minutos.');
      
      const resultado = await adminBDService.restaurarBD(archivoSeleccionado);
      
      setMensaje('✅ Base de datos restaurada exitosamente');
      setArchivoSeleccionado(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      
      // Limpiar mensaje después de 7 segundos
      setTimeout(() => setMensaje(null), 7000);
      
    } catch (error: any) {
      console.error('Error al restaurar BD:', error);
      setMensaje(`❌ Error al restaurar: ${error.response?.data?.error || error.message || 'Error desconocido'}`);
      setTimeout(() => setMensaje(null), 10000);
    } finally {
      setProcesando(false);
    }
  };

  const handleCancelarConfirmacion = () => {
    setMostrarConfirmacion(false);
  };

  const formatearTamañoArchivo = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className={`restaurar-bd-card ${className || ''}`}>
      <div className="respaldo-header">
        <h3>🔄 Restaurar Base de Datos</h3>
        <p className="respaldo-descripcion">
          Restaurar la base de datos desde un archivo SQL de respaldo.
          <strong> Esta operación sobrescribirá los datos actuales.</strong>
        </p>
        <div className="advertencia-restauracion">
          ⚠️ <strong>ADVERTENCIA:</strong> Esta operación es irreversible y 
          reemplazará todos los datos actuales con los del archivo de respaldo.
        </div>
      </div>

      <div className="seleccion-archivo">
        <h4>📁 Seleccionar Archivo SQL</h4>
        <div className="archivo-input-container">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleSeleccionarArchivo}
            accept=".sql"
            disabled={procesando}
            className="archivo-input"
          />
          <div className="archivo-info">
            <small>Formatos aceptados: .sql</small>
          </div>
        </div>

        {archivoSeleccionado && (
          <div className="archivo-seleccionado">
            <h5>📄 Archivo Seleccionado</h5>
            <div className="archivo-detalles">
              <div className="detalle-item">
                <strong>Nombre:</strong> {archivoSeleccionado.name}
              </div>
              <div className="detalle-item">
                <strong>Tamaño:</strong> {formatearTamañoArchivo(archivoSeleccionado.size)}
              </div>
              <div className="detalle-item">
                <strong>Tipo:</strong> {archivoSeleccionado.type || 'application/sql'}
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="respaldo-actions">
        <button 
          onClick={handleIniciarRestauracion}
          disabled={procesando || !archivoSeleccionado}
          className={`respaldo-button danger ${procesando ? 'loading' : ''}`}
        >
          {procesando ? (
            <>
              <span className="spinner"></span>
              Restaurando...
            </>
          ) : (
            <>
              🔄 Restaurar Base de Datos
            </>
          )}
        </button>
      </div>

      {/* Modal de Confirmación */}
      {mostrarConfirmacion && (
        <div className="modal-overlay">
          <div className="modal-confirmacion">
            <div className="modal-header">
              <h3>⚠️ Confirmar Restauración</h3>
            </div>
            <div className="modal-body">
              <p>
                <strong>¿Está seguro que desea restaurar la base de datos?</strong>
              </p>
              <p>Esta operación:</p>
              <ul>
                <li>Sobrescribirá todos los datos actuales</li>
                <li>No se puede deshacer</li>
                <li>Puede tomar varios minutos</li>
                <li>Usuarios conectados pueden ser desconectados</li>
              </ul>
              
              {archivoSeleccionado && (
                <div className="archivo-confirmacion">
                  <strong>Archivo a restaurar:</strong> {archivoSeleccionado.name}
                </div>
              )}
            </div>
            <div className="modal-actions">
              <button 
                onClick={handleCancelarConfirmacion}
                className="respaldo-button secondary"
              >
                ❌ Cancelar
              </button>
              <button 
                onClick={handleConfirmarRestauracion}
                className="respaldo-button danger"
              >
                ✅ Confirmar Restauración
              </button>
            </div>
          </div>
        </div>
      )}

      {mensaje && (
        <div className={`respaldo-mensaje ${mensaje.includes('❌') ? 'error' : mensaje.includes('⚠️') ? 'warning' : 'success'}`}>
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default RestaurarBD;
