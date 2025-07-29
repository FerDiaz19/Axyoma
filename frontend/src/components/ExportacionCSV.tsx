import React, { useState } from 'react';
import adminBDService from '../services/adminBDService';

interface ExportacionCSVProps {
  tablaNombre: string;
  descripcion: string;
  className?: string;
}

const ExportacionCSV: React.FC<ExportacionCSVProps> = ({ 
  tablaNombre, 
  descripcion, 
  className = '' 
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
    <div className={`exportacion-csv-container ${className}`}>
      <div className="exportacion-info">
        <h4>{descripcion}</h4>
        <p>Tabla: {tablaNombre}</p>
      </div>
      
      <button 
        onClick={handleExportar}
        disabled={descargando}
        className={`export-btn ${descargando ? 'loading' : ''}`}
        title={`Exportar ${tablaNombre} a CSV`}
      >
        {descargando ? (
          <>
            <span className="btn-spinner">⏳</span>
            <span className="btn-text">Exportando...</span>
          </>
        ) : (
          <>
            <span className="btn-icon">📤</span>
            <span className="btn-text">Exportar CSV</span>
          </>
        )}
      </button>
      
      {mensaje && (
        <div className={`mensaje ${mensaje.startsWith('✅') ? 'success' : 'error'}`}>
          {mensaje}
        </div>
      )}
    </div>
  );
};

export default ExportacionCSV;
