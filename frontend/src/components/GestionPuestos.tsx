import React, { useState, useEffect } from 'react';
import { obtenerPuestos, crearPuesto, actualizarPuesto, eliminarPuesto, obtenerDepartamentos, Puesto, Departamento } from '../services/organizacionService';
import '../css/GestionPuestos.css';

const GestionPuestos: React.FC = () => {
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingPuesto, setEditingPuesto] = useState<Puesto | null>(null);
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    departamento_id: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [puestosData, departamentosData] = await Promise.all([
        obtenerPuestos(),
        obtenerDepartamentos()
      ]);
      setPuestos(puestosData);
      setDepartamentos(departamentosData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingPuesto) {
        await actualizarPuesto(editingPuesto.puesto_id!, {
          nombre: formData.nombre,
          descripcion: formData.descripcion,
          departamento_id: parseInt(formData.departamento_id)
        });
      } else {
        await crearPuesto({
          nombre: formData.nombre,
          descripcion: formData.descripcion,
          departamento_id: parseInt(formData.departamento_id)
        });
      }
      setShowModal(false);
      setFormData({ nombre: '', descripcion: '', departamento_id: '' });
      setEditingPuesto(null);
      loadData();
    } catch (error) {
      console.error('Error saving puesto:', error);
    }
  };

  const handleEdit = (puesto: Puesto) => {
    setEditingPuesto(puesto);
    setFormData({
      nombre: puesto.nombre,
      descripcion: puesto.descripcion || '',
      departamento_id: puesto.departamento_id?.toString() || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de eliminar este puesto?')) {
      try {
        await eliminarPuesto(id);
        loadData();
      } catch (error) {
        console.error('Error deleting puesto:', error);
      }
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setFormData({ nombre: '', descripcion: '', departamento_id: '' });
    setEditingPuesto(null);
  };

  if (loading) {
    return <div className="loading">Cargando puestos...</div>;
  }

  return (
    <div className="gestion-puestos">
      <div className="header-section">
        <h2>💼 Gestión de Puestos</h2>
        <button className="btn-primary" onClick={() => setShowModal(true)}>
          + Nuevo Puesto
        </button>
      </div>

      <div className="puestos-grid">
        {puestos.map(puesto => (
          <div key={puesto.puesto_id} className="puesto-card">
            <div className="card-header">
              <h3>{puesto.nombre}</h3>
              <div className="card-actions">
                <button 
                  className="btn-edit"
                  onClick={() => handleEdit(puesto)}
                >
                  ✏️
                </button>
                <button 
                  className="btn-delete"
                  onClick={() => handleDelete(puesto.puesto_id!)}
                >
                  🗑️
                </button>
              </div>
            </div>
            <div className="card-body">
              <p className="description">{puesto.descripcion}</p>
              <p className="departamento-info">
                <strong>Departamento:</strong> {puesto.departamento_nombre}
              </p>
              <span className={`status ${puesto.status ? 'active' : 'inactive'}`}>
                {puesto.status ? 'Activo' : 'Inactivo'}
              </span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{editingPuesto ? 'Editar Puesto' : 'Nuevo Puesto'}</h3>
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
                <label>Departamento:</label>
                <select
                  value={formData.departamento_id}
                  onChange={(e) => setFormData({...formData, departamento_id: e.target.value})}
                  required
                >
                  <option value="">Seleccionar departamento</option>
                  {departamentos.map(departamento => (
                    <option key={departamento.departamento_id} value={departamento.departamento_id}>
                      {departamento.nombre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-actions">
                <button type="button" className="btn-secondary" onClick={closeModal}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary">
                  {editingPuesto ? 'Actualizar' : 'Crear'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionPuestos;
