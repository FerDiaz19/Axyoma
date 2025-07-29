import React, { useState } from 'react';
import adminBDService from '../services/adminBDService';
import './RespaldoBD.css';

interface RespaldoCompletoProps {
  className?: string;
}

const RespaldoCompleto: React.FC<RespaldoCompletoProps> = ({ className }) => {
  const [procesando, setProcesando] = useState(false);
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [ultimoRespaldo, setUltimoRespaldo] = useState<any>(null);

  const handleCrearRespaldo = async () => {
    try {
      setProcesando(true);
      setMensaje(null);
      
      const resultado = await adminBDService.crearRespaldoCompleto();
      
      setUltimoRespaldo(resultado);
      setMensaje('✅ Respaldo completo creado exitosamente');
      
      // Limpiar mensaje después de 5 segundos
      setTimeout(() => setMensaje(null), 5000);
      
    } catch (error: any) {
      console.error('Error al crear respaldo:', error);
      setMensaje(`❌ Error: ${error.response?.data?.error || error.message || 'Error desconocido'}`);
      
      // Limpiar mensaje de error después de 7 segundos
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

  return (
    <div className={`respaldo-completo-card ${className || ''}`}>
      <div className="respaldo-header">
        <h3>🗄️ Respaldo Completo de Base de Datos</h3>
        <p className="respaldo-descripcion">
          Crear un respaldo completo de toda la base de datos en formato SQL.
          Solo disponible para SuperAdmin.
        </p>
      </div>
      
      <div className="respaldo-actions">
        <button 
          onClick={handleCrearRespaldo}
          disabled={procesando}
          className={`respaldo-button primary ${procesando ? 'loading' : ''}`}
        >
          {procesando ? (
            <>
              <span className="spinner"></span>
              Creando respaldo...
            </>
          ) : (
            <>
              📦 Crear Respaldo Completo
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
              <strong>Tipo:</strong> Respaldo Completo (SQL)
            </div>
          </div>
        </div>
      )}

      {mensaje && (
        <div className={`respaldo-mensaje ${mensaje.includes('❌') ? 'error' : 'success'}`}>
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default RespaldoCompleto;
