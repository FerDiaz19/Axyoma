import React, { useState, useEffect } from 'react';
import { 
  getEmpleados, 
  createEmpleado, 
  updateEmpleado, 
  deleteEmpleado,
  getPlantas,
  getDepartamentos,
  getPuestos 
} from '../services/empleadoService';
import '../css/EmpleadosCRUD.css';

interface Empleado {
  empleado_id?: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  genero: 'Masculino' | 'Femenino';
  antiguedad?: number;
  status?: boolean;
  puesto: number;
  departamento: number;
  planta: number;
}

interface Planta {
  planta_id: number;
  nombre: string;
}

interface Departamento {
  departamento_id: number;
  nombre: string;
  planta_id: number; // El backend devuelve planta_id, no planta
  planta_nombre?: string;
}

interface Puesto {
  puesto_id: number;
  nombre: string;
  departamento_id: number; // Cambiado para coincidir con el backend
}

const EmpleadosCRUD: React.FC = () => {
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  const [formData, setFormData] = useState<Empleado>({
    nombre: '',
    apellido_paterno: '',
    apellido_materno: '',
    genero: 'Masculino',
    antiguedad: 0,
    puesto: 0,
    departamento: 0,
    planta: 0
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [empleadosData, plantasData, departamentosData, puestosData] = await Promise.all([
        getEmpleados(),
        getPlantas(),
        getDepartamentos(),
        getPuestos()
      ]);
      
      setEmpleados(empleadosData);
      setPlantas(plantasData);
      setDepartamentos(departamentosData);
      setPuestos(puestosData);
    } catch (err: any) {
      console.error('Error cargando datos:', err);
      setError('Error al cargar datos');
    }
  };

  const filteredDepartamentos = departamentos.filter(dept => dept.planta_id === formData.planta);
  
  const filteredPuestos = puestos.filter(puesto => puesto.departamento_id === formData.departamento);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    
    // Reset dependent fields when parent changes
    if (name === 'planta') {
      setFormData({
        ...formData,
        planta: parseInt(value) || 0,
        departamento: 0, // Reset departamento when planta changes
        puesto: 0 // Reset puesto when planta changes
      });
    } else if (name === 'departamento') {
      setFormData({
        ...formData,
        departamento: parseInt(value) || 0,
        puesto: 0 // Reset puesto when departamento changes
      });
    } else if (name === 'puesto' || name === 'antiguedad') {
      setFormData({
        ...formData,
        [name]: parseInt(value) || 0
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editingId) {
        await updateEmpleado(editingId, formData);
      } else {
        await createEmpleado(formData);
      }
      await loadData();
      resetForm();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error al guardar empleado');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (empleado: Empleado) => {
    setFormData(empleado);
    setEditingId(empleado.empleado_id || null);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Estás seguro de eliminar este empleado?')) {
      try {
        await deleteEmpleado(id);
        await loadData();
      } catch (err: any) {
        setError('Error al eliminar empleado');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      genero: 'Masculino',
      antiguedad: 0,
      puesto: 0,
      departamento: 0,
      planta: 0
    });
    setEditingId(null);
    setShowForm(false);
  };

  return (
    <div className="empleados-crud">
      <h2>Gestión de Empleados</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="crud-actions">
        <button 
          onClick={() => setShowForm(!showForm)}
          className="btn-primary"
        >
          {showForm ? 'Cancelar' : 'Agregar Empleado'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="empleado-form">
          <h3>{editingId ? 'Editar Empleado' : 'Agregar Empleado'}</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="nombre">Nombre:</label>
              <input
                type="text"
                id="nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="apellido_paterno">Apellido Paterno:</label>
              <input
                type="text"
                id="apellido_paterno"
                name="apellido_paterno"
                value={formData.apellido_paterno}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="apellido_materno">Apellido Materno:</label>
              <input
                type="text"
                id="apellido_materno"
                name="apellido_materno"
                value={formData.apellido_materno || ''}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="genero">Género:</label>
              <select
                id="genero"
                name="genero"
                value={formData.genero}
                onChange={handleChange}
                required
              >
                <option value="Masculino">Masculino</option>
                <option value="Femenino">Femenino</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="antiguedad">Antigüedad (años):</label>
              <input
                type="number"
                id="antiguedad"
                name="antiguedad"
                value={formData.antiguedad || ''}
                onChange={handleChange}
                min="0"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="planta">Planta:</label>
              <select
                id="planta"
                name="planta"
                value={formData.planta || ''}
                onChange={handleChange}
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

            <div className="form-group">
              <label htmlFor="departamento">Departamento:</label>
              <select
                id="departamento"
                name="departamento"
                value={formData.departamento || ''}
                onChange={handleChange}
                required
                disabled={!formData.planta}
              >
                <option value="">Seleccionar departamento</option>
                {filteredDepartamentos.map(dept => (
                  <option key={dept.departamento_id} value={dept.departamento_id}>
                    {dept.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="puesto">Puesto:</label>
              <select
                id="puesto"
                name="puesto"
                value={formData.puesto || ''}
                onChange={handleChange}
                required
                disabled={!formData.departamento}
              >
                <option value="">Seleccionar puesto</option>
                {filteredPuestos.map(puesto => (
                  <option key={puesto.puesto_id} value={puesto.puesto_id}>
                    {puesto.nombre}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              {loading ? 'Guardando...' : editingId ? 'Actualizar' : 'Crear'}
            </button>
            <button type="button" onClick={resetForm}>
              Cancelar
            </button>
          </div>
        </form>
      )}

      <div className="empleados-table">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Apellidos</th>
              <th>Género</th>
              <th>Antigüedad</th>
              <th>Planta</th>
              <th>Departamento</th>
              <th>Puesto</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados.map(empleado => (
              <tr key={empleado.empleado_id}>
                <td>{empleado.nombre}</td>
                <td>{`${empleado.apellido_paterno} ${empleado.apellido_materno || ''}`}</td>
                <td>{empleado.genero}</td>
                <td>{empleado.antiguedad || 0} años</td>
                <td>{plantas.find(p => p.planta_id === empleado.planta)?.nombre || 'N/A'}</td>
                <td>{departamentos.find(d => d.departamento_id === empleado.departamento)?.nombre || 'N/A'}</td>
                <td>{puestos.find(p => p.puesto_id === empleado.puesto)?.nombre || 'N/A'}</td>
                <td>
                  <button 
                    onClick={() => handleEdit(empleado)}
                    className="btn-edit"
                  >
                    Editar
                  </button>
                  <button 
                    onClick={() => handleDelete(empleado.empleado_id!)}
                    className="btn-delete"
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EmpleadosCRUD;
