import React, { useState, useEffect, useCallback } from 'react';
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

interface EmpleadosCRUDProps {
  userData?: any; // Para filtrar por planta cuando es Admin Planta
}

const EmpleadosCRUD: React.FC<EmpleadosCRUDProps> = ({ userData }) => {
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  
  // Estados para filtros
  const [filtroNombre, setFiltroNombre] = useState('');
  const [filtroDepartamento, setFiltroDepartamento] = useState('');
  const [filtroPuesto, setFiltroPuesto] = useState('');
  const [empleadosFiltrados, setEmpleadosFiltrados] = useState<Empleado[]>([]);
  
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
  const [loadingData, setLoadingData] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  const loadData = useCallback(async () => {
    setLoadingData(true);
    try {
      console.log('🔍 EmpleadosCRUD: Iniciando carga de datos...');
      const [empleadosData, plantasData, departamentosData, puestosData] = await Promise.all([
        getEmpleados(),
        getPlantas(),
        getDepartamentos(),
        getPuestos()
      ]);
      
      console.log('✅ Datos cargados:', {
        empleados: empleadosData.length,
        plantas: plantasData.length,
        departamentos: departamentosData.length,
        puestos: puestosData.length
      });
      
      // Si es Admin Planta, filtrar solo datos de su planta asignada
      if (userData?.tipo_dashboard === 'admin-planta' && userData?.planta_id) {
        const empleadosDePlanta = empleadosData.filter(emp => emp.planta === userData.planta_id);
        const departamentosDePlanta = departamentosData.filter(dept => dept.planta_id === userData.planta_id);
        const puestosDePlanta = puestosData.filter(puesto => 
          departamentosDePlanta.some(dept => dept.departamento_id === puesto.departamento_id)
        );
        
        setEmpleados(empleadosDePlanta);
        setPlantas([{ planta_id: userData.planta_id, nombre: userData.nombre_planta }]);
        setDepartamentos(departamentosDePlanta);
        setPuestos(puestosDePlanta);
        
        // Pre-seleccionar la planta para nuevos empleados
        setFormData(prev => ({ ...prev, planta: userData.planta_id }));
      } else {
        // Admin Empresa puede ver todos los datos de su empresa
        setEmpleados(empleadosData);
        setPlantas(plantasData);
        setDepartamentos(departamentosData);
        setPuestos(puestosData);
      }
    } catch (err: any) {
      console.error('❌ Error cargando datos:', err);
      setError('Error al cargar datos: ' + (err.message || 'Error desconocido'));
    } finally {
      setLoadingData(false);
    }
  }, [userData]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  useEffect(() => {
    // Filtrar empleados cuando cambian los filtros o empleados
    let filtrados = empleados;
    
    if (filtroNombre.trim()) {
      filtrados = filtrados.filter(empleado =>
        empleado.nombre.toLowerCase().includes(filtroNombre.toLowerCase()) ||
        empleado.apellido_paterno.toLowerCase().includes(filtroNombre.toLowerCase()) ||
        (empleado.apellido_materno && empleado.apellido_materno.toLowerCase().includes(filtroNombre.toLowerCase()))
      );
    }
    
    if (filtroDepartamento) {
      filtrados = filtrados.filter(empleado => 
        empleado.departamento === parseInt(filtroDepartamento)
      );
    }
    
    if (filtroPuesto) {
      filtrados = filtrados.filter(empleado => 
        empleado.puesto === parseInt(filtroPuesto)
      );
    }
    
    setEmpleadosFiltrados(filtrados);
  }, [empleados, filtroNombre, filtroDepartamento, filtroPuesto]);

  const filteredDepartamentos = departamentos.filter(dept => {
    // Si no hay planta seleccionada, no mostrar departamentos
    if (!formData.planta) return false;
    // Filtrar por planta seleccionada - asegurar que ambos sean números
    return dept.planta_id === Number(formData.planta);
  });
  
  const filteredPuestos = puestos.filter(puesto => {
    // Si no hay departamento seleccionado, no mostrar puestos
    if (!formData.departamento) return false;
    // Filtrar por departamento seleccionado - asegurar que ambos sean números
    return puesto.departamento_id === Number(formData.departamento);
  });

  // Debug logging
  console.log('Debug Empleados CRUD:', {
    'formData.planta': formData.planta,
    'formData.planta type': typeof formData.planta,
    'departamentos total': departamentos.length,
    'filteredDepartamentos': filteredDepartamentos.length,
    'departamentos sample': departamentos.slice(0, 2).map(d => ({ id: d.departamento_id, nombre: d.nombre, planta_id: d.planta_id })),
    'filteredDepartamentos sample': filteredDepartamentos.slice(0, 2).map(d => ({ id: d.departamento_id, nombre: d.nombre, planta_id: d.planta_id }))
  });

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
    const empleado = empleados.find(emp => emp.empleado_id === id);
    const nombreCompleto = empleado ? `${empleado.nombre} ${empleado.apellido_paterno} ${empleado.apellido_materno || ''}`.trim() : 'este empleado';
    
    const confirmMessage = `¿Está seguro de eliminar al empleado "${nombreCompleto}"?\n\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        await deleteEmpleado(id);
        await loadData();
        alert('Empleado eliminado exitosamente');
      } catch (err: any) {
        setError('Error al eliminar empleado');
        alert('Error al eliminar el empleado');
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
      
      {loadingData && (
        <div className="loading-message">
          <p>Cargando datos de empleados...</p>
        </div>
      )}
      
      {/* Filtros */}
      <div className="filtros">
        <div className="filtros-row">
          <div className="filtro-group">
            <label>Buscar por nombre:</label>
            <input
              type="text"
              placeholder="Nombre o apellidos..."
              value={filtroNombre}
              onChange={(e) => setFiltroNombre(e.target.value)}
              className="filtro-input"
            />
          </div>
          
          <div className="filtro-group">
            <label>Departamento:</label>
            <select
              value={filtroDepartamento}
              onChange={(e) => setFiltroDepartamento(e.target.value)}
              className="filtro-select"
            >
              <option value="">Todos los departamentos</option>
              {departamentos.map((dept) => (
                <option key={dept.departamento_id} value={dept.departamento_id}>
                  {dept.nombre}
                </option>
              ))}
            </select>
          </div>
          
          <div className="filtro-group">
            <label>Puesto:</label>
            <select
              value={filtroPuesto}
              onChange={(e) => setFiltroPuesto(e.target.value)}
              className="filtro-select"
            >
              <option value="">Todos los puestos</option>
              {puestos.map((puesto) => (
                <option key={puesto.puesto_id} value={puesto.puesto_id}>
                  {puesto.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        {(filtroNombre || filtroDepartamento || filtroPuesto) && (
          <div className="filtros-info">
            Mostrando {empleadosFiltrados.length} de {empleados.length} empleados
            <button 
              onClick={() => {
                setFiltroNombre('');
                setFiltroDepartamento('');
                setFiltroPuesto('');
              }}
              className="btn-clear-filters"
            >
              Limpiar filtros
            </button>
          </div>
        )}
      </div>
      
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
              {userData?.tipo_dashboard === 'admin-planta' ? (
                <input
                  type="text"
                  value={userData?.nombre_planta || 'Planta no asignada'}
                  disabled
                  className="readonly-input"
                  title="Como Admin de Planta, solo puedes gestionar empleados de tu planta asignada"
                />
              ) : (
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
              )}
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
            {empleadosFiltrados.map(empleado => (
              <tr key={empleado.empleado_id}>
                <td>{empleado.nombre}</td>
                <td>{`${empleado.apellido_paterno} ${empleado.apellido_materno || ''}`}</td>
                <td>{empleado.genero}</td>
                <td>{empleado.antiguedad || 0} años</td>
                <td>{plantas.find(p => p.planta_id === empleado.planta)?.nombre || 'N/A'}</td>
                <td>{departamentos.find(d => d.departamento_id === empleado.departamento)?.nombre || 'N/A'}</td>
                <td>{puestos.find(p => p.puesto_id === empleado.puesto)?.nombre || 'N/A'}</td>
                <td>
                  <div className="action-buttons">
                    <button 
                      onClick={() => handleEdit(empleado)}
                      className="btn-edit"
                      title="Editar empleado"
                    >
                      ✏️ Editar
                    </button>
                    <button 
                      onClick={() => handleDelete(empleado.empleado_id!)}
                      className="btn-delete"
                      title="Eliminar empleado"
                    >
                      🗑️ Eliminar
                    </button>
                  </div>
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
