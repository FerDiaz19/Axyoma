import React, { useState } from 'react';
import ExportacionCSV from './ExportacionCSV';
import RespaldoCompleto from './RespaldoCompleto';
import RespaldoParcial from './RespaldoParcial';
import RestaurarBD from './RestaurarBD';
import './GestionBD.css';

interface GestionBDProps {
  className?: string;
}

const GestionBD: React.FC<GestionBDProps> = ({ className }) => {
  const [pestañaActiva, setPestañaActiva] = useState<string>('exportaciones');

  const pestañas = [
    { id: 'exportaciones', nombre: 'Exportaciones CSV', icono: '📄' },
    { id: 'respaldo-completo', nombre: 'Respaldo Completo', icono: '🗄️' },
    { id: 'respaldo-parcial', nombre: 'Respaldo Parcial', icono: '📋' },
    { id: 'restaurar', nombre: 'Restaurar BD', icono: '🔄' },
  ];

  const tablasExportables = [
    { nombre: 'empresas', descripcion: 'Empresas registradas' },
    { nombre: 'empleados', descripcion: 'Empleados del sistema' },
    { nombre: 'plantas', descripcion: 'Plantas industriales' },
    { nombre: 'departamentos', descripcion: 'Departamentos organizacionales' },
    { nombre: 'puestos', descripcion: 'Puestos de trabajo' },
    { nombre: 'suscripciones', descripcion: 'Suscripciones activas' },
  ];

  const renderContenido = () => {
    switch (pestañaActiva) {
      case 'exportaciones':
        return (
          <div className="exportaciones-grid">
            <div className="exportaciones-header">
              <h3>📄 Exportaciones CSV</h3>
              <p>Exportar datos de tablas específicas en formato CSV</p>
            </div>
            
            <div className="exportaciones-lista">
              {tablasExportables.map((tabla) => (
                <ExportacionCSV
                  key={tabla.nombre}
                  tablaNombre={tabla.nombre}
                  descripcion={tabla.descripcion}
                  className="exportacion-item"
                />
              ))}
            </div>
          </div>
        );

      case 'respaldo-completo':
        return <RespaldoCompleto />;

      case 'respaldo-parcial':
        return <RespaldoParcial />;

      case 'restaurar':
        return <RestaurarBD />;

      default:
        return <div>Sección no encontrada</div>;
    }
  };

  return (
    <div className={`gestion-bd-container ${className || ''}`}>
      <div className="gestion-bd-header">
        <h2>🛠️ Gestión de Base de Datos</h2>
        <p className="gestion-bd-descripcion">
          Herramientas para administrar, respaldar y restaurar la base de datos del sistema.
        </p>
      </div>

      <div className="gestion-bd-tabs">
        <div className="tabs-header">
          {pestañas.map((pestaña) => (
            <button
              key={pestaña.id}
              onClick={() => setPestañaActiva(pestaña.id)}
              className={`tab-button ${pestañaActiva === pestaña.id ? 'active' : ''}`}
            >
              <span className="tab-icon">{pestaña.icono}</span>
              <span className="tab-text">{pestaña.nombre}</span>
            </button>
          ))}
        </div>

        <div className="tabs-content">
          {renderContenido()}
        </div>
      </div>
    </div>
  );
};

export default GestionBD;