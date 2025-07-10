import React, { useState, useEffect, useCallback } from 'react';
import { logout } from '../services/authService';
import EditModal from './EditModal';
import GestionEvaluaciones from './GestionEvaluaciones';
import {
  getEstadisticasSistema,
  getEmpresas,
  getUsuarios,
  getPlantas,
  getDepartamentos,
  getPuestos,
  getEmpleados,
  suspenderEmpresa,
  suspenderUsuario,
  eliminarEmpresa,
  eliminarUsuario,
  editarEmpresa,
  editarUsuario,
  crearUsuario,
  type SuperAdminEmpresa,
  type SuperAdminUsuario,
  type SuperAdminPlanta,
  type SuperAdminDepartamento,
  type SuperAdminPuesto,
  type SuperAdminEmpleado,
  type SuperAdminEstadisticas
} from '../services/superAdminService';
import '../css/SuperAdminDashboard.css';

interface SuperAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'estadisticas' | 'empresas' | 'usuarios' | 'plantas' | 'departamentos' | 'puestos' | 'empleados' | 'evaluaciones'>('estadisticas');
  const [loading, setLoading] = useState(false);
  
  // Estados para datos
  const [estadisticas, setEstadisticas] = useState<SuperAdminEstadisticas | null>(null);
  const [empresas, setEmpresas] = useState<SuperAdminEmpresa[]>([]);
  const [usuarios, setUsuarios] = useState<SuperAdminUsuario[]>([]);
  const [plantas, setPlantas] = useState<SuperAdminPlanta[]>([]);
  const [departamentos, setDepartamentos] = useState<SuperAdminDepartamento[]>([]);
  const [puestos, setPuestos] = useState<SuperAdminPuesto[]>([]);
  const [empleados, setEmpleados] = useState<SuperAdminEmpleado[]>([]);
  
  // Estados para filtros
  const [filtroTexto, setFiltroTexto] = useState('');
  const [filtroStatus, setFiltroStatus] = useState<'all' | 'active' | 'inactive'>('all');
  const [filtroNivelUsuario, setFiltroNivelUsuario] = useState('');
  const [filtroEmpresa, setFiltroEmpresa] = useState('');

  // Estados para modal de edición
  const [modalEditar, setModalEditar] = useState<{
    isOpen: boolean;
    type: string;
    data: any;
    title: string;
  }>({
    isOpen: false,
    type: '',
    data: {},
    title: ''
  });

  const cargarEstadisticas = async () => {
    setLoading(true);
    try {
      console.log('🔄 SuperAdmin: Cargando estadísticas del sistema...');
      const data = await getEstadisticasSistema();
      setEstadisticas(data);
      console.log('✅ SuperAdmin: Estadísticas cargadas exitosamente');
    } catch (error) {
      console.error('❌ SuperAdmin: Error cargando estadísticas:', error);
      alert('Error al cargar estadísticas del sistema');
    } finally {
      setLoading(false);
    }
  };

  const cargarDatosPorSeccion = useCallback(async () => {
    setLoading(true);
    try {
      console.log(`🔄 SuperAdmin: Cargando datos de ${activeSection}...`);
      
      const params: any = {};
      
      if (filtroTexto) {
        params.buscar = filtroTexto;
      }
      
      if (filtroStatus !== 'all') {
        params.status = filtroStatus === 'active' ? 'true' : 'false';
      }
      
      switch (activeSection) {
        case 'empresas':
          const empresasData = await getEmpresas(params);
          setEmpresas(empresasData.empresas);
          break;
          
        case 'usuarios':
          if (filtroNivelUsuario) {
            params.nivel_usuario = filtroNivelUsuario;
          }
          if (filtroStatus !== 'all') {
            params.activo = filtroStatus === 'active' ? 'true' : 'false';
            delete params.status;
          }
          const usuariosData = await getUsuarios(params);
          setUsuarios(usuariosData.usuarios);
          break;
          
        case 'plantas':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const plantasData = await getPlantas(params);
          setPlantas(plantasData.plantas);
          break;
          
        case 'departamentos':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const departamentosData = await getDepartamentos(params);
          setDepartamentos(departamentosData.departamentos);
          break;
          
        case 'puestos':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const puestosData = await getPuestos(params);
          setPuestos(puestosData.puestos);
          break;
          
        case 'empleados':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const empleadosData = await getEmpleados(params);
          setEmpleados(empleadosData.empleados);
          break;
      }
      
      console.log(`✅ SuperAdmin: Datos de ${activeSection} cargados exitosamente`);
    } catch (error) {
      console.error(`❌ SuperAdmin: Error cargando ${activeSection}:`, error);
      alert(`Error al cargar ${activeSection}`);
    } finally {
      setLoading(false);
    }
  }, [activeSection, filtroTexto, filtroStatus, filtroNivelUsuario, filtroEmpresa]);

  useEffect(() => {
    cargarEstadisticas();
  }, []);

  useEffect(() => {
    if (activeSection !== 'estadisticas') {
      cargarDatosPorSeccion();
    }
  }, [activeSection, filtroTexto, filtroStatus, filtroNivelUsuario, filtroEmpresa, cargarDatosPorSeccion]);

  const handleLogout = () => {
    logout();
    onLogout();
  };

  // Función para suspender/activar
  const handleToggleStatus = async (type: string, id: number, currentStatus: boolean, nombre: string) => {
    const action = currentStatus ? 'suspender' : 'activar';
    const confirmMessage = `¿Está seguro de ${action} "${nombre}"?\n\n${action === 'suspender' ? 'Se pondrá en hibernación.' : 'Se reactivará completamente.'}`;
    
    if (window.confirm(confirmMessage)) {
      try {
        if (type === 'empresa') {
          await suspenderEmpresa(id, action);
          setEmpresas(prev => prev.map(item => 
            item.empresa_id === id ? { ...item, status: !currentStatus } : item
          ));
        } else if (type === 'usuario') {
          await suspenderUsuario(id, action);
          setUsuarios(prev => prev.map(item => 
            item.user_id === id ? { ...item, is_active: !currentStatus } : item
          ));
        } else if (type === 'departamento') {
          setDepartamentos(prev => prev.map(item => 
            item.departamento_id === id ? { ...item, activo: !currentStatus } : item
          ));
        } else if (type === 'empleado') {
          setEmpleados(prev => prev.map(item => 
            item.empleado_id === id ? { ...item, activo: !currentStatus } : item
          ));
        }
        
        alert(`${nombre} ${action === 'suspender' ? 'suspendido' : 'activado'} exitosamente`);
        
      } catch (error: any) {
        console.error(`Error al ${action}:`, error);
        alert(error.message || `Error al ${action}`);
      }
    }
  };

  // Función para eliminar
  const handleDelete = async (type: string, id: number, nombre: string) => {
    const confirmMessage = `¿Está seguro de ELIMINAR PERMANENTEMENTE "${nombre}"?\n\nEsta acción NO se puede deshacer y eliminará todos los datos relacionados.\n\nEscriba "ELIMINAR" para confirmar:`;
    
    const confirmation = prompt(confirmMessage);
    if (confirmation === 'ELIMINAR') {
      try {
        if (type === 'empresa') {
          await eliminarEmpresa(id);
          setEmpresas(prev => prev.filter(item => item.empresa_id !== id));
        } else if (type === 'usuario') {
          await eliminarUsuario(id);
          setUsuarios(prev => prev.filter(item => item.user_id !== id));
        } else if (type === 'departamento') {
          setDepartamentos(prev => prev.filter(item => item.departamento_id !== id));
        } else if (type === 'empleado') {
          setEmpleados(prev => prev.filter(item => item.empleado_id !== id));
        }
        
        alert(`${nombre} eliminado exitosamente`);
        
      } catch (error: any) {
        console.error('Error al eliminar:', error);
        alert(error.message || 'Error al eliminar');
      }
    }
  };

  // Función para abrir modal de edición
  const handleOpenEdit = (type: string, data: any, title: string) => {
    setModalEditar({
      isOpen: true,
      type,
      data,
      title
    });
  };

  // Función para cerrar modal de edición
  const handleCloseEdit = () => {
    setModalEditar({
      isOpen: false,
      type: '',
      data: {},
      title: ''
    });
  };

  // Función para guardar cambios en modal de edición
  const handleSaveEdit = async (updatedData: any) => {
    try {
      // Verificar si es edición o creación
      const isCreating = Object.keys(modalEditar.data).length === 0;
      
      if (isCreating) {
        // Crear nuevo elemento
        await handleSaveCreate(updatedData);
      } else {
        // Editar elemento existente
        switch (modalEditar.type) {
          case 'empresa':
            if (!modalEditar.data.empresa_id) {
              throw new Error('ID de empresa no encontrado');
            }
            await editarEmpresa(modalEditar.data.empresa_id, updatedData);
            break;
          case 'usuario':
            if (!modalEditar.data.user_id) {
              throw new Error('ID de usuario no encontrado');
            }
            await editarUsuario(modalEditar.data.user_id, updatedData);
            break;
          default:
            throw new Error(`Edición de tipo "${modalEditar.type}" no implementada`);
        }
        console.log('✅ Elemento editado exitosamente:', modalEditar.type);
      }
      
      handleCloseEdit();
      // Recargar datos de la sección activa
      await cargarDatosPorSeccion();
    } catch (error: any) {
      console.error('Error al guardar cambios:', error);
      throw error; // Re-lanzar para que EditModal pueda manejarlo
    }
  };

  // Función para abrir modal de creación
  const handleOpenCreate = (type: string, title: string) => {
    setModalEditar({
      isOpen: true,
      type,
      data: {}, // Datos vacíos para crear
      title
    });
  };

  // Función para crear nuevo elemento
  const handleSaveCreate = async (newData: any) => {
    try {
      switch (modalEditar.type) {
        case 'usuario':
          // Solo permitir crear usuarios SuperAdmin
          await crearUsuario({
            username: newData.username,
            email: newData.email,
            nombre: newData.nombre,
            apellido_paterno: newData.apellido_paterno,
            apellido_materno: newData.apellido_materno || '',
            password: newData.password || '1234',
            is_active: newData.is_active !== false
          });
          break;
        
        // TODO: Implementar otros tipos de creación cuando sea necesario
        default:
          throw new Error(`Creación de tipo "${modalEditar.type}" no implementada`);
      }
      
      console.log('✅ Elemento creado exitosamente:', modalEditar.type);
      handleCloseEdit();
      // Recargar datos de la sección activa
      await cargarDatosPorSeccion();
    } catch (error: any) {
      console.error('Error al crear:', error);
      throw error; // Re-lanzar para que EditModal pueda manejarlo
    }
  };

  // Función para obtener los campos del modal según el tipo
  const getModalFields = () => {
    switch (modalEditar.type) {
      case 'empresa':
        return [
          { name: 'nombre', label: 'Nombre de la Empresa', type: 'text' as const, required: true },
          { name: 'rfc', label: 'RFC', type: 'text' as const, required: true },
          { name: 'telefono', label: 'Teléfono', type: 'text' as const, required: false },
          { name: 'correo', label: 'Correo Electrónico', type: 'email' as const, required: false },
          { name: 'direccion', label: 'Dirección', type: 'textarea' as const, required: false },
          { name: 'status', label: 'Activa', type: 'checkbox' as const, required: false }
        ];
      case 'usuario':
        return [
          { name: 'username', label: 'Nombre de Usuario', type: 'text' as const, required: true },
          { name: 'email', label: 'Correo Electrónico', type: 'email' as const, required: true },
          { name: 'nombre', label: 'Nombre', type: 'text' as const, required: true },
          { name: 'apellido_paterno', label: 'Apellido Paterno', type: 'text' as const, required: true },
          { name: 'apellido_materno', label: 'Apellido Materno', type: 'text' as const, required: false },
          { name: 'nivel_usuario', label: 'Rol', type: 'select' as const, required: true, options: [
            { value: 'superadmin', label: 'Super Administrador' }
          ], disabled: modalEditar.data && Object.keys(modalEditar.data).length > 0 }, // Solo edición, no creación
          { name: 'password', label: 'Contraseña', type: 'password' as const, required: modalEditar.data && Object.keys(modalEditar.data).length === 0 }, // Solo para creación
          { name: 'is_active', label: 'Usuario Activo', type: 'checkbox' as const, required: false }
        ];
      case 'departamento':
        return [
          { name: 'nombre', label: 'Nombre del Departamento', type: 'text' as const, required: true },
          { name: 'descripcion', label: 'Descripción', type: 'textarea' as const, required: false },
          { name: 'status', label: 'Activo', type: 'checkbox' as const, required: false }
        ];
      case 'empleado':
        return [
          { name: 'nombre', label: 'Nombre', type: 'text' as const, required: true },
          { name: 'apellido_paterno', label: 'Apellido Paterno', type: 'text' as const, required: true },
          { name: 'apellido_materno', label: 'Apellido Materno', type: 'text' as const, required: false },
          { name: 'correo', label: 'Correo Electrónico', type: 'email' as const, required: false },
          { name: 'telefono', label: 'Teléfono', type: 'text' as const, required: false },
          { name: 'numero_empleado', label: 'Número de Empleado', type: 'text' as const, required: true },
          { name: 'salario', label: 'Salario', type: 'number' as const, required: false },
          { name: 'status', label: 'Activo', type: 'checkbox' as const, required: false }
        ];
      default:
        return [];
    }
  };

  // Funciones de filtrado
  const filtrarEmpresas = () => {
    return empresas.filter(empresa => {
      const matchTexto = empresa.nombre.toLowerCase().includes(filtroTexto.toLowerCase()) ||
                        empresa.rfc.toLowerCase().includes(filtroTexto.toLowerCase());
      const matchStatus = filtroStatus === 'all' || 
                         (filtroStatus === 'active' && empresa.status) ||
                         (filtroStatus === 'inactive' && !empresa.status);
      return matchTexto && matchStatus;
    });
  };

  const filtrarUsuarios = () => {
    return usuarios.filter(usuario => {
      const matchTexto = usuario.username.toLowerCase().includes(filtroTexto.toLowerCase()) ||
                        usuario.email.toLowerCase().includes(filtroTexto.toLowerCase()) ||
                        usuario.nombre_completo.toLowerCase().includes(filtroTexto.toLowerCase());
      const matchStatus = filtroStatus === 'all' || 
                         (filtroStatus === 'active' && usuario.is_active) ||
                         (filtroStatus === 'inactive' && !usuario.is_active);
      const matchNivel = !filtroNivelUsuario || usuario.nivel_usuario === filtroNivelUsuario;
      const matchEmpresa = !filtroEmpresa || 
                          (usuario.empresa && usuario.empresa.nombre.toLowerCase().includes(filtroEmpresa.toLowerCase())) ||
                          (usuario.planta && usuario.planta.empresa_nombre.toLowerCase().includes(filtroEmpresa.toLowerCase()));
      return matchTexto && matchStatus && matchNivel && matchEmpresa;
    });
  };

  const filtrarDepartamentos = () => {
    return departamentos.filter(departamento => {
      const matchTexto = departamento.nombre.toLowerCase().includes(filtroTexto.toLowerCase());
      const matchStatus = filtroStatus === 'all' || 
                         (filtroStatus === 'active' && departamento.status) ||
                         (filtroStatus === 'inactive' && !departamento.status);
      return matchTexto && matchStatus;
    });
  };

  const filtrarEmpleados = () => {
    return empleados.filter(empleado => {
      const matchTexto = empleado.nombre_completo.toLowerCase().includes(filtroTexto.toLowerCase()) ||
                        (empleado.correo && empleado.correo.toLowerCase().includes(filtroTexto.toLowerCase()));
      const matchStatus = filtroStatus === 'all' || 
                         (filtroStatus === 'active' && empleado.status) ||
                         (filtroStatus === 'inactive' && !empleado.status);
      const matchEmpresa = !filtroEmpresa || empleado.empresa.nombre.toLowerCase().includes(filtroEmpresa.toLowerCase());
      return matchTexto && matchStatus && matchEmpresa;
    });
  };

  // Render de filtros
  const renderFiltros = () => (
    <div className="filtros-container">
      <div className="filtros-row">
        <input
          type="text"
          placeholder="Buscar..."
          value={filtroTexto}
          onChange={(e) => setFiltroTexto(e.target.value)}
          className="filtro-input"
        />
        
        <select
          value={filtroStatus}
          onChange={(e) => setFiltroStatus(e.target.value as any)}
          className="filtro-select"
        >
          <option value="all">Todos los estados</option>
          <option value="active">Solo activos</option>
          <option value="inactive">Solo inactivos</option>
        </select>
        
        {activeSection === 'usuarios' && (
          <select
            value={filtroNivelUsuario}
            onChange={(e) => setFiltroNivelUsuario(e.target.value)}
            className="filtro-select"
          >
            <option value="">Todos los niveles</option>
            <option value="superadmin">Super Admin</option>
            <option value="admin-empresa">Admin Empresa</option>
            <option value="admin-planta">Admin Planta</option>
            <option value="empleado">Empleado</option>
          </select>
        )}
        
        {(activeSection === 'usuarios' || activeSection === 'plantas' || activeSection === 'departamentos' || activeSection === 'puestos' || activeSection === 'empleados') && (
          <input
            type="text"
            placeholder="Filtrar por empresa..."
            value={filtroEmpresa}
            onChange={(e) => setFiltroEmpresa(e.target.value)}
            className="filtro-input"
          />
        )}
        
        <button 
          onClick={() => {
            setFiltroTexto('');
            setFiltroStatus('all');
            setFiltroNivelUsuario('');
            setFiltroEmpresa('');
          }}
          className="btn-secondary"
        >
          Limpiar filtros
        </button>
      </div>
    </div>
  );

  // Render de tabla de empresas
  const renderEmpresas = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>🏢 Gestión de Empresas</h3>
        <div className="stats-mini">
          <span>Total: {empresas.length}</span>
          <span>Activas: {empresas.filter(e => e.status).length}</span>
          <span>Suspendidas: {empresas.filter(e => !e.status).length}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>RFC</th>
              <th>Administrador</th>
              <th>Plantas</th>
              <th>Empleados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filtrarEmpresas().map((empresa) => (
              <tr key={empresa.empresa_id}>
                <td>{empresa.empresa_id}</td>
                <td>
                  <div>
                    <strong>{empresa.nombre}</strong>
                    <small>{empresa.correo}</small>
                  </div>
                </td>
                <td>{empresa.rfc}</td>
                <td>
                  <div>
                    <strong>{empresa.administrador?.nombre_completo || 'Sin asignar'}</strong>
                    <small>{empresa.administrador?.email || ''}</small>
                  </div>
                </td>
                <td>{empresa.plantas_count}</td>
                <td>{empresa.empleados_count}</td>
                <td>
                  <span className={`status ${empresa.status ? 'active' : 'inactive'}`}>
                    {empresa.status ? '🟢 Activa' : '🔴 Suspendida'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('empresa', empresa.empresa_id, empresa.status, empresa.nombre)}
                      className={`btn-action ${empresa.status ? 'warning' : 'success'}`}
                    >
                      {empresa.status ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('empresa', empresa.empresa_id, empresa.nombre)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleOpenEdit('empresa', empresa, `Editar Empresa: ${empresa.nombre}`)}
                      className="btn-action edit"
                      title="Editar empresa"
                    >
                      ✏️ Editar
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

  // Render de tabla de usuarios
  const renderUsuarios = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>👥 Gestión de Usuarios</h3>
        <div className="section-actions">
          {/* Solo mostrar botón de crear usuario para SuperAdmin */}
          {userData?.nivel_usuario === 'superadmin' && (
            <button 
              onClick={() => handleOpenCreate('usuario', 'Crear Nuevo Usuario SuperAdmin')}
              className="superadmin-create-btn"
            >
              ➕ Crear Usuario SuperAdmin
            </button>
          )}
        </div>
        <div className="stats-mini">
          <span>Total: {usuarios.length}</span>
          <span>Activos: {usuarios.filter(u => u.is_active).length}</span>
          <span>Suspendidos: {usuarios.filter(u => !u.is_active).length}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Usuario</th>
              <th>Nombre</th>
              <th>Nivel</th>
              <th>Empresa/Planta</th>
              <th>Registro</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filtrarUsuarios().map((usuario) => (
              <tr key={usuario.user_id}>
                <td>{usuario.user_id}</td>
                <td>
                  <div>
                    <strong>{usuario.username}</strong>
                    <small>{usuario.email}</small>
                  </div>
                </td>
                <td>{usuario.nombre_completo}</td>
                <td>
                  <span className={`nivel ${usuario.nivel_usuario}`}>
                    {usuario.nivel_usuario === 'superadmin' && '👑 Super Admin'}
                    {usuario.nivel_usuario === 'admin-empresa' && '🏢 Admin Empresa'}
                    {usuario.nivel_usuario === 'admin-planta' && '🏭 Admin Planta'}
                  </span>
                </td>
                <td>
                  <div>
                    {usuario.empresa && <strong>{usuario.empresa.nombre}</strong>}
                    {usuario.planta && <small>{usuario.planta.nombre}</small>}
                  </div>
                </td>
                <td>{new Date(usuario.fecha_registro).toLocaleDateString()}</td>
                <td>
                  <span className={`status ${usuario.is_active ? 'active' : 'inactive'}`}>
                    {usuario.is_active ? '🟢 Activo' : '🔴 Suspendido'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('usuario', usuario.user_id, usuario.is_active, usuario.username)}
                      className={`btn-action ${usuario.is_active ? 'warning' : 'success'}`}
                      disabled={usuario.nivel_usuario === 'superadmin'}
                      title={usuario.nivel_usuario === 'superadmin' ? 'No se puede suspender SuperAdmin' : ''}
                    >
                      {usuario.is_active ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('usuario', usuario.user_id, usuario.username)}
                      className="btn-action danger"
                      disabled={usuario.nivel_usuario === 'superadmin'}
                      title={usuario.nivel_usuario === 'superadmin' ? 'No se puede eliminar SuperAdmin' : ''}
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleOpenEdit('usuario', usuario, `Editar Usuario: ${usuario.nombre_completo}`)}
                      className="btn-action edit"
                      title="Editar usuario"
                    >
                      ✏️ Editar
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

  // Render de tabla de departamentos
  const renderDepartamentos = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>🏢 Gestión de Departamentos Base</h3>
        <div className="section-actions">
          <button 
            onClick={() => handleOpenCreate('departamento', 'Crear Nuevo Departamento')}
            className="btn-create"
          >
            ➕ Crear Departamento
          </button>
        </div>
        <div className="stats-mini">
          <span>Total: {departamentos.length}</span>
          <span>Activos: {departamentos.filter(d => d.status).length}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Estado</th>
              <th>Empresas Usando</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filtrarDepartamentos().map((departamento) => (
              <tr key={departamento.departamento_id}>
                <td>{departamento.departamento_id}</td>
                <td>
                  <div>
                    <strong>{departamento.nombre}</strong>
                  </div>
                </td>
                <td>{departamento.descripcion || 'Sin descripción'}</td>
                <td>
                  <span className={`status ${departamento.status ? 'active' : 'inactive'}`}>
                    {departamento.status ? '🟢 Activo' : '🔴 Inactivo'}
                  </span>
                </td>
                <td>{departamento.empleados_count || 0}</td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('departamento', departamento.departamento_id, departamento.status, departamento.nombre)}
                      className={`btn-action ${departamento.status ? 'warning' : 'success'}`}
                    >
                      {departamento.status ? '⏸️ Desactivar' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('departamento', departamento.departamento_id, departamento.nombre)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleOpenEdit('departamento', departamento, `Editar Departamento: ${departamento.nombre}`)}
                      className="btn-action edit"
                      title="Editar departamento"
                    >
                      ✏️ Editar
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

  // Render de tabla de empleados
  const renderEmpleados = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>👤 Gestión de Empleados</h3>
        <div className="section-actions">
          <button 
            onClick={() => handleOpenCreate('empleado', 'Crear Nuevo Empleado')}
            className="btn-create"
          >
            ➕ Crear Empleado
          </button>
        </div>
        <div className="stats-mini">
          <span>Total: {empleados.length}</span>
          <span>Activos: {empleados.filter(e => e.status).length}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empleado</th>
              <th>Empresa</th>
              <th>Departamento</th>
              <th>Puesto</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filtrarEmpleados().map((empleado) => (
              <tr key={empleado.empleado_id}>
                <td>{empleado.empleado_id}</td>
                <td>
                  <div>
                    <strong>{empleado.nombre_completo}</strong>
                    <small>{empleado.correo}</small>
                  </div>
                </td>
                <td>{empleado.empresa.nombre}</td>
                <td>{empleado.departamento.nombre}</td>
                <td>{empleado.puesto.nombre}</td>
                <td>
                  <span className={`status ${empleado.status ? 'active' : 'inactive'}`}>
                    {empleado.status ? '🟢 Activo' : '🔴 Inactivo'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('empleado', empleado.empleado_id, empleado.status, empleado.nombre_completo)}
                      className={`btn-action ${empleado.status ? 'warning' : 'success'}`}
                    >
                      {empleado.status ? '⏸️ Desactivar' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('empleado', empleado.empleado_id, empleado.nombre_completo)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleOpenEdit('empleado', empleado, `Editar Empleado: ${empleado.nombre_completo}`)}
                      className="btn-action edit"
                      title="Editar empleado"
                    >
                      ✏️ Editar
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

  // Render de estadísticas
  const renderEstadisticas = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>📊 Estadísticas del Sistema</h3>
      </div>
      
      {estadisticas && (
        <div className="stats-grid">
          <div className="stat-card">
            <h4>🏢 Empresas</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_empresas}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activas: {estadisticas.empresas_activas}</span>
              <span>❌ Suspendidas: {estadisticas.total_empresas - estadisticas.empresas_activas}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>🏭 Plantas</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_plantas}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activas: {estadisticas.plantas_activas}</span>
              <span>❌ Suspendidas: {estadisticas.total_plantas - estadisticas.plantas_activas}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>🏢 Departamentos</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_departamentos}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {estadisticas.departamentos_activos}</span>
              <span>❌ Suspendidos: {estadisticas.total_departamentos - estadisticas.departamentos_activos}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>💼 Puestos</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_puestos}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {estadisticas.puestos_activos}</span>
              <span>❌ Suspendidos: {estadisticas.total_puestos - estadisticas.puestos_activos}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>👤 Empleados</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_empleados}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {estadisticas.empleados_activos}</span>
              <span>❌ Suspendidos: {estadisticas.total_empleados - estadisticas.empleados_activos}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>👥 Usuarios</h4>
            <div className="stat-numbers">
              <span className="stat-main">{estadisticas.total_usuarios}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>👑 SuperAdmin: {estadisticas.usuarios_por_nivel.superadmin}</span>
              <span>🏢 Admin Empresa: {estadisticas.usuarios_por_nivel['admin-empresa']}</span>
              <span>🏭 Admin Planta: {estadisticas.usuarios_por_nivel['admin-planta']}</span>
              <span>👤 Empleados: {estadisticas.usuarios_por_nivel.empleado}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  if (loading) {
    return <div className="loading">🔄 Cargando datos del sistema...</div>;
  }

  return (
    <div className="dashboard superadmin-dashboard">
      <header className="dashboard-header">
        <div className="header-info">
          <h1>👑 Panel de Super Administrador</h1>
          <p>Control total del sistema Axyoma</p>
        </div>
        <div className="user-info">
          <span>{userData?.nombre_completo || userData?.usuario}</span>
          <span>({userData?.nivel_usuario})</span>
        </div>
        <button onClick={handleLogout} className="logout-btn">
          Cerrar Sesión
        </button>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={activeSection === 'estadisticas' ? 'active' : ''}
          onClick={() => setActiveSection('estadisticas')}
        >
          📊 Estadísticas
        </button>
        <button 
          className={activeSection === 'empresas' ? 'active' : ''}
          onClick={() => setActiveSection('empresas')}
        >
          🏢 Empresas ({empresas.length})
        </button>
        <button 
          className={activeSection === 'usuarios' ? 'active' : ''}
          onClick={() => setActiveSection('usuarios')}
        >
          👥 Usuarios ({usuarios.length})
        </button>
        <button 
          className={activeSection === 'plantas' ? 'active' : ''}
          onClick={() => setActiveSection('plantas')}
        >
          🏭 Plantas ({plantas.length})
        </button>
        <button 
          className={activeSection === 'departamentos' ? 'active' : ''}
          onClick={() => setActiveSection('departamentos')}
        >
          🏢 Departamentos ({departamentos.length})
        </button>
        <button 
          className={activeSection === 'puestos' ? 'active' : ''}
          onClick={() => setActiveSection('puestos')}
        >
          💼 Puestos ({puestos.length})
        </button>
        <button 
          className={activeSection === 'empleados' ? 'active' : ''}
          onClick={() => setActiveSection('empleados')}
        >
          👤 Empleados ({empleados.length})
        </button>
        <button 
          className={activeSection === 'evaluaciones' ? 'active' : ''}
          onClick={() => setActiveSection('evaluaciones')}
        >
          📝 Evaluaciones
        </button>
      </nav>

      <main className="dashboard-content">
        {activeSection === 'estadisticas' && renderEstadisticas()}
        {activeSection === 'empresas' && renderEmpresas()}
        {activeSection === 'usuarios' && renderUsuarios()}
        {activeSection === 'plantas' && (
          <div className="coming-soon">
            🏭 <strong>Gestión de Plantas</strong><br/>
            Próximamente: Ver todas las plantas del sistema con filtros por empresa
          </div>
        )}
        {activeSection === 'departamentos' && renderDepartamentos()}
        {activeSection === 'puestos' && (
          <div className="coming-soon">
            💼 <strong>Gestión de Puestos</strong><br/>
            Próximamente: Ver todos los puestos del sistema con filtros por empresa/departamento
          </div>
        )}
        {activeSection === 'empleados' && renderEmpleados()}
        {activeSection === 'evaluaciones' && (
          <GestionEvaluaciones 
            usuario={userData}
          />
        )}
      </main>

      {modalEditar.isOpen && (
        <EditModal
          isOpen={modalEditar.isOpen}
          onClose={() => setModalEditar(prev => ({ ...prev, isOpen: false }))}
          title={modalEditar.title}
          initialData={modalEditar.data}
          onSave={handleSaveEdit}
          fields={getModalFields()} // Obtener campos según el tipo
          infoMessage={
            modalEditar.type === 'usuario' && Object.keys(modalEditar.data).length === 0
              ? 'Se creará un nuevo usuario con privilegios de Super Administrador. La contraseña por defecto será "1234".'
              : undefined
          }
          infoType="info"
        />
      )}
    </div>
  );
};

export default SuperAdminDashboard;
