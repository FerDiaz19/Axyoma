import React, { useState, useEffect } from 'react';
import api from '../api';

interface Planta {
  planta_id: number;
  nombre: string;
  direccion: string;
  fecha_registro: string;
  status: boolean;
  empresa_id: number;
  empresa_nombre: string;
}

interface GestionPlantasProps {
  empresaId: number;
}

const GestionPlantas: React.FC<GestionPlantasProps> = ({ empresaId }) => {
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [plantasFiltradas, setPlantasFiltradas] = useState<Planta[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingPlanta, setEditingPlanta] = useState<Planta | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filtroNombre, setFiltroNombre] = useState('');
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
  });

  useEffect(() => {
    cargarPlantas();
  }, []);

  useEffect(() => {
    // Aplicar filtros
    let plantasFiltradas = plantas;
    
    if (filtroNombre.trim()) {
      plantasFiltradas = plantasFiltradas.filter(planta =>
        planta.nombre.toLowerCase().includes(filtroNombre.toLowerCase()) ||
        planta.direccion.toLowerCase().includes(filtroNombre.toLowerCase())
      );
    }
    
    setPlantasFiltradas(plantasFiltradas);
  }, [plantas, filtroNombre]);

  const cargarPlantas = async () => {
    try {
      setError(null);
      const response = await api.get('/plantas/');
      setPlantas(response.data);
    } catch (error: any) {
      console.error('Error cargando plantas:', error);
      setError('Error al cargar las plantas');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    
    try {
      if (editingPlanta) {
        // Actualizar planta existente
        await api.put(`/plantas/${editingPlanta.planta_id}/`, formData);
      } else {
        // Crear nueva planta
        await api.post('/plantas/', formData);
      }
      
      // Recargar lista y resetear formulario
      await cargarPlantas();
      resetForm();
    } catch (error: any) {
      console.error('Error guardando planta:', error);
      setError(error.response?.data?.detail || 'Error al guardar la planta');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (planta: Planta) => {
    setEditingPlanta(planta);
    setFormData({
      nombre: planta.nombre,
      direccion: planta.direccion,
    });
    setShowForm(true);
  };

  const handleDelete = async (planta: Planta) => {
    const confirmMessage = `¿Está seguro de eliminar la planta "${planta.nombre}"?\n\nEsta acción también eliminará todos los departamentos, puestos y empleados asociados a esta planta.\n\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        setError(null);
        await api.delete(`/plantas/${planta.planta_id}/`);
        await cargarPlantas();
        alert('Planta eliminada exitosamente');
      } catch (error: any) {
        console.error('Error eliminando planta:', error);
        const errorMessage = error.response?.data?.detail || error.response?.data?.message || 'Error al eliminar la planta';
        setError(errorMessage);
        alert(`Error al eliminar la planta: ${errorMessage}`);
      }
    }
  };

  const resetForm = () => {
    setFormData({ nombre: '', direccion: '' });
    setEditingPlanta(null);
    setShowForm(false);
  };

  if (loading) {
    return <div className="loading">Cargando plantas...</div>;
  }

  return (
    <div className="gestion-plantas">
      <div className="header">
        <h2>Gestión de Plantas</h2>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(true)}
        >
          + Agregar Planta
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Filtros */}
      <div className="filtros">
        <div className="filtro-group">
          <label>Buscar por nombre o dirección:</label>
          <input
            type="text"
            placeholder="Escriba para filtrar..."
            value={filtroNombre}
            onChange={(e) => setFiltroNombre(e.target.value)}
            className="filtro-input"
          />
        </div>
        {filtroNombre && (
          <div className="filtro-info">
            Mostrando {plantasFiltradas.length} de {plantas.length} plantas
          </div>
        )}
      </div>

      {/* Lista de plantas */}
      <div className="plantas-grid">
        {plantasFiltradas.map((planta) => (
          <div key={planta.planta_id} className="planta-card">
            <h3>{planta.nombre}</h3>
            <p className="direccion">{planta.direccion}</p>
            <p className="fecha">
              Registrada: {new Date(planta.fecha_registro).toLocaleDateString()}
            </p>
            <div className="actions">
              <button 
                className="btn btn-secondary"
                onClick={() => handleEdit(planta)}
              >
                Editar
              </button>
              <button 
                className="btn btn-danger"
                onClick={() => handleDelete(planta)}
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {plantasFiltradas.length === 0 && plantas.length > 0 && (
        <div className="no-results">
          <p>No se encontraron plantas que coincidan con "{filtroNombre}"</p>
        </div>
      )}

      {plantas.length === 0 && (
        <div className="empty-state">
          <p>No hay plantas registradas</p>
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            Agregar Primera Planta
          </button>
        </div>
      )}

      {/* Modal/Formulario */}
      {showForm && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>{editingPlanta ? 'Editar Planta' : 'Nueva Planta'}</h3>
            <form onSubmit={handleSubmit}>
              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}
              
              <div className="form-group">
                <label>Nombre de la Planta:</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Dirección:</label>
                <textarea
                  value={formData.direccion}
                  onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                  required
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? 'Guardando...' : (editingPlanta ? 'Actualizar' : 'Guardar')}
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={resetForm}
                  disabled={saving}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionPlantas;
