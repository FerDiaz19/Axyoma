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
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingPlanta, setEditingPlanta] = useState<Planta | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
  });

  useEffect(() => {
    cargarPlantas();
  }, []);

  const cargarPlantas = async () => {
    try {
      setError(null);
      const response = await api.get('/plantas/');
      setPlantas(response.data);
    } catch (error) {
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

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de eliminar esta planta?')) {
      try {
        await api.delete(`/plantas/${id}/`);
        await cargarPlantas();
      } catch (error) {
        console.error('Error eliminando planta:', error);
        alert('Error al eliminar la planta');
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

      {/* Lista de plantas */}
      <div className="plantas-grid">
        {plantas.map((planta) => (
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
                onClick={() => handleDelete(planta.planta_id)}
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

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
                <button type="submit" className="btn btn-primary">
                  {editingPlanta ? 'Actualizar' : 'Guardar'}
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={resetForm}
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
