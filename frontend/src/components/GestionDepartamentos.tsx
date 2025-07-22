import React, { useState, useEffect } from 'react';
import { obtenerDepartamentos, crearDepartamento, actualizarDepartamento, eliminarDepartamento, obtenerPlantas, Departamento, Planta } from '../services/organizacionService';
import '../css/GestionDepartamentos.css';

const GestionDepartamentos: React.FC = () => {
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingDepartamento, setEditingDepartamento] = useState<Departamento | null>(null);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    planta_id: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [departamentosData, plantasData] = await Promise.all([
        obtenerDepartamentos(),
        obtenerPlantas()
      ]);
      setDepartamentos(departamentosData);
      setPlantas(plantasData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingDepartamento) {
        await actualizarDepartamento(editingDepartamento.departamento_id!, {
          nombre: formData.nombre,
          descripcion: formData.descripcion,
          planta_id: parseInt(formData.planta_id)
        });
      } else {
        await crearDepartamento({
          nombre: formData.nombre,
          descripcion: formData.descripcion,
          planta_id: parseInt(formData.planta_id)
        });
      }
      setShowModal(false);
      setFormData({ nombre: '', descripcion: '', planta_id: '' });
      setEditingDepartamento(null);
      loadData();
    } catch (error) {
      console.error('Error saving departamento:', error);
    }
  };

  const handleEdit = (departamento: Departamento) => {
    setEditingDepartamento(departamento);
    setFormData({
      nombre: departamento.nombre,
      descripcion: departamento.descripcion || '',
      planta_id: departamento.planta_id?.toString() || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de eliminar este departamento?')) {
      try {
        await eliminarDepartamento(id);
        loadData();
      } catch (error) {
        console.error('Error deleting departamento:', error);
      }
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setFormData({ nombre: '', descripcion: '', planta_id: '' });
    setEditingDepartamento(null);
  };

  if (loading) {
    return <div className="loading">Cargando departamentos...</div>;
  }

  return (
    <div className="gestion-departamentos">
      <div className="header-section">
        <h2>🏢 Gestión de Departamentos</h2>
        <button className="btn-primary" onClick={() => setShowModal(true)}>
          + Nuevo Departamento
        </button>
      </div>

      <div className="departamentos-grid">
        {departamentos.map(departamento => (
          <div key={departamento.departamento_id} className="departamento-card">
            <div className="card-header">
              <h3>{departamento.nombre}</h3>
              <div className="card-actions">
                <button 
                  className="btn-edit"
                  onClick={() => handleEdit(departamento)}
                >
                  ✏️
                </button>
                <button 
                  className="btn-delete"
                  onClick={() => handleDelete(departamento.departamento_id!)}
                >
                  🗑️
                </button>
              </div>
            </div>
            <div className="card-body">
              <p className="description">{departamento.descripcion}</p>
              <p className="planta-info">
                <strong>Planta:</strong> {departamento.planta_nombre}
              </p>
              <span className={`status ${departamento.status ? 'active' : 'inactive'}`}>
                {departamento.status ? 'Activo' : 'Inactivo'}
              </span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{editingDepartamento ? 'Editar Departamento' : 'Nuevo Departamento'}</h3>
              <button className="close-btn" onClick={closeModal}>×</button>
            </div>
            <form onSubmit={handleSubmit} className="modal-form">
              <div className="form-group">
                <label>Nombre:</label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Descripción:</label>
                <textarea
                  value={formData.descripcion}
                  onChange={(e) => setFormData({...formData, descripcion: e.target.value})}
                  rows={3}
                />
              </div>
              <div className="form-group">
                <label>Planta:</label>
                <select
                  value={formData.planta_id}
                  onChange={(e) => setFormData({...formData, planta_id: e.target.value})}
                  required
                >
                  <option value="">Seleccionar planta</option>
                  {plantas.map(planta => (
                    <option key={planta.planta_id} value={planta.planta_id}>
                      {planta.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-actions">
                <button type="button" className="btn-secondary" onClick={closeModal}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary">
                  {editingDepartamento ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionDepartamentos;
