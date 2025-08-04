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
  numero_empleado?: string;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  email?: string;
  telefono?: string;
  fecha_ingreso?: string;
  fecha_registro?: string;
  status?: boolean;
  puesto: number;
  departamento?: number;
  planta?: number;

  // Datos relacionados del backend
  empresa_id?: number;
  empresa_nombre?: string;
  planta_id?: number;
  planta_nombre?: string;
  departamento_id?: number;
  departamento_nombre?: string;
  puesto_id?: number;
  puesto_nombre?: string;
}

interface Planta {
  planta_id: number;
  nombre: string;
}

interface Departamento {
  departamento_id: number;
  nombre: string;
  planta_id: number;
  planta_nombre?: string;
}

interface Puesto {
  puesto_id: number;
  nombre: string;
  departamento_id: number;
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
    email: '',
    telefono: '',
    fecha_ingreso: '',
    puesto: 0
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);

  const loadData = useCallback(async () => {
    try {
      console.log('🔄 Cargando datos de empleados...');
      console.log('👤 userData:', userData);

      const [empleadosData, plantasData, departamentosData, puestosData] = await Promise.all([
        getEmpleados(),
        getPlantas(),
        getDepartamentos(),
        getPuestos()
      ]);

      console.log('📊 Datos obtenidos:');
      console.log('  - Empleados:', empleadosData.length);
      console.log('  - Plantas:', plantasData.length);
      console.log('  - Departamentos:', departamentosData.length);
      console.log('  - Puestos:', puestosData.length);

      // Si es Admin Planta, filtrar solo datos de su planta asignada
      if (userData?.tipo_dashboard === 'admin-planta' && userData?.planta_id) {
        console.log('🏭 Filtrando datos para admin-planta:', userData.planta_id);

        const empleadosDePlanta = empleadosData.filter(emp => {
          console.log(`  - Empleado ${emp.nombre}: planta_id=${emp.planta_id}, esperada=${userData.planta_id}`);
          return emp.planta_id === userData.planta_id;
        });

        const departamentosDePlanta = departamentosData.filter(dept => dept.planta_id === userData.planta_id);
        const puestosDePlanta = puestosData.filter(puesto =>
          departamentosDePlanta.some(dept => dept.departamento_id === puesto.departamento_id)
        );

        console.log('📊 Datos filtrados:');
        console.log('  - Empleados de planta:', empleadosDePlanta.length);
        console.log('  - Departamentos de planta:', departamentosDePlanta.length);
        console.log('  - Puestos de planta:', puestosDePlanta.length);
        console.log('🔍 Empleados de planta:', empleadosDePlanta);

        setEmpleados(empleadosDePlanta);
        setPlantas([{ planta_id: userData.planta_id, nombre: userData.nombre_planta }]);
        setDepartamentos(departamentosDePlanta);
        setPuestos(puestosDePlanta);

        // Pre-seleccionar la planta para nuevos empleados
        setFormData(prev => ({ ...prev, planta: userData.planta_id }));
      } else {
        // Admin Empresa puede ver todos los datos de su empresa
        console.log('🏢 Datos completos para admin-empresa');
        setEmpleados(empleadosData);
        setPlantas(plantasData);
        setDepartamentos(departamentosData);
        setPuestos(puestosData);
      }
    } catch (err: any) {
      console.error('❌ Error cargando datos:', err);
      setError('Error al cargar datos');
    }
  }, [userData]);

  useEffect(() => {
    console.log('📋 Lista de empleados actualizada:', empleados.length, 'empleados');
    console.log('📋 Empleados:', empleados);
  }, [empleados]);

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
        empleado.departamento_id === parseInt(filtroDepartamento)
      );
    }

    if (filtroPuesto) {
      filtrados = filtrados.filter(empleado =>
        empleado.puesto === parseInt(filtroPuesto)
      );
    }

    setEmpleadosFiltrados(filtrados);
  }, [empleados, filtroNombre, filtroDepartamento, filtroPuesto]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;

    if (name === 'puesto' || name === 'departamento') {
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

    // Si cambia el departamento, resetear el puesto
    if (name === 'departamento') {
      setFormData(prev => ({
        ...prev,
        departamento: parseInt(value) || 0,
        puesto: 0 // Reset puesto cuando cambia departamento
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    console.log('📝 Datos del formulario a enviar:', formData);

    try {
      if (editingId) {
        console.log('🔄 Actualizando empleado ID:', editingId);
        await updateEmpleado(editingId, formData);
        console.log('✅ Empleado actualizado exitosamente');
      } else {
        const resultado = await createEmpleado(formData);
        console.log('✅ Empleado creado exitosamente:', resultado);
      }
      console.log('🔄 Recargando datos...');
      await loadData();
      console.log('✅ Datos recargados');
      resetForm();
    } catch (err: any) {
      console.error('❌ Error:', err.response?.data?.detail || err.message);
      console.error('❌ Error completo:', err.response?.data);
      setError(err.response?.data?.error || err.response?.data?.detail || 'Error al guardar empleado');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (empleado: Empleado) => {
    setFormData({
      nombre: empleado.nombre,
      apellido_paterno: empleado.apellido_paterno,
      apellido_materno: empleado.apellido_materno || '',
      email: empleado.email || '',
      telefono: empleado.telefono || '',
      fecha_ingreso: empleado.fecha_ingreso || '',
      puesto: empleado.puesto_id || empleado.puesto || 0,
      departamento: empleado.departamento_id || empleado.departamento || 0,
      planta: empleado.planta_id || empleado.planta || 0
    });
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
      email: '',
      telefono: '',
      fecha_ingreso: '',
      departamento: 0,
      puesto: 0
    });
    setEditingId(null);
    setShowForm(false);
  };

  return (
    <div className="empleados-crud">
      <h2>Gestión de Empleados</h2>

      {error && <div className="error-message">{error}</div>}

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
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email || ''}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="telefono">Teléfono:</label>
              <input
                type="tel"
                id="telefono"
                name="telefono"
                value={formData.telefono || ''}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="fecha_ingreso">Fecha de Ingreso:</label>
              <input
                type="date"
                id="fecha_ingreso"
                name="fecha_ingreso"
                value={formData.fecha_ingreso || ''}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="departamento">Departamento:</label>
              <select
                id="departamento"
                name="departamento"
                value={formData.departamento || ''}
                onChange={handleChange}
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
                <option value="">
                  {!formData.departamento ? 'Primero selecciona un departamento' : 'Seleccionar puesto'}
                </option>
                {puestos
                  .filter(puesto => puesto.departamento_id === formData.departamento)
                  .map(puesto => (
                    <option key={puesto.puesto_id} value={puesto.puesto_id}>
                      {puesto.nombre}
                    </option>
                  ))
                }
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
              <th>Email</th>
              <th>Teléfono</th>
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
                <td>{empleado.email || 'N/A'}</td>
                <td>{empleado.telefono || 'N/A'}</td>
                <td>{empleado.planta_nombre || 'N/A'}</td>
                <td>{empleado.departamento_nombre || 'N/A'}</td>
                <td>{empleado.puesto_nombre || 'N/A'}</td>
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
