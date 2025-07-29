import React, { useState } from 'react';
import adminBDService from '../services/adminBDService';
import './ExportacionCSV.css';

interface ExportacionCSVProps {
  tablaNombre: string;
  descripcion: string;
  className?: string;
}

const ExportacionCSV: React.FC<ExportacionCSVProps> = ({ 
  tablaNombre, 
  descripcion, 
  className 
}) => {
  const [descargando, setDescargando] = useState(false);
  const [mensaje, setMensaje] = useState<string | null>(null);

  const handleExportar = async () => {
    try {
      setDescargando(true);
      setMensaje(null);
      
      const blob = await adminBDService.exportarTabla(tablaNombre);
      
      // Crear nombre del archivo con timestamp
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[T:]/g, '_');
      const nombreArchivo = `${tablaNombre}_${timestamp}.csv`;
      
      // Descargar archivo
      adminBDService.descargarArchivo(blob, nombreArchivo);
      
      setMensaje('✅ Exportación completada exitosamente');
      
      // Limpiar mensaje después de 3 segundos
      setTimeout(() => setMensaje(null), 3000);
      
    } catch (error: any) {
      console.error('Error al exportar:', error);
      setMensaje(`❌ Error: ${error.response?.data?.error || error.message || 'Error desconocido'}`);
      
      // Limpiar mensaje de error después de 5 segundos
      setTimeout(() => setMensaje(null), 5000);
    } finally {
      setDescargando(false);
    }
  };

  return (
    <div className={`exportacion-csv-card ${className || ''}`}>
      <div className="exportacion-header">
        <h4>📄 {descripcion}</h4>
        <p className="exportacion-tabla-nombre">Tabla: {tablaNombre}</p>
      </div>
      
      <div className="exportacion-actions">
        <button 
          onClick={handleExportar}
          disabled={descargando}
          className={`exportacion-button ${descargando ? 'loading' : ''}`}
        >
          {descargando ? (
            <>
              <span className="spinner"></span>
              Exportando...
            </>
          ) : (
            <>
              📤 Exportar CSV
            </>
          )}
        </button>
      </div>
      
      {mensaje && (
        <div className={`exportacion-mensaje ${mensaje.startsWith('✅') ? 'success' : 'error'}`}>
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default ExportacionCSV;
