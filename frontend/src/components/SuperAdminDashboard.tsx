import React, { useState, useEffect, useCallback } from 'react';
import { logout } from '../services/authService';
import EvaluacionesGestion from './EvaluacionesGestion';
import GestionBD from './GestionBD';
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
  suspenderPlan,
  editarEmpresa,
  editarUsuario,
  editarPlanta,
  editarDepartamento,
  editarPuesto,
  editarEmpleado,
  type Empresa, // Usar tipo Empresa en lugar de SuperAdminEmpresa
  type SuperAdminUsuario,
  type SuperAdminPlanta,
  type SuperAdminDepartamento,
  type SuperAdminPuesto,
  type SuperAdminEmpleado,
  type SuperAdminEstadisticas
} from '../services/superAdminService';
import {
  listarPlanes,
  listarPlanesAdmin,  // ← Nueva función para SuperAdmin
  listarSuscripciones,
  listarPagos,
  crearPlan,
  editarPlan,
  crearSuscripcion,
  renovarSuscripcion,
  suspenderSuscripcion,
  reactivarSuscripcion,
  getEstadoSuscripcionTexto,
  getEstadoSuscripcionColor,
  getEstadoPagoTexto,
  type PlanSuscripcion,
  type SuscripcionEmpresa,
  type Pago
} from '../services/suscripcionService';
import EditModal from './EditModal';
import '../css/SuperAdminDashboard.css';
import useDebounce from '../hooks/useDebounce';

interface SuperAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

// Definimos interfaces extendidas para los tipos de la API
interface EmpresaExtendida extends Empresa {
  // Ya tiene todo lo que necesitamos
}

// Interfaces para datos extendidos - usando any temporalmente para compilar
type UsuarioExtendido = any;
type PlantaExtendida = any;
type DepartamentoExtendido = any;
type PuestoExtendido = any;
type EmpleadoExtendido = any;

// Tipo legado para compatibilidad
interface EstadisticasLegadas {
  total_empresas: number;
  empresas_activas: number;
  total_usuarios: number;
  usuarios_activos: number;
  total_plantas: number;
  plantas_activas: number;
  total_empleados: number;
  empleados_activos: number;
  total_departamentos: number;
  departamentos_activos: number;
  total_puestos: number;
  puestos_activos: number;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'estadisticas' | 'empresas' | 'usuarios' | 'plantas' | 'departamentos' | 'puestos' | 'empleados' | 'suscripciones' | 'planes' | 'pagos' | 'evaluaciones' | 'gestion-bd'>('empresas');
  const [loading, setLoading] = useState(false);
  
  // Modificamos los estados para usar los tipos extendidos
  const [estadisticas, setEstadisticas] = useState<SuperAdminEstadisticas | null>(null);
  const [empresas, setEmpresas] = useState<EmpresaExtendida[]>([]);
  const [usuarios, setUsuarios] = useState<UsuarioExtendido[]>([]);
  const [plantas, setPlantas] = useState<PlantaExtendida[]>([]);
  const [departamentos, setDepartamentos] = useState<DepartamentoExtendido[]>([]);
  const [puestos, setPuestos] = useState<PuestoExtendido[]>([]);
  const [empleados, setEmpleados] = useState<EmpleadoExtendido[]>([]);
  const [suscripciones, setSuscripciones] = useState<SuscripcionEmpresa[]>([]);
  const [planes, setPlanes] = useState<PlanSuscripcion[]>([]);
  const [pagos, setPagos] = useState<Pago[]>([]); // Desactivado temporalmente
  
  // Estado para filtros
  const [filtroTexto, setFiltroTexto] = useState('');
  // Aplicar debounce al filtro de texto
  const debouncedFiltroTexto = useDebounce(filtroTexto, 500);
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

  // Funciones auxiliares para formateo
  const formatearDuracion = (dias: number) => {
    if (dias === 30) return "1 mes";
    if (dias === 90) return "3 meses";
    if (dias === 180) return "6 meses";
    if (dias === 365) return "1 año";
    return `${dias} días`;
  };

  const formatearPrecio = (precio: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(precio);
  };

  // Helper para obtener datos de estadísticas compatibles con nueva estructura
  const getStatsData = (): EstadisticasLegadas | null => {
    if (!estadisticas) return null;
    
    // Si es la nueva estructura
    if (estadisticas.dashboard) {
      return {
        total_empresas: estadisticas.dashboard.tarjetas_principales.empresas.total,
        empresas_activas: estadisticas.dashboard.tarjetas_principales.empresas.activas,
        total_usuarios: estadisticas.dashboard.tarjetas_principales.usuarios.total,
        usuarios_activos: estadisticas.dashboard.tarjetas_principales.usuarios.activos,
        total_plantas: estadisticas.dashboard.tarjetas_principales.plantas.total,
        plantas_activas: estadisticas.dashboard.tarjetas_principales.plantas.activas,
        total_empleados: estadisticas.dashboard.tarjetas_principales.empleados.total,
        empleados_activos: estadisticas.dashboard.tarjetas_principales.empleados.activos,
        total_departamentos: estadisticas.dashboard.estadisticas_detalladas.departamentos.total,
        departamentos_activos: estadisticas.dashboard.estadisticas_detalladas.departamentos.activos,
        total_puestos: estadisticas.dashboard.estadisticas_detalladas.puestos.total,
        puestos_activos: estadisticas.dashboard.estadisticas_detalladas.puestos.activos,
      };
    }
    
    // Si es la estructura antigua, devolverla tal como está
    return estadisticas as any;
  };

  const cargarEstadisticas = async () => {
    setLoading(true);
    try {
      console.log('🔄 SuperAdmin: Cargando estadísticas del sistema...');
      const estadisticasData = await getEstadisticasSistema();
      setEstadisticas(estadisticasData);
      console.log('✅ SuperAdmin: Estadísticas cargadas exitosamente:', estadisticasData);
    } catch (error) {
      console.error('❌ SuperAdmin: Error cargando estadísticas:', error);
      // Si falla, usar datos por defecto con estructura nueva
      setEstadisticas({
        dashboard: {
          tarjetas_principales: {
            empresas: { 
              total: 0, 
              activas: 0, 
              inactivas: 0, 
              porcentaje_activas: 0, 
              icono: "🏢", 
              color: "blue", 
              tendencia: "neutral" 
            },
            usuarios: { 
              total: 0, 
              activos: 0, 
              inactivos: 0, 
              porcentaje_activos: 0, 
              icono: "👥", 
              color: "green", 
              tendencia: "neutral" 
            },
            plantas: { 
              total: 0, 
              activas: 0, 
              inactivas: 0, 
              porcentaje_activas: 0, 
              icono: "🏭", 
              color: "orange", 
              tendencia: "neutral" 
            },
            empleados: { 
              total: 0, 
              activos: 0, 
              inactivos: 0, 
              porcentaje_activos: 0, 
              icono: "👤", 
              color: "purple", 
              tendencia: "neutral" 
            }
          },
          estadisticas_detalladas: {
            departamentos: { total: 0, activos: 0, inactivos: 0 },
            puestos: { total: 0, activos: 0, inactivos: 0 },
            estructura: {
              empresas_con_plantas: 0,
              plantas_con_departamentos: 0,
              departamentos_con_puestos: 0,
              promedio_plantas_por_empresa: 0,
              promedio_departamentos_por_planta: 0,
              promedio_empleados_por_departamento: 0
            }
          },
          distribucion_usuarios: {},
          alertas_sistema: {},
          salud_sistema: {}
        }
      } as any);
    } finally {
      setLoading(false);
    }
  };

  // Modificamos la función de carga de datos para adaptarla a los tipos
  const cargarDatosPorSeccion = useCallback(async () => {
    setLoading(true);
    try {
      console.log(`🔄 SuperAdmin: Cargando datos de ${activeSection}...`);
      
      const params: any = {};
      
      if (debouncedFiltroTexto) {  // Usar el valor con debounce aquí
        params.buscar = debouncedFiltroTexto;
      }
      
      if (filtroStatus !== 'all') {
        params.status = filtroStatus === 'active' ? 'true' : 'false';
      }
      
      switch (activeSection) {
        case 'empresas':
          console.log('🔄 SuperAdmin: Cargando empresas...');
          const empresasData = await getEmpresas(params.buscar, params.status);
          console.log('📊 SuperAdmin: Empresas cargadas:', empresasData?.length || 0);
          console.log('🔍 SuperAdmin: Estructura de datos de empresas:', empresasData?.[0]);
          console.log('🔎 SuperAdmin: Todos los datos de empresas:', empresasData);
          if (Array.isArray(empresasData)) {
            setEmpresas(empresasData);
            console.log('✅ SuperAdmin: Datos de empresas cargados exitosamente');
          } else {
            console.error('❌ SuperAdmin: datos de empresas no es un array:', empresasData);
            setEmpresas([]);
          }
          break;
          
        case 'usuarios':
          if (filtroNivelUsuario) {
            params.nivel_usuario = filtroNivelUsuario;
          }
          if (filtroStatus !== 'all') {
            params.activo = filtroStatus === 'active' ? 'true' : 'false';
            delete params.status;
          }
          // Convertir params a string para evitar el error TS2345
          const usuariosData = await getUsuarios(
            params.buscar || '',
            params.nivel_usuario || '',
            params.activo || ''
          );
          // Transformamos los datos para incluir propiedades adicionales
          const usuariosExtendidos: UsuarioExtendido[] = usuariosData.map((usuario: any) => ({
            ...usuario,
            nombre_completo: usuario.nombre + ' ' + usuario.apellido_paterno + (usuario.apellido_materno ? ' ' + usuario.apellido_materno : '')
          }));
          setUsuarios(usuariosExtendidos || []);
          break;
          
        case 'plantas':
          console.log('🔄 SuperAdmin: Cargando plantas...');
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          
          try {
            // Usar getPlantas en lugar de getEmpresas
            const plantasResponse = await getPlantas(params);
            console.log('📊 SuperAdmin: Respuesta plantas:', plantasResponse);
            
            // Verificar y procesar correctamente la respuesta según su estructura
            if (Array.isArray(plantasResponse)) {
              // Si la API devuelve directamente un array de plantas
              setPlantas(plantasResponse);
              console.log(`✅ SuperAdmin: Cargadas ${plantasResponse.length} plantas`);
            } else if (plantasResponse && (plantasResponse as any).plantas) {
              // Si la API devuelve un objeto con una propiedad 'plantas'
              setPlantas((plantasResponse as any).plantas);
              console.log(`✅ SuperAdmin: Cargadas ${(plantasResponse as any).plantas.length} plantas`);
            } else {
              // Si la respuesta tiene un formato inesperado
              console.error('❌ SuperAdmin: formato de respuesta de plantas incorrecto:', plantasResponse);
              setPlantas([]);
            }
          } catch (error) {
            console.error('❌ SuperAdmin: Error cargando plantas:', error);
            setPlantas([]);
          }
          break;
          
        case 'departamentos':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const departamentosData = await getDepartamentos(params);
          setDepartamentos(departamentosData);
          break;
          
        case 'puestos':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const puestosData = await getPuestos(params);
          setPuestos(puestosData);
          break;
          
        case 'empleados':
          if (filtroEmpresa) {
            params.empresa_id = filtroEmpresa;
          }
          const empleadosData = await getEmpleados(params);
          setEmpleados(empleadosData);
          break;
          
        case 'suscripciones':
          const suscripcionesData = await listarSuscripciones();
          setSuscripciones(suscripcionesData);
          break;
          
        case 'planes':
          const planesData = await listarPlanesAdmin();  // ← Usar función específica para SuperAdmin
          setPlanes(planesData);
          break;
          
        case 'pagos':
          const pagosData = await listarPagos();
          setPagos(pagosData);
          break;
      }
      
      console.log(`✅ SuperAdmin: Datos de ${activeSection} cargados exitosamente`);
    } catch (error) {
      console.error(`❌ SuperAdmin: Error cargando ${activeSection}:`, error);
      alert(`Error al cargar ${activeSection}`);
    } finally {
      setLoading(false);
    }
  }, [activeSection, debouncedFiltroTexto, filtroStatus, filtroNivelUsuario, filtroEmpresa]);

  useEffect(() => {
    cargarEstadisticas();
  }, []);

  // Nuevo efecto para limpiar filtros cuando cambia la sección activa
  useEffect(() => {
    // Limpiar todos los filtros al cambiar de sección
    setFiltroTexto('');
    setFiltroStatus('all');
    setFiltroNivelUsuario('');
    setFiltroEmpresa('');
    
    // Log para verificar que se están limpiando los filtros
    console.log(`🧹 Limpiando filtros al cambiar a sección: ${activeSection}`);
  }, [activeSection]); // Este efecto solo se ejecutará cuando cambie activeSection
  
  // Dejamos el useEffect original que carga datos cuando cambia la sección
  useEffect(() => {
    if (activeSection !== 'estadisticas') {
      cargarDatosPorSeccion();
    }
  }, [activeSection, cargarDatosPorSeccion]);

  // Agregar log para monitorear el estado de empresas
  useEffect(() => {
    console.log('🔎 SuperAdmin: Estado empresas actualizado:', empresas?.length || 0, 'empresas');
    if (empresas?.length > 0) {
      console.log('📋 SuperAdmin: Datos primer empresa:', {
        id: empresas[0].empresa_id,
        nombre: empresas[0].nombre,
        correo: empresas[0].correo,
        telefono: empresas[0].telefono,
        direccion: empresas[0].direccion,
        plantas_count: empresas[0].plantas_count
      });
    }
  }, [empresas]);

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
          await suspenderPlan(id, action);
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
          setPlantas(prev => prev.map((item) => 
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
      const planesData = await listarPlanesAdmin();  // ← Usar función específica para SuperAdmin
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
        profile_id: 0, // Se asignará automáticamente
        username: formData.username,
        email: formData.email,
        nombre_completo: `${formData.nombre} ${formData.apellido_paterno} ${formData.apellido_materno || ''}`.trim(),
        correo: formData.email,
        password: formData.password || '1234',
        is_active: formData.is_active !== false,
        nivel_usuario: 'superadmin',
        fecha_registro: new Date().toISOString(),
        ultimo_login: null,
        empresa: null,
        planta: null
      });
      
      // Recargar la lista de usuarios - corregimos la llamada
      const usuariosData = await getUsuarios('', '', '');
      
      // Transformamos los datos para incluir nombre_completo
      const usuariosExtendidos: UsuarioExtendido[] = usuariosData.map((usuario: any) => ({
        ...usuario,
        nombre_completo: usuario.nombre + ' ' + usuario.apellido_paterno + (usuario.apellido_materno ? ' ' + usuario.apellido_materno : '')
      }));
      
      setUsuarios(usuariosExtendidos || []);
      
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
          onChange={(e) => {
            e.preventDefault(); // Prevenir comportamiento predeterminado
            setFiltroTexto(e.target.value);
          }}
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
              <span className="stat-main">{getStatsData()?.total_empresas || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activas: {getStatsData()?.empresas_activas || 0}</span>
              <span>❌ Suspendidas: {(getStatsData()?.total_empresas || 0) - (getStatsData()?.empresas_activas || 0)}</span>
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
              <span className="stat-main">{getStatsData()?.total_plantas || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activas: {getStatsData()?.plantas_activas || 0}</span>
              <span>❌ Suspendidas: {(getStatsData()?.total_plantas || 0) - (getStatsData()?.plantas_activas || 0)}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>🏢 Departamentos</h4>
            <div className="stat-numbers">
              <span className="stat-main">{getStatsData()?.total_departamentos || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {getStatsData()?.departamentos_activos || 0}</span>
              <span>❌ Suspendidos: {(getStatsData()?.total_departamentos || 0) - (getStatsData()?.departamentos_activos || 0)}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>💼 Puestos</h4>
            <div className="stat-numbers">
              <span className="stat-main">{getStatsData()?.total_puestos || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {getStatsData()?.puestos_activos || 0}</span>
              <span>❌ Suspendidos: {(getStatsData()?.total_puestos || 0) - (getStatsData()?.puestos_activos || 0)}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>👤 Empleados</h4>
            <div className="stat-numbers">
              <span className="stat-main">{getStatsData()?.total_empleados || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>✅ Activos: {getStatsData()?.empleados_activos || 0}</span>
              <span>❌ Suspendidos: {(getStatsData()?.total_empleados || 0) - (getStatsData()?.empleados_activos || 0)}</span>
            </div>
          </div>
          
          <div className="stat-card">
            <h4>👥 Usuarios</h4>
            <div className="stat-numbers">
              <span className="stat-main">{getStatsData()?.total_usuarios || 0}</span>
              <span className="stat-detail">Total</span>
            </div>
            <div className="stat-breakdown">
              <span>👑 Total Usuarios: {getStatsData()?.total_usuarios || 0}</span>
              <span>✅ Usuarios Activos: {getStatsData()?.usuarios_activos || 0}</span>
              <span>👤 Total Empleados: {getStatsData()?.total_empleados || 0}</span>
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
        <h2>🏢 Gestión de Empresas</h2>
        <div className="stats-mini" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px',
          marginBottom: '20px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{empresas?.length || 0}</div>
            <div style={{ fontSize: '0.8rem' }}>Total Empresas</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>
              {empresas?.filter(e => e.status).length || 0}
            </div>
            <div style={{ fontSize: '0.8rem' }}>Activas</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
            color: '#333',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>
              {empresas?.filter(e => !e.status).length || 0}
            </div>
            <div style={{ fontSize: '0.8rem' }}>Suspendidas</div>
          </div>
        </div>
        <button className="btn-primary" onClick={() => cargarDatosPorSeccion()}>
          🔄 Recargar Datos
        </button>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        {loading ? (
          <div className="loading">Cargando empresas...</div>
        ) : empresas.length > 0 ? (
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Empresa</th>
                <th>RFC</th>
                <th>Contacto</th>
                <th>Ubicación</th>
                <th>Plantas</th>
                <th>Fecha Registro</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {empresas.map((empresa) => (
                <tr key={empresa.empresa_id}>
                  <td>
                    <div style={{
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      color: 'white',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      fontWeight: 'bold',
                      textAlign: 'center',
                      minWidth: '50px'
                    }}>
                      #{empresa.empresa_id}
                    </div>
                  </td>
                  <td>
                    <div>
                      <strong style={{ fontSize: '1.1rem', color: '#333' }}>{empresa.nombre}</strong>
                      <div style={{ 
                        marginTop: '4px',
                        fontSize: '0.85rem',
                        color: '#666',
                        fontWeight: 'normal'
                      }}>
                        🏢 {empresa.nombre?.length > 25 ? empresa.nombre.substring(0, 25) + '...' : empresa.nombre}
                      </div>
                    </div>
                  </td>
                  <td>
                    <div style={{
                      background: '#f8f9fa',
                      padding: '8px 12px',
                      borderRadius: '6px',
                      border: '1px solid #e9ecef',
                      fontFamily: 'monospace',
                      fontWeight: 'bold',
                      fontSize: '0.9rem'
                    }}>
                      {empresa.rfc || 'Sin RFC'}
                    </div>
                  </td>
                  <td>
                    <div style={{ lineHeight: '1.4' }}>
                      {empresa.correo && empresa.correo.trim() && (
                        <div style={{ marginBottom: '4px' }}>
                          <span style={{ fontSize: '0.8rem', color: '#666' }}>📧</span>
                          <span style={{ fontSize: '0.85rem', marginLeft: '4px' }}>
                            {empresa.correo.length > 20 ? empresa.correo.substring(0, 20) + '...' : empresa.correo}
                          </span>
                        </div>
                      )}
                      {empresa.telefono && empresa.telefono.trim() && (
                        <div>
                          <span style={{ fontSize: '0.8rem', color: '#666' }}>📞</span>
                          <span style={{ fontSize: '0.85rem', marginLeft: '4px' }}>{empresa.telefono}</span>
                        </div>
                      )}
                      {(!empresa.correo || !empresa.correo.trim()) && (!empresa.telefono || !empresa.telefono.trim()) && (
                        <span style={{ fontSize: '0.8rem', color: '#999', fontStyle: 'italic' }}>Sin contacto</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div style={{ lineHeight: '1.4' }}>
                      {empresa.direccion && empresa.direccion.trim() ? (
                        <div>
                          <span style={{ fontSize: '0.8rem', color: '#666' }}>📍</span>
                          <span style={{ fontSize: '0.85rem', marginLeft: '4px' }}>
                            {empresa.direccion.length > 30 ? empresa.direccion.substring(0, 30) + '...' : empresa.direccion}
                          </span>
                        </div>
                      ) : (
                        <span style={{ fontSize: '0.8rem', color: '#999', fontStyle: 'italic' }}>Sin dirección</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div style={{
                      background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
                      color: 'white',
                      padding: '8px 12px',
                      borderRadius: '20px',
                      textAlign: 'center',
                      fontWeight: 'bold',
                      minWidth: '60px'
                    }}>
                      🏭 {empresa.plantas_count || 0}
                    </div>
                  </td>
                  <td>
                    <div style={{ lineHeight: '1.4' }}>
                      {empresa.fecha_registro && empresa.fecha_registro !== null && typeof empresa.fecha_registro === 'string' && empresa.fecha_registro.trim() ? (
                        <div>
                          <div style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
                            {new Date(empresa.fecha_registro).toLocaleDateString()}
                          </div>
                          <div style={{ fontSize: '0.8rem', color: '#666' }}>
                            {Math.floor((new Date().getTime() - new Date(empresa.fecha_registro).getTime()) / (1000 * 60 * 60 * 24))} días
                          </div>
                        </div>
                      ) : (
                        <span style={{ fontSize: '0.8rem', color: '#999', fontStyle: 'italic' }}>📅 Sin fecha</span>
                      )}
                    </div>
                  </td>
                  <td>
                    <div style={{
                      display: 'inline-block',
                      padding: '8px 16px',
                      borderRadius: '20px',
                      fontWeight: 'bold',
                      fontSize: '0.9rem',
                      background: empresa.status ? '#e8f5e8' : '#ffebee',
                      color: empresa.status ? '#2e7d32' : '#d32f2f',
                      border: `2px solid ${empresa.status ? '#2e7d32' : '#d32f2f'}`,
                      textAlign: 'center',
                      minWidth: '100px'
                    }}>
                      {empresa.status ? '✅ ACTIVA' : '❌ SUSPENDIDA'}
                    </div>
                  </td>
                  <td>
                    <div className="action-buttons" style={{
                      display: 'flex',
                      gap: '8px',
                      justifyContent: 'center'
                    }}>
                      <button 
                        onClick={() => handleEdit('empresa', empresa)}
                        style={{
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          color: 'white',
                          border: 'none',
                          padding: '8px 12px',
                          borderRadius: '6px',
                          fontSize: '0.85rem',
                          fontWeight: 'bold',
                          cursor: 'pointer'
                        }}
                      >
                        ✏️ Editar
                      </button>
                      <button 
                        onClick={() => handleToggleStatus('empresa', empresa.empresa_id, empresa.status, empresa.nombre)}
                        style={{
                          background: empresa.status ? 
                            'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)' : 
                            'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
                          color: empresa.status ? '#333' : 'white',
                          border: 'none',
                          padding: '8px 12px',
                          borderRadius: '6px',
                          fontSize: '0.85rem',
                          fontWeight: 'bold',
                          cursor: 'pointer'
                        }}
                      >
                        {empresa.status ? "⏸️ Suspender" : "▶️ Activar"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="no-data">No se encontraron empresas. {debouncedFiltroTexto ? "Intente con otros filtros." : ""}</div>
        )}
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
                <td>{usuario.nombre_completo || `${usuario.nombre} ${usuario.apellido_paterno}`}</td>
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
                <td>{usuario.fecha_registro ? new Date(usuario.fecha_registro).toLocaleDateString() : 'N/A'}</td>
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
        <h2>Gestión de Plantas</h2>
        <button className="btn-primary" onClick={() => cargarDatosPorSeccion()}>
          🔄 Recargar Datos
        </button>
      </div>
      
      {renderFiltros()}

      <div className="table-container">
        {loading ? (
          <div className="loading">Cargando plantas...</div>
        ) : plantas.length > 0 ? (
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Empresa</th>
                <th>Dirección</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {plantas.map((planta) => (
                <tr key={planta.planta_id}>
                  <td>{planta.planta_id}</td>
                  <td>{planta.nombre}</td>
                  <td>{planta.empresa_nombre || (planta.empresa_nombre && planta.empresa_nombre) || "—"}</td>
                  <td>{planta.direccion || "—"}</td>
                  <td>
                    <span className={planta.status ? "status active" : "status inactive"}>
                      {planta.status ? "Activa" : "Suspendida"}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button onClick={() => handleEdit('planta', planta)}>
                        ✏️ Editar
                      </button>
                      <button onClick={() => handleToggleStatus('planta', planta.planta_id, planta.status, planta.nombre)}>
                        {planta.status ? "⏸️ Suspender" : "▶️ Activar"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="no-data">No se encontraron plantas. {debouncedFiltroTexto ? "Intente con otros filtros." : ""}</div>
        )}
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
                    <strong>{departamento.planta?.nombre || "Sin planta"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{departamento.empresa?.nombre || "Sin empresa"}</strong>
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
                    <strong>{puesto.departamento?.nombre || "Sin departamento"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{puesto.planta?.nombre || "Sin planta"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{puesto.empresa?.nombre || "Sin empresa"}</strong>
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
                    <strong>{empleado.puesto?.nombre || "Sin puesto"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.departamento?.nombre || "Sin departamento"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.planta?.nombre || "Sin planta"}</strong>
                  </div>
                </td>
                <td>
                  <div>
                    <strong>{empleado.empresa?.nombre || "Sin empresa"}</strong>
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
        <div className="stats-mini" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px',
          marginBottom: '20px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{planes.length}</div>
            <div style={{ fontSize: '0.8rem' }}>Total Planes</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{planes.filter(p => p.status).length}</div>
            <div style={{ fontSize: '0.8rem' }}>✅ Activos</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
            color: '#333',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{planes.filter(p => !p.status).length}</div>
            <div style={{ fontSize: '0.8rem' }}>❌ Inactivos</div>
          </div>
        </div>
        <button 
          onClick={() => setModalCrearPlan(true)}
          className="btn-primary"
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: 'bold'
          }}
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
        <h3>💳 Empresas con Suscripciones Activas</h3>
        <div className="stats-mini" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
          gap: '10px',
          marginBottom: '20px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{suscripciones?.length || 0}</div>
            <div style={{ fontSize: '0.8rem' }}>Total</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{suscripciones?.filter(s => s.estado === 'Activa').length || 0}</div>
            <div style={{ fontSize: '0.8rem' }}>✅ Activas</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            color: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{suscripciones?.filter(s => {
              const fechaFin = new Date(s.fecha_fin);
              const hoy = new Date();
              const diasRestantes = Math.ceil((fechaFin.getTime() - hoy.getTime()) / (1000 * 60 * 60 * 24));
              return s.estado === 'Activa' && diasRestantes <= 30 && diasRestantes > 0;
            }).length || 0}</div>
            <div style={{ fontSize: '0.8rem' }}>⏰ Por Vencer</div>
          </div>
          <div style={{
            background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
            color: '#333',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{suscripciones?.filter(s => s.estado !== 'Activa').length || 0}</div>
            <div style={{ fontSize: '0.8rem' }}>❌ Vencidas</div>
          </div>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Empresa</th>
              <th>Plan</th>
              <th>Precio</th>
              <th>Fecha Inicio</th>
              <th>Fecha Fin</th>
              <th>Días Restantes</th>
              <th>Estado</th>
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
                    <strong>{new Date(suscripcion.fecha_inicio).toLocaleDateString()}</strong>
                  </td>
                  <td>
                    <strong>{fechaFin.toLocaleDateString()}</strong>
                  </td>
                  <td>
                    <div style={{
                      display: 'inline-block',
                      padding: '8px 16px',
                      borderRadius: '20px',
                      fontWeight: 'bold',
                      fontSize: '0.9rem',
                      background: estaVencida ? '#ffebee' : porVencer ? '#fff3e0' : '#e8f5e8',
                      color: estaVencida ? '#d32f2f' : porVencer ? '#f57c00' : '#2e7d32',
                      border: `2px solid ${estaVencida ? '#d32f2f' : porVencer ? '#f57c00' : '#2e7d32'}`,
                      textAlign: 'center',
                      minWidth: '120px'
                    }}>
                      {estaVencida ? (
                        <div>
                          <div>⚠️ VENCIDA</div>
                          <div style={{ fontSize: '0.8rem' }}>hace {Math.abs(diasRestantes)} días</div>
                        </div>
                      ) : porVencer ? (
                        <div>
                          <div>⏰ {diasRestantes} DÍAS</div>
                          <div style={{ fontSize: '0.8rem' }}>¡Por vencer!</div>
                        </div>
                      ) : (
                        <div>
                          <div>✅ {diasRestantes} DÍAS</div>
                          <div style={{ fontSize: '0.8rem' }}>Activa</div>
                        </div>
                      )}
                    </div>
                  </td>
                  <td>
                    <span className={`status ${estadoColor}`}>
                      {estadoTexto}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  // Render de tabla de pagos (RF-004) - Desactivado temporalmente
  /*
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
  */

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
              <span className="nav-text">Empresas</span>
            </button>
            <button 
              className={activeSection === 'usuarios' ? 'active' : ''}
              onClick={() => setActiveSection('usuarios')}
            >
              <span className="nav-icon">👥</span>
              <span className="nav-text">Usuarios</span>
            </button>
            <button 
              className={activeSection === 'plantas' ? 'active' : ''}
              onClick={() => setActiveSection('plantas')}
            >
              <span className="nav-icon">🏭</span>
              <span className="nav-text">Plantas</span>
            </button>
            <button 
              className={activeSection === 'departamentos' ? 'active' : ''}
              onClick={() => setActiveSection('departamentos')}
            >
              <span className="nav-icon">🏢</span>
              <span className="nav-text">Departamentos</span>
            </button>
            <button 
              className={activeSection === 'puestos' ? 'active' : ''}
              onClick={() => setActiveSection('puestos')}
            >
              <span className="nav-icon">💼</span>
              <span className="nav-text">Puestos</span>
            </button>
            <button 
              className={activeSection === 'empleados' ? 'active' : ''}
              onClick={() => setActiveSection('empleados')}
            >
              <span className="nav-icon">👤</span>
              <span className="nav-text">Empleados</span>
            </button>
            <button 
              className={activeSection === 'suscripciones' ? 'active' : ''}
              onClick={() => setActiveSection('suscripciones')}
            >
              <span className="nav-icon">💳</span>
              <span className="nav-text">Suscripciones</span>
            </button>
            <button 
              className={activeSection === 'planes' ? 'active' : ''}
              onClick={() => setActiveSection('planes')}
            >
              <span className="nav-icon">📋</span>
              <span className="nav-text">Planes</span>
            </button>
            {/* <button 
              className={activeSection === 'pagos' ? 'active' : ''}
              onClick={() => setActiveSection('pagos')}
            >
              <span className="nav-icon">💰</span>
              <span className="nav-text">Pagos</span>
            </button> */}
            <button 
              className={activeSection === 'evaluaciones' ? 'active' : ''}
              onClick={() => setActiveSection('evaluaciones')}
            >
              <span className="nav-icon">📝</span>
              <span className="nav-text">Evaluaciones</span>
            </button>
            <button 
              className={activeSection === 'gestion-bd' ? 'active' : ''}
              onClick={() => setActiveSection('gestion-bd')}
            >
              <span className="nav-icon">🗄️</span>
              <span className="nav-text">Gestión BD</span>
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
        <main className="dashboard-content">
          {activeSection === 'estadisticas' && renderEstadisticas()}
          {activeSection === 'empresas' && renderEmpresas()}
          {activeSection === 'usuarios' && renderUsuarios()}
          {activeSection === 'plantas' && renderPlantas()}
          {activeSection === 'departamentos' && renderDepartamentos()}
          {activeSection === 'puestos' && renderPuestos()}
          {activeSection === 'empleados' && renderEmpleados()}
          {activeSection === 'planes' && renderPlanes()}
          {activeSection === 'suscripciones' && renderSuscripciones()}
          {/* {activeSection === 'pagos' && renderPagos()} // Desactivado temporalmente */}
          {activeSection === 'evaluaciones' && <EvaluacionesGestion userData={{ nivel_usuario: 'superadmin' }} />}
          {activeSection === 'gestion-bd' && <GestionBD />}
        </main>
      </div>

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
    </div>
  );
};

export default SuperAdminDashboard;