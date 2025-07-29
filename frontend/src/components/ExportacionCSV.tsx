import React, { useState } from 'react';
import { exportarTabla } from '../services/adminBDService';

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
  const [exportando, setExportando] = useState(false);

  const handleExportar = async () => {
    setExportando(true);
    try {
      await exportarTabla(tablaNombre);
      // Mostrar notificación de éxito más sutil
      const notification = document.createElement('div');
      notification.className = 'export-success-notification';
      notification.innerHTML = `
        <div class="notification-content">
          <span class="notification-icon">✅</span>
          <span class="notification-text">Tabla ${tablaNombre} exportada exitosamente</span>
        </div>
      `;
      document.body.appendChild(notification);
      
      // Remover notificación después de 3 segundos
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification);
        }
      }, 3000);
    } catch (error) {
      console.error('Error al exportar:', error);
      // Mostrar notificación de error
      const notification = document.createElement('div');
      notification.className = 'export-error-notification';
      notification.innerHTML = `
        <div class="notification-content">
          <span class="notification-icon">❌</span>
          <span class="notification-text">Error al exportar tabla ${tablaNombre}</span>
        </div>
      `;
      document.body.appendChild(notification);
      
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification);
        }
      }, 3000);
    } finally {
      setExportando(false);
    }
  };

  return (
    <button 
      onClick={handleExportar}
      disabled={exportando}
      className={`export-btn ${className} ${exportando ? 'exporting' : ''}`}
      title={`Exportar ${tablaNombre} a CSV`}
    >
      {exportando ? (
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
  );
};

export default ExportacionCSV;
