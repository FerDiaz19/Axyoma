import React, { useState, useEffect, useCallback } from 'react';
import { logout } from '../services/authService';
import EvaluacionesGestion from './EvaluacionesGestion';
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
  suspenderPlanta,
  suspenderDepartamento,
  suspenderPuesto,
  suspenderEmpleado,
  eliminarEmpresa,
  eliminarUsuario,
  eliminarPlanta,
  eliminarDepartamento,
  eliminarPuesto,
  eliminarEmpleado,
  editarEmpresa,
  editarUsuario,
  editarPlanta,
  editarDepartamento,
  editarPuesto,
  editarEmpleado,
  type SuperAdminEmpresa,
  type SuperAdminUsuario,
  type SuperAdminPlanta,
  type SuperAdminDepartamento,
  type SuperAdminPuesto,
  type SuperAdminEmpleado,
  type SuperAdminEstadisticas
} from '../services/superAdminService';
import {
  listarPlanes,
  listarSuscripciones,
  listarPagos,
  crearPlan,
  editarPlan,
  crearSuscripcion,
  renovarSuscripcion,
  suspenderSuscripcion,
  reactivarSuscripcion,
  formatearPrecio,
  formatearDuracion,
  getEstadoSuscripcionTexto,
  getEstadoSuscripcionColor,
  getEstadoPagoTexto,
  type PlanSuscripcion,
  type SuscripcionEmpresa,
  type Pago
} from '../services/suscripcionService';
import EditModal from './EditModal';
import '../css/SuperAdminDashboard.css';

interface SuperAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'estadisticas' | 'empresas' | 'usuarios' | 'plantas' | 'departamentos' | 'puestos' | 'empleados' | 'suscripciones' | 'planes' | 'pagos' | 'evaluaciones'>('estadisticas');
  const [loading, setLoading] = useState(false);
  
  // Estados para datos
  const [estadisticas, setEstadisticas] = useState<SuperAdminEstadisticas | null>(null);
  const [empresas, setEmpresas] = useState<SuperAdminEmpresa[]>([]);
  const [usuarios, setUsuarios] = useState<SuperAdminUsuario[]>([]);
  const [plantas, setPlantas] = useState<SuperAdminPlanta[]>([]);
  const [departamentos, setDepartamentos] = useState<SuperAdminDepartamento[]>([]);
  const [puestos, setPuestos] = useState<SuperAdminPuesto[]>([]);
  const [empleados, setEmpleados] = useState<SuperAdminEmpleado[]>([]);
  const [suscripciones, setSuscripciones] = useState<SuscripcionEmpresa[]>([]);
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [pagos, setPagos] = useState<Pago[]>([]);
  
  // Estados para filtros
  const [filtroTexto, setFiltroTexto] = useState('');
  const [filtroStatus, setFiltroStatus] = useState<'all' | 'active' | 'inactive'>('all');
  const [filtroNivelUsuario, setFiltroNivelUsuario] = useState('');
  const [filtroEmpresa, setFiltroEmpresa] = useState('');

  // Estados para modal de edición
  const [modalEditar, setModalEditar] = useState({
    isOpen: false,
    type: '',
    id: 0,
    data: {},
    title: ''
  });

  // Estados para modales de creación
  const [modalCrearPlan, setModalCrearPlan] = useState(false);
  const [modalCrearSuscripcion, setModalCrearSuscripcion] = useState(false);
  const [modalCrearUsuario, setModalCrearUsuario] = useState(false);

  const cargarEstadisticas = async () => {
    setLoading(true);
    try {
      console.log('🔄 SuperAdmin: Cargando estadísticas del sistema...');
      const estadisticasData = await getEstadisticasSistema();
      setEstadisticas(estadisticasData);
      console.log('✅ SuperAdmin: Estadísticas cargadas exitosamente:', estadisticasData);
    } catch (error) {
      console.error('❌ SuperAdmin: Error cargando estadísticas:', error);
      // Si falla, usar datos por defecto
      setEstadisticas({
        total_empresas: 0,
        empresas_activas: 0,
        total_usuarios: 0,
        usuarios_activos: 0,
        total_empleados: 0,
        empleados_activos: 0,
        total_plantas: 0,
        plantas_activas: 0,
        total_departamentos: 0,
        departamentos_activos: 0,
        total_puestos: 0,
        puestos_activos: 0,
        total_evaluaciones: 0,
        total_suscripciones: 0,
        suscripciones_activas: 0,
        planes_disponibles: 0
      });
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
          
        case 'suscripciones':
          const suscripcionesData = await listarSuscripciones();
          setSuscripciones(suscripcionesData);
          break;
          
        case 'planes':
          const planesData = await listarPlanes();
          setPlanes(planesData);
          break;
          
        case 'pagos':
          // Temporalmente deshabilitado - endpoint no disponible
          console.log('⚠️ Pagos temporalmente deshabilitados');
          setPagos([]);
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
  }, [activeSection, cargarDatosPorSeccion]);

  const handleLogout = async () => {
    await logout();
    onLogout();
  };

  // Función para suspender/activar
  const handleToggleStatus = async (type: string, id: number, currentStatus: boolean, nombre?: string) => {
    const action = currentStatus ? 'suspender' : 'activar';
    const nombreItem = nombre || `${type} #${id}`;
    const confirmMessage = `¿Está seguro de ${action} "${nombreItem}"?\n\n${action === 'suspender' ? 'Se pondrá en hibernación.' : 'Se reactivará completamente.'}`;
    
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
        } else if (type === 'planta') {
          await suspenderPlanta(id, action);
          setPlantas(prev => prev.map(item => 
            item.planta_id === id ? { ...item, status: !currentStatus } : item
          ));
        } else if (type === 'departamento') {
          await suspenderDepartamento(id, action);
          setDepartamentos(prev => prev.map(item => 
            item.departamento_id === id ? { ...item, status: !currentStatus } : item
          ));
        } else if (type === 'puesto') {
          await suspenderPuesto(id, action);
          setPuestos(prev => prev.map(item => 
            item.puesto_id === id ? { ...item, status: !currentStatus } : item
          ));
        } else if (type === 'empleado') {
          await suspenderEmpleado(id, action);
          setEmpleados(prev => prev.map(item => 
            item.empleado_id === id ? { ...item, status: !currentStatus } : item
          ));
        } else if (type === 'plan') {
          const { cambiarEstadoPlan } = await import('../services/suscripcionService');
          await cambiarEstadoPlan(id, !currentStatus);
          setPlanes(prev => prev.map(item => 
            item.plan_id === id ? { ...item, status: !currentStatus } : item
          ));
        }
        
        alert(`${nombreItem} ${action === 'suspender' ? 'suspendido' : 'activado'} exitosamente`);
        
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
        } else if (type === 'planta') {
          await eliminarPlanta(id);
          setPlantas(prev => prev.filter(item => item.planta_id !== id));
        } else if (type === 'departamento') {
          await eliminarDepartamento(id);
          setDepartamentos(prev => prev.filter(item => item.departamento_id !== id));
        } else if (type === 'puesto') {
          await eliminarPuesto(id);
          setPuestos(prev => prev.filter(item => item.puesto_id !== id));
        } else if (type === 'empleado') {
          await eliminarEmpleado(id);
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
  const handleEdit = (type: string, item: any) => {
    let title = '';
    let data = {};

    switch (type) {
      case 'empresa':
        title = `Editar Empresa: ${item.nombre}`;
        data = {
          nombre: item.nombre,
          rfc: item.rfc,
          telefono: item.telefono || '',
          correo: item.correo || '',
          direccion: item.direccion || '',
          status: item.status
        };
        break;
      case 'usuario':
        title = `Editar Usuario: ${item.username}`;
        data = {
          username: item.username,
          email: item.email,
          nombre_completo: item.nombre_completo,
          nivel_usuario: item.nivel_usuario,
          is_active: item.is_active
        };
        break;
      case 'planta':
        title = `Editar Planta: ${item.nombre}`;
        data = {
          nombre: item.nombre,
          direccion: item.direccion || '',
          telefono: item.telefono || '',
          status: item.status
        };
        break;
      case 'departamento':
        title = `Editar Departamento: ${item.nombre}`;
        data = {
          nombre: item.nombre,
          descripcion: item.descripcion || '',
          status: item.status
        };
        break;
      case 'puesto':
        title = `Editar Puesto: ${item.nombre}`;
        data = {
          nombre: item.nombre,
          descripcion: item.descripcion || '',
          status: item.status
        };
        break;        case 'empleado':
          title = `Editar Empleado: ${item.nombre_completo}`;
          data = {
            nombre: item.nombre,
            apellido_paterno: item.apellido_paterno,
            apellido_materno: item.apellido_materno || '',
            telefono: item.telefono || '',
            correo: item.correo || '',
            fecha_ingreso: item.fecha_ingreso || '',
            status: item.status
          };
          break;
        case 'plan':
          title = `Editar Plan: ${item.nombre}`;
          data = {
            nombre: item.nombre,
            descripcion: item.descripcion || '',
            duracion: item.duracion,
            precio: item.precio,
            status: item.status
          };
          break;
    }

    setModalEditar({
      isOpen: true,
      type,
      id: item[`${type}_id`] || item.user_id,
      data,
      title
    });
  };

  // Función para guardar cambios
  const handleSaveEdit = async (formData: any) => {
    try {
      const { type, id } = modalEditar;
      
      switch (type) {
        case 'empresa':
          await editarEmpresa(id, formData);
          setEmpresas(prev => prev.map(item => 
            item.empresa_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'usuario':
          await editarUsuario(id, formData);
          setUsuarios(prev => prev.map(item => 
            item.user_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'planta':
          await editarPlanta(id, formData);
          setPlantas(prev => prev.map(item => 
            item.planta_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'departamento':
          await editarDepartamento(id, formData);
          setDepartamentos(prev => prev.map(item => 
            item.departamento_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'puesto':
          await editarPuesto(id, formData);
          setPuestos(prev => prev.map(item => 
            item.puesto_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'empleado':
          await editarEmpleado(id, formData);
          setEmpleados(prev => prev.map(item => 
            item.empleado_id === id ? { ...item, ...formData } : item
          ));
          break;
        case 'plan':
          const planData = {
            nombre: formData.nombre,
            descripcion: formData.descripcion,
            duracion: parseInt(formData.duracion),
            precio: parseFloat(formData.precio),
            status: formData.status !== false
          };
          await editarPlan(id, planData);
          setPlanes(prev => prev.map(item => 
            item.plan_id === id ? { ...item, ...planData } : item
          ));
          break;
      }
      
      alert('Cambios guardados exitosamente');
    } catch (error: any) {
      console.error('Error guardando cambios:', error);
      alert(error.message || 'Error al guardar los cambios');
      throw error; // Para que el modal no se cierre automáticamente
    }
  };

  // Función para crear nuevo plan
  const handleCrearPlan = async (formData: any) => {
    try {
      await crearPlan({
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        duracion: parseInt(formData.duracion),
        precio: parseFloat(formData.precio),
        status: formData.status !== false
      });
      
      // Recargar la lista de planes
      const planesData = await listarPlanes();
      setPlanes(planesData);
      
      alert('Plan creado exitosamente');
    } catch (error: any) {
      console.error('Error creando plan:', error);
      alert(error.message || 'Error al crear el plan');
      throw error;
    }
  };

  // Función para crear nueva suscripción
  const handleCrearSuscripcion = async (formData: any) => {
    try {
      const result = await crearSuscripcion(
        parseInt(formData.empresa_id),
        parseInt(formData.plan_id)
      );
      
      // Recargar la lista de suscripciones
      const suscripcionesData = await listarSuscripciones();
      setSuscripciones(suscripcionesData);
      
      alert(`Suscripción creada exitosamente. ID: ${result.suscripcion_id}`);
    } catch (error: any) {
      console.error('Error creando suscripción:', error);
      alert(error.message || 'Error al crear la suscripción');
      throw error;
    }
  };

  // Función para crear nuevo usuario SuperAdmin
  const handleCrearUsuario = async (formData: any) => {
    try {
      const { crearUsuario } = await import('../services/superAdminService');
      await crearUsuario({
        username: formData.username,
        email: formData.email,
        nombre: formData.nombre,
        apellido_paterno: formData.apellido_paterno,
        apellido_materno: formData.apellido_materno || '',
        password: formData.password || '1234',
        is_active: formData.is_active !== false
      });
      
      // Recargar la lista de usuarios
      const usuariosData = await getUsuarios({});
      setUsuarios(usuariosData.usuarios);
      
      alert(`Usuario SuperAdmin creado exitosamente.\nUsuario: ${formData.username}\nContraseña temporal: ${formData.password || '1234'}`);
    } catch (error: any) {
      console.error('Error creando usuario:', error);
      alert(error.message || 'Error al crear el usuario');
      throw error;
    }
  };

  // Función para renovar suscripción
  const handleRenovarSuscripcion = async (suscripcionId: number) => {
    if (window.confirm('¿Renovar la suscripción?')) {
      try {
        // Buscar la suscripción actual para obtener empresa_id y plan_id
        const suscripcionActual = suscripciones.find(s => s.suscripcion_id === suscripcionId);
        if (!suscripcionActual) {
          alert('Suscripción no encontrada');
          return;
        }
        
        const result = await renovarSuscripcion(suscripcionActual.empresa_id, suscripcionActual.plan_id);
        
        // Recargar la lista de suscripciones
        const suscripcionesData = await listarSuscripciones();
        setSuscripciones(suscripcionesData);
        
        alert(`Suscripción renovada exitosamente. Nueva fecha fin: ${result.fecha_fin}`);
      } catch (error: any) {
        console.error('Error renovando suscripción:', error);
        alert(error.message || 'Error al renovar la suscripción');
      }
    }
  };

  // Función para suspender suscripción
  const handleSuspenderSuscripcion = async (suscripcionId: number) => {
    if (window.confirm('¿Suspender la suscripción?')) {
      try {
        await suspenderSuscripcion(suscripcionId);
        
        // Recargar la lista de suscripciones
        const suscripcionesData = await listarSuscripciones();
        setSuscripciones(suscripcionesData);
        
        alert('Suscripción suspendida exitosamente');
      } catch (error: any) {
        console.error('Error suspendiendo suscripción:', error);
        alert(error.message || 'Error al suspender la suscripción');
      }
    }
  };

  // Función para reactivar suscripción
  const handleReactivarSuscripcion = async (suscripcionId: number) => {
    if (window.confirm('¿Reactivar la suscripción?')) {
      try {
        await reactivarSuscripcion(suscripcionId);
        
        // Recargar la lista de suscripciones
        const suscripcionesData = await listarSuscripciones();
        setSuscripciones(suscripcionesData);
        
        alert('Suscripción reactivada exitosamente');
      } catch (error: any) {
        console.error('Error reactivando suscripción:', error);
        alert(error.message || 'Error al reactivar la suscripción');
      }
    }
  };

  // Función para obtener campos del formulario según el tipo
  const getFormFields = (type: string) => {
    switch (type) {
      case 'empresa':
        return [
          { name: 'nombre', label: 'Nombre de la Empresa', type: 'text' as const, required: true },
          { name: 'rfc', label: 'RFC', type: 'text' as const, required: true },
          { name: 'telefono', label: 'Teléfono', type: 'text' as const },
          { name: 'correo', label: 'Correo', type: 'email' as const },
          { name: 'direccion', label: 'Dirección', type: 'textarea' as const },
          { name: 'status', label: 'Activa', type: 'checkbox' as const }
        ];
      case 'usuario':
        return [
          { name: 'username', label: 'Nombre de Usuario', type: 'text' as const, required: true },
          { name: 'email', label: 'Email', type: 'email' as const, required: true },
          { name: 'nombre_completo', label: 'Nombre Completo', type: 'text' as const, required: true },
          { 
            name: 'nivel_usuario', 
            label: 'Nivel de Usuario', 
            type: 'select' as const, 
            required: true,
            options: [
              { value: 'superadmin', label: '👑 Super Admin' },
              { value: 'admin_empresa', label: '🏢 Admin Empresa' },
              { value: 'admin_planta', label: '🏭 Admin Planta' },
              { value: 'empleado', label: '👤 Empleado' }
            ]
          },
          { name: 'is_active', label: 'Usuario Activo', type: 'checkbox' as const }
        ];
      case 'crear-usuario':
        return [
          { name: 'username', label: 'Nombre de Usuario', type: 'text' as const, required: true },
          { name: 'email', label: 'Email', type: 'email' as const, required: true },
          { name: 'nombre', label: 'Nombre', type: 'text' as const, required: true },
          { name: 'apellido_paterno', label: 'Apellido Paterno', type: 'text' as const, required: true },
          { name: 'apellido_materno', label: 'Apellido Materno', type: 'text' as const },
          { name: 'password', label: 'Contraseña Temporal', type: 'password' as const, placeholder: '1234 (por defecto)' },
          { name: 'is_active', label: 'Usuario Activo', type: 'checkbox' as const, defaultValue: true }
        ];
      case 'planta':
        return [
          { name: 'nombre', label: 'Nombre de la Planta', type: 'text' as const, required: true },
          { name: 'direccion', label: 'Dirección', type: 'textarea' as const },
          { name: 'telefono', label: 'Teléfono', type: 'text' as const },
          { name: 'status', label: 'Activa', type: 'checkbox' as const }
        ];
      case 'departamento':
        return [
          { name: 'nombre', label: 'Nombre del Departamento', type: 'text' as const, required: true },
          { name: 'descripcion', label: 'Descripción', type: 'textarea' as const },
          { name: 'status', label: 'Activo', type: 'checkbox' as const }
        ];
      case 'puesto':
        return [
          { name: 'nombre', label: 'Nombre del Puesto', type: 'text' as const, required: true },
          { name: 'descripcion', label: 'Descripción', type: 'textarea' as const },
          { name: 'status', label: 'Activo', type: 'checkbox' as const }
        ];
      case 'empleado':
        return [
          { name: 'nombre', label: 'Nombre', type: 'text' as const, required: true },
          { name: 'apellido_paterno', label: 'Apellido Paterno', type: 'text' as const, required: true },
          { name: 'apellido_materno', label: 'Apellido Materno', type: 'text' as const },
          { name: 'telefono', label: 'Teléfono', type: 'text' as const },
          { name: 'correo', label: 'Correo', type: 'email' as const },
          { name: 'fecha_ingreso', label: 'Fecha de Ingreso', type: 'text' as const },
          { name: 'status', label: 'Activo', type: 'checkbox' as const }
        ];
      case 'plan':
        return [
          { name: 'nombre', label: 'Nombre del Plan', type: 'text' as const, required: true },
          { name: 'descripcion', label: 'Descripción', type: 'textarea' as const },
          { name: 'duracion', label: 'Duración (días)', type: 'number' as const, required: true },
          { name: 'precio', label: 'Precio (MXN)', type: 'number' as const, required: true, step: 0.01 },
          { name: 'status', label: 'Activo', type: 'checkbox' as const }
        ];
      default:
        return [];
    }
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
            <option value="admin_empresa">Admin Empresa</option>
            <option value="admin_planta">Admin Planta</option>
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
            <h4>📋 Suscripciones</h4>
            <div className="stat-numbers">
              <span className="stat-main">{suscripciones?.length || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activas: {suscripciones?.filter(s => s.estado === 'activa' || s.estado === 'Activa').length || 0}</span>
              <span>⏰ Por vencer: {suscripciones?.filter(s => {
                const diasRestantes = Math.ceil((new Date(s.fecha_fin).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
                return diasRestantes <= 7 && diasRestantes >= 0;
              }).length || 0}</span>
              <span>❌ Vencidas: {suscripciones?.filter(s => {
                const diasRestantes = Math.ceil((new Date(s.fecha_fin).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
                return diasRestantes < 0;
              }).length || 0}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>💰 Pagos</h4>
            <div className="stat-numbers">
              <span className="stat-main">{pagos?.length || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Completados: {pagos?.filter(p => p.estado_pago === 'completado' || p.estado_pago === 'Completado').length || 0}</span>
              <span>⏳ Pendientes: {pagos?.filter(p => p.estado_pago === 'pendiente' || p.estado_pago === 'Pendiente').length || 0}</span>
              <span>❌ Fallidos: {pagos?.filter(p => p.estado_pago === 'fallido' || p.estado_pago === 'Fallido').length || 0}</span>
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
              <span>👑 Total Usuarios: {estadisticas.total_usuarios}</span>
              <span>✅ Usuarios Activos: {estadisticas.usuarios_activos}</span>
              <span>👤 Total Empleados: {estadisticas.total_empleados}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  // Render de tabla de empresas
  const renderEmpresas = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>🏢 Gestión de Empresas</h3>
        <div className="stats-mini">
          <span>Total: {empresas?.length || 0}</span>
          <span>Activas: {empresas?.filter(e => e.status).length || 0}</span>
          <span>Suspendidas: {empresas?.filter(e => !e.status).length || 0}</span>
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
            {empresas?.map((empresa) => (
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
                      onClick={() => handleEdit('empresa', empresa)}
                      className="btn-action primary"
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
        <div className="stats-mini">
          <span>Total: {usuarios?.length || 0}</span>
          <span>Activos: {usuarios?.filter(u => u.is_active).length || 0}</span>
          <span>Suspendidos: {usuarios?.filter(u => !u.is_active).length || 0}</span>
        </div>
        <div className="section-actions">
          <button 
            onClick={() => setModalCrearUsuario(true)}
            className="btn-primary"
          >
            ➕ Crear Usuario SuperAdmin
          </button>
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
            {usuarios?.map((usuario) => (
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
                    {usuario.nivel_usuario === 'admin_empresa' && '🏢 Admin Empresa'}
                    {usuario.nivel_usuario === 'admin_planta' && '🏭 Admin Planta'}
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
                      onClick={() => handleToggleStatus('usuario', usuario.user_id, usuario.is_active, usuario.nombre_completo)}
                      className={`btn-action ${usuario.is_active ? 'warning' : 'success'}`}
                    >
                      {usuario.is_active ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('usuario', usuario.user_id, usuario.nombre_completo)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleEdit('usuario', usuario)}
                      className="btn-action primary"
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

  // Render de tabla de plantas
  const renderPlantas = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>🏭 Gestión de Plantas</h3>
        <div className="stats-mini">
          <span>Total: {plantas?.length || 0}</span>
          <span>Activas: {plantas?.filter(p => p.status).length || 0}</span>
          <span>Suspendidas: {plantas?.filter(p => !p.status).length || 0}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Planta</th>
              <th>Empresa</th>
              <th>Administrador</th>
              <th>Departamentos</th>
              <th>Empleados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {plantas?.map((planta) => (
              <tr key={planta.planta_id}>
                <td>{planta.planta_id}</td>
                <td>
                  <div>
                    <strong>{planta.nombre}</strong>
                    {planta.direccion && <small>{planta.direccion}</small>}
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{planta.empresa_nombre}</strong>
                    <small>ID: {planta.empresa_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{planta.username || 'Sin usuario'}</strong>
                  </div>
                </td>
                <td>{planta.departamentos_count}</td>
                <td>{planta.empleados_count}</td>
                <td>
                  <span className={`status ${planta.status ? 'active' : 'inactive'}`}>
                    {planta.status ? '🟢 Activa' : '🔴 Suspendida'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('planta', planta.planta_id, planta.status, planta.nombre)}
                      className={`btn-action ${planta.status ? 'warning' : 'success'}`}
                    >
                      {planta.status ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('planta', planta.planta_id, planta.nombre)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleEdit('planta', planta)}
                      className="btn-action primary"
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
        <h3>🏢 Gestión de Departamentos</h3>
        <div className="stats-mini">
          <span>Total: {departamentos?.length || 0}</span>
          <span>Activos: {departamentos?.filter(d => d.status).length || 0}</span>
          <span>Suspendidos: {departamentos?.filter(d => !d.status).length || 0}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Departamento</th>
              <th>Planta</th>
              <th>Empresa</th>
              <th>Puestos</th>
              <th>Empleados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {departamentos?.map((departamento) => (
              <tr key={departamento.departamento_id}>
                <td>{departamento.departamento_id}</td>
                <td>
                  <div>
                    <strong>{departamento.nombre}</strong>
                    {departamento.descripcion && <small>{departamento.descripcion}</small>}
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{departamento.planta_nombre}</strong>
                    <small>ID: {departamento.planta_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{departamento.empresa_nombre}</strong>
                    <small>ID: {departamento.empresa_id}</small>
                  </div>
                </td>
                <td>{departamento.puestos_count}</td>
                <td>{departamento.empleados_count}</td>
                <td>
                  <span className={`status ${departamento.status ? 'active' : 'inactive'}`}>
                    {departamento.status ? '🟢 Activo' : '🔴 Suspendido'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('departamento', departamento.departamento_id, departamento.status, departamento.nombre)}
                      className={`btn-action ${departamento.status ? 'warning' : 'success'}`}
                    >
                      {departamento.status ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('departamento', departamento.departamento_id, departamento.nombre)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleEdit('departamento', departamento)}
                      className="btn-action primary"
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

  // Render de tabla de puestos
  const renderPuestos = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>💼 Gestión de Puestos</h3>
        <div className="stats-mini">
          <span>Total: {puestos?.length || 0}</span>
          <span>Activos: {puestos?.filter(p => p.status).length || 0}</span>
          <span>Suspendidos: {puestos?.filter(p => !p.status).length || 0}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Puesto</th>
              <th>Departamento</th>
              <th>Planta</th>
              <th>Empresa</th>
              <th>Empleados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {puestos?.map((puesto) => (
              <tr key={puesto.puesto_id}>
                <td>{puesto.puesto_id}</td>
                <td>
                  <div>
                    <strong>{puesto.nombre}</strong>
                    {puesto.descripcion && <small>{puesto.descripcion}</small>}
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{puesto.departamento_nombre}</strong>
                    <small>ID: {puesto.departamento_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{puesto.planta_nombre}</strong>
                    <small>ID: {puesto.planta_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{puesto.empresa_nombre}</strong>
                    <small>ID: {puesto.empresa_id}</small>
                  </div>
                </td>
                <td>{puesto.empleados_count}</td>
                <td>
                  <span className={`status ${puesto.status ? 'active' : 'inactive'}`}>
                    {puesto.status ? '🟢 Activo' : '🔴 Suspendido'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('puesto', puesto.puesto_id, puesto.status, puesto.nombre)}
                      className={`btn-action ${puesto.status ? 'warning' : 'success'}`}
                    >
                      {puesto.status ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('puesto', puesto.puesto_id, puesto.nombre)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleEdit('puesto', puesto)}
                      className="btn-action primary"
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
        <div className="stats-mini">
          <span>Total: {empleados?.length || 0}</span>
          <span>Activos: {empleados?.filter(e => e.status)?.length || 0}</span>
          <span>Suspendidos: {empleados?.filter(e => !e.status)?.length || 0}</span>
        </div>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empleado</th>
              <th>Número</th>
              <th>Puesto</th>
              <th>Departamento</th>
              <th>Planta</th>
              <th>Empresa</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados?.map((empleado) => (
              <tr key={empleado.empleado_id}>
                <td>{empleado.empleado_id}</td>
                <td>
                  <div>
                    <strong>{empleado.nombre_completo}</strong>
                    {empleado.correo && <small>{empleado.correo}</small>}
                  </div>
                </td>
                <td>{empleado.numero_empleado}</td>
                <td>
                  <div>
                    <strong>{empleado.puesto_nombre}</strong>
                    <small>ID: {empleado.puesto_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.departamento_nombre}</strong>
                    <small>ID: {empleado.departamento_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.planta_nombre}</strong>
                    <small>ID: {empleado.planta_id}</small>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.empresa_nombre}</strong>
                    <small>ID: {empleado.empresa_id}</small>
                  </div>
                </td>
                <td>
                  <span className={`status ${empleado.status ? 'active' : 'inactive'}`}>
                    {empleado.status ? '🟢 Activo' : '🔴 Suspendido'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleToggleStatus('empleado', empleado.empleado_id, empleado.status, empleado.nombre_completo)}
                      className={`btn-action ${empleado.status ? 'warning' : 'success'}`}
                    >
                      {empleado.status ? '⏸️ Suspender' : '▶️ Activar'}
                    </button>
                    <button 
                      onClick={() => handleDelete('empleado', empleado.empleado_id, empleado.nombre_completo)}
                      className="btn-action danger"
                    >
                      🗑️ Eliminar
                    </button>
                    <button 
                      onClick={() => handleEdit('empleado', empleado)}
                      className="btn-action primary"
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

  // Render de tabla de planes (RF-001)
  const renderPlanes = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>📋 Gestión de Planes de Suscripción</h3>
        <div className="stats-mini">
          <span>Total: {planes.length}</span>
          <span>Activos: {planes.filter(p => p.status).length}</span>
          <span>Inactivos: {planes.filter(p => !p.status).length}</span>
        </div>
        <button 
          onClick={() => setModalCrearPlan(true)}
          className="btn-primary"
        >
          ➕ Crear Nuevo Plan
        </button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Duración</th>
              <th>Precio</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {planes?.map((plan) => (
              <tr key={plan.plan_id}>
                <td>{plan.plan_id}</td>
                <td>
                  <div>
                    <strong>{plan.nombre}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    {plan.descripcion ? (
                      <small>{plan.descripcion.length > 100 ? 
                        `${plan.descripcion.substring(0, 100)}...` : 
                        plan.descripcion}
                      </small>
                    ) : (
                      <span className="text-muted">Sin descripción</span>
                    )}
                  </div>
                </td>
                <td>
                  <strong>{formatearDuracion(plan.duracion)}</strong>
                </td>
                <td>
                  <strong className="precio">{formatearPrecio(plan.precio)}</strong>
                </td>
                <td>
                  <span className={`status ${plan.status ? 'active' : 'inactive'}`}>
                    {plan.status ? '🟢 Activo' : '🔴 Inactivo'}
                  </span>
                </td>
                <td>
                  <div className="actions">
                    <button 
                      onClick={() => handleEdit('plan', plan)}
                      className="btn-action primary"
                      title="Editar plan"
                    >
                      ✏️ Editar
                    </button>
                    <button 
                      onClick={() => handleToggleStatus('plan', plan.plan_id, plan.status, plan.nombre)}
                      className={`btn-action ${plan.status ? 'warning' : 'success'}`}
                      title={plan.status ? 'Desactivar plan' : 'Activar plan'}
                    >
                      {plan.status ? '🚫 Desactivar' : '✅ Activar'}
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

  // Render de tabla de suscripciones (RF-003)
  const renderSuscripciones = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>💳 Gestión de Suscripciones</h3>
        <div className="stats-mini">
          <span>Total: {suscripciones?.length || 0}</span>
          <span>Activas: {suscripciones?.filter(s => s.estado === 'Activa').length || 0}</span>
          <span>Por vencer: {suscripciones?.filter(s => {
            const fechaFin = new Date(s.fecha_fin);
            const hoy = new Date();
            const diasRestantes = Math.ceil((fechaFin.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
            return s.estado === 'Activa' && diasRestantes <= 30 && diasRestantes > 0;
          }).length || 0}</span>
          <span>Vencidas: {suscripciones?.filter(s => s.estado !== 'Activa').length || 0}</span>
        </div>
        <button 
          onClick={() => setModalCrearSuscripcion(true)}
          className="btn-primary"
        >
          ➕ Crear Nueva Suscripción
        </button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>Plan</th>
              <th>Precio</th>
              <th>Fecha Fin</th>
              <th>Días Restantes</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {suscripciones?.map((suscripcion) => {
              const estadoColor = getEstadoSuscripcionColor(suscripcion.estado);
              const estadoTexto = getEstadoSuscripcionTexto(suscripcion.estado);
              
              // Calcular días restantes más precisamente
              const fechaFin = new Date(suscripcion.fecha_fin);
              const hoy = new Date();
              const diasRestantes = Math.ceil((fechaFin.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
              const estaVencida = diasRestantes < 0;
              const porVencer = diasRestantes <= 7 && diasRestantes >= 0;
              
              return (
                <tr key={suscripcion.suscripcion_id} className={estaVencida ? 'expired' : porVencer ? 'expiring' : ''}>
                  <td>{suscripcion.suscripcion_id}</td>
                  <td>
                    <div>
                      <strong>{suscripcion.empresa_nombre || `Empresa #${suscripcion.empresa_id}`}</strong>
                      <small>ID: {suscripcion.empresa_id}</small>
                    </div>
                  </td>
                  <td>
                    <div>
                      <strong>{suscripcion.plan_nombre || `Plan #${suscripcion.plan_id}`}</strong>
                      <small>{suscripcion.plan_duracion ? formatearDuracion(suscripcion.plan_duracion) : ''}</small>
                    </div>
                  </td>
                  <td>
                    <strong className="precio">{formatearPrecio(parseFloat(String(suscripcion.plan_precio || '0')))}</strong>
                  </td>
                  <td>
                    <div>
                      <strong>{fechaFin.toLocaleDateString()}</strong>
                      <small>Inicio: {new Date(suscripcion.fecha_inicio).toLocaleDateString()}</small>
                    </div>
                  </td>
                  <td>
                    <span className={`dias-restantes ${estaVencida ? 'expired' : porVencer ? 'warning' : 'active'}`}>
                      {estaVencida ? (
                        <span style={{ color: '#dc3545' }}>⚠️ Vencida hace {Math.abs(diasRestantes)} días</span>
                      ) : porVencer ? (
                        <span style={{ color: '#ffc107' }}>⏰ {diasRestantes} días (Pronto vence)</span>
                      ) : (
                        <span style={{ color: '#28a745' }}>✅ {diasRestantes} días</span>
                      )}
                    </span>
                  </td>
                  <td>
                    <span className={`status ${estadoColor}`}>
                      {estadoTexto}
                    </span>
                  </td>
                  <td>
                    <div className="actions">
                      {suscripcion.estado === 'Activa' && (
                        <button 
                          onClick={() => handleRenovarSuscripcion(suscripcion.suscripcion_id)}
                          className="btn-action success"
                          title="Renovar suscripción"
                        >
                          🔄 Renovar
                        </button>
                      )}
                      {suscripcion.estado === 'Activa' && (
                        <button 
                          onClick={() => handleSuspenderSuscripcion(suscripcion.suscripcion_id)}
                          className="btn-action warning"
                          title="Suspender suscripción"
                        >
                          ⏸️ Suspender
                        </button>
                      )}
                      {suscripcion.estado === 'Suspendida' && (
                        <button 
                          onClick={() => handleReactivarSuscripcion(suscripcion.suscripcion_id)}
                          className="btn-action primary"
                          title="Reactivar suscripción"
                        >
                          ⚡ Reactivar
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  // Render de tabla de pagos (RF-004)
  const renderPagos = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>💰 Gestión de Pagos</h3>
        <div className="stats-mini">
          <span>Total: {pagos?.length || 0}</span>
          <span>Completados: {pagos?.filter(p => p.estado_pago === 'Completado').length || 0}</span>
          <span>Pendientes: {pagos?.filter(p => p.estado_pago === 'Pendiente').length || 0}</span>
          <span>Fallidos: {pagos?.filter(p => p.estado_pago === 'Fallido').length || 0}</span>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>Plan</th>
              <th>Suscripción</th>
              <th>Monto</th>
              <th>Método de Pago</th>
              <th>Estado</th>
              <th>Fecha</th>
              <th>Referencia</th>
            </tr>
          </thead>
          <tbody>
            {pagos?.map((pago) => {
              const estadoTexto = getEstadoPagoTexto(pago.estado_pago);
              return (
                <tr key={pago.pago_id}>
                  <td>{pago.pago_id}</td>
                  <td>
                    <div>
                      <strong>{pago.empresa_nombre || `Empresa`}</strong>
                      <small>Suscripción: {pago.suscripcion_id}</small>
                    </div>
                  </td>
                  <td>
                    <div>
                      <strong>{pago.plan_nombre || `Plan`}</strong>
                    </div>
                  </td>
                  <td>
                    <div>
                      <span>ID: {pago.suscripcion_id}</span>
                    </div>
                  </td>
                  <td>
                    <strong className="precio">{formatearPrecio(pago.monto_pago)}</strong>
                  </td>
                  <td>
                    <span>{pago.transaccion_id || 'N/A'}</span>
                  </td>
                  <td>
                    <span className={`status ${pago.estado_pago === 'Completado' ? 'active' : pago.estado_pago === 'Pendiente' ? 'warning' : 'inactive'}`}>
                      {estadoTexto}
                    </span>
                  </td>
                  <td>
                    <div>
                      <strong>{new Date(pago.fecha_pago).toLocaleDateString()}</strong>
                      <small>{new Date(pago.fecha_pago).toLocaleTimeString()}</small>
                    </div>
                  </td>
                  <td>
                    <small className="referencia">{pago.transaccion_id || 'Sin ID'}</small>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  if (loading) {
    return <div className="loading">🔄 Cargando datos del sistema...</div>;
  }

  return (
    <div className="dashboard superadmin-dashboard">
      {/* Sidebar - Always visible */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>👑 AXYOMA</h2>
            <span className="sidebar-subtitle">Super Admin Panel</span>
          </div>
        </div>
          <nav className="sidebar-nav">
            <button 
              className={activeSection === 'estadisticas' ? 'active' : ''}
              onClick={() => setActiveSection('estadisticas')}
            >
              <span className="nav-icon">📊</span>
              <span className="nav-text">Estadísticas</span>
            </button>
            <button 
              className={activeSection === 'empresas' ? 'active' : ''}
              onClick={() => setActiveSection('empresas')}
            >
              <span className="nav-icon">🏢</span>
              <span className="nav-text">Empresas ({empresas?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'usuarios' ? 'active' : ''}
              onClick={() => setActiveSection('usuarios')}
            >
              <span className="nav-icon">👥</span>
              <span className="nav-text">Usuarios ({usuarios?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'plantas' ? 'active' : ''}
              onClick={() => setActiveSection('plantas')}
            >
              <span className="nav-icon">🏭</span>
              <span className="nav-text">Plantas ({plantas?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'departamentos' ? 'active' : ''}
              onClick={() => setActiveSection('departamentos')}
            >
              <span className="nav-icon">🏢</span>
              <span className="nav-text">Departamentos ({departamentos?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'puestos' ? 'active' : ''}
              onClick={() => setActiveSection('puestos')}
            >
              <span className="nav-icon">💼</span>
              <span className="nav-text">Puestos ({puestos?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'empleados' ? 'active' : ''}
              onClick={() => setActiveSection('empleados')}
            >
              <span className="nav-icon">👤</span>
              <span className="nav-text">Empleados ({empleados?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'suscripciones' ? 'active' : ''}
              onClick={() => setActiveSection('suscripciones')}
            >
              <span className="nav-icon">💳</span>
              <span className="nav-text">Suscripciones ({suscripciones?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'planes' ? 'active' : ''}
              onClick={() => setActiveSection('planes')}
            >
              <span className="nav-icon">📋</span>
              <span className="nav-text">Planes ({planes?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'pagos' ? 'active' : ''}
              onClick={() => setActiveSection('pagos')}
            >
              <span className="nav-icon">💰</span>
              <span className="nav-text">Pagos ({pagos?.length || 0})</span>
            </button>
            <button 
              className={activeSection === 'evaluaciones' ? 'active' : ''}
              onClick={() => setActiveSection('evaluaciones')}
            >
              <span className="nav-icon">📝</span>
              <span className="nav-text">Evaluaciones</span>
            </button>
        </nav>
      </aside>

      {/* Main content area */}
      <div className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="header-left">
            <h1>Panel de Super Administrador</h1>
            <p className="header-subtitle">Control total del sistema Axyoma</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar">
                <span className="avatar-icon">👤</span>
              </div>
              <div className="user-details">
                <span className="user-name">{userData?.nombre_completo || userData?.usuario}</span>
                <span className="user-role">{userData?.nivel_usuario}</span>
              </div>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <span className="logout-icon">🚪</span>
              Cerrar Sesión
            </button>
          </div>
        </header>

        {/* Content area */}
        <main className="dashboard-content">{activeSection === 'estadisticas' && renderEstadisticas()}
          {activeSection === 'empresas' && renderEmpresas()}
          {activeSection === 'usuarios' && renderUsuarios()}
          {activeSection === 'plantas' && renderPlantas()}
          {activeSection === 'departamentos' && renderDepartamentos()}
          {activeSection === 'puestos' && renderPuestos()}
          {activeSection === 'empleados' && renderEmpleados()}
          {activeSection === 'planes' && renderPlanes()}
          {activeSection === 'suscripciones' && renderSuscripciones()}
          {activeSection === 'pagos' && renderPagos()}
          {activeSection === 'evaluaciones' && <EvaluacionesGestion userData={{ nivel_usuario: 'superadmin' }} />}

      {modalEditar.isOpen && (
        <EditModal
          isOpen={modalEditar.isOpen}
          onClose={() => setModalEditar(prev => ({ ...prev, isOpen: false }))}
          title={modalEditar.title}
          initialData={modalEditar.data}
          onSave={handleSaveEdit}
          fields={getFormFields(modalEditar.type)}
        />
      )}

      {/* Modal para crear nuevo plan */}
      {modalCrearPlan && (
        <EditModal
          isOpen={modalCrearPlan}
          onClose={() => setModalCrearPlan(false)}
          title="📋 Crear Nuevo Plan de Suscripción"
          initialData={{
            nombre: '',
            descripcion: '',
            duracion: 30,
            precio: 0,
            status: true
          }}
          onSave={handleCrearPlan}
          fields={getFormFields('plan')}
        />
      )}

      {/* Modal para crear nueva suscripción */}
      {modalCrearSuscripcion && (
        <EditModal
          isOpen={modalCrearSuscripcion}
          onClose={() => setModalCrearSuscripcion(false)}
          title="💳 Crear Nueva Suscripción"
          initialData={{
            empresa_id: '',
            plan_id: ''
          }}
          onSave={handleCrearSuscripcion}
          fields={[
            { 
              name: 'empresa_id', 
              label: 'Empresa', 
              type: 'select' as const, 
              required: true,
              options: empresas.filter(empresa => empresa.status).map(empresa => ({
                value: empresa.empresa_id.toString(),
                label: `${empresa.nombre} (ID: ${empresa.empresa_id})`
              }))
            },
            { 
              name: 'plan_id', 
              label: 'Plan', 
              type: 'select' as const, 
              required: true,
              options: planes.filter(plan => plan.status).map(plan => ({
                value: plan.plan_id.toString(),
                label: `${plan.nombre} - ${formatearPrecio(plan.precio)}`
              }))
            }
          ]}
        />
      )}

      {/* Modal para crear nuevo usuario SuperAdmin */}
      {modalCrearUsuario && (
        <EditModal
          isOpen={modalCrearUsuario}
          onClose={() => setModalCrearUsuario(false)}
          title="👑 Crear Nuevo Usuario SuperAdmin"
          initialData={{
            username: '',
            email: '',
            nombre: '',
            apellido_paterno: '',
            apellido_materno: '',
            password: '1234',
            is_active: true
          }}
          onSave={handleCrearUsuario}
          fields={getFormFields('crear-usuario')}
        />
      )}
        </main>
      </div>
    </div>
  );
};

export default SuperAdminDashboard;
