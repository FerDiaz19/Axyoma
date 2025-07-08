import React, { useState, useEffect, useCallback } from 'react';
import { logout } from '../services/authService';
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
  const [activeSection, setActiveSection] = useState<'estadisticas' | 'empresas' | 'usuarios' | 'plantas' | 'departamentos' | 'puestos' | 'empleados'>('estadisticas');
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
        }
        
        alert(`${nombre} eliminado exitosamente`);
        
      } catch (error: any) {
        console.error('Error al eliminar:', error);
        alert(error.message || 'Error al eliminar');
      }
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
        {activeSection === 'departamentos' && (
          <div className="coming-soon">
            🏢 <strong>Gestión de Departamentos</strong><br/>
            Próximamente: Ver todos los departamentos del sistema con filtros por empresa/planta
          </div>
        )}
        {activeSection === 'puestos' && (
          <div className="coming-soon">
            💼 <strong>Gestión de Puestos</strong><br/>
            Próximamente: Ver todos los puestos del sistema con filtros por empresa/departamento
          </div>
        )}
        {activeSection === 'empleados' && (
          <div className="coming-soon">
            👤 <strong>Gestión de Empleados</strong><br/>
            Próximamente: Ver todos los empleados del sistema con filtros avanzados
          </div>
        )}
      </main>
    </div>
  );
};

export default SuperAdminDashboard;
