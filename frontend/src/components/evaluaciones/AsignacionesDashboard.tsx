
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import evaluacionesAPI, { Evaluacion, Asignacion, AsignacionEmpleado, AsignacionRequest } from '../../services/evaluacionesService';
import api from '../../api'; // Asume que este es tu cliente Axios configurado
import './AsignacionesDashboard.css'; // Estilos para esta página


// --- Interfaces de Datos ---
interface UserData {
    usuario: string;
    user_id?: number;
    nivel_usuario: string;
    empresa_id?: number;
    nombre_empresa?: string;
    planta_id?: number;
}

interface Empleado {
    empleado_id: number;
    nombre: string;
    apellido_paterno: string;
    apellido_materno?: string; // Opcional según tu ejemplo
    email?: string;
    telefono?: string;
    fecha_ingreso?: string;
    status?: boolean;
    // Propiedad calculada para mostrar en la UI
    nombre_completo: string;
    planta_id?: number;
    planta_nombre?: string;
    puesto_id?: number;
    puesto_nombre?: string;
    departamento_id?: number;
    departamento_nombre?: string;
    empresa_id?: number;
    empresa_nombre?: string;
}

interface Planta {
    planta_id: number;
    nombre: string;
    empresa_id?: number; // Agregado para permitir el filtrado directo por empresa
}
interface Puesto {
    puesto_id: number;
    nombre: string;
    departamento_id?: number; // Asegurarse de que el puesto tenga el ID de departamento
}
interface Departamento {
    departamento_id: number;
    nombre: string;
    planta_id?: number; // Asegurarse de que el departamento tenga el ID de planta
}

// --- Props del Componente ---
interface AsignacionesDashboardProps {
    userData: UserData;
}

const AsignacionesDashboard: React.FC<AsignacionesDashboardProps> = ({ userData }) => {
    const [evaluaciones, setEvaluaciones] = useState<Evaluacion[]>([]);
    const [selectedEvaluacion, setSelectedEvaluacion] = useState<Evaluacion | null>(null);
    const [asignacionesBase, setAsignacionesBase] = useState<Asignacion[]>([]);
    const [loadingEvaluaciones, setLoadingEvaluaciones] = useState(true);
    const [loadingAsignaciones, setLoadingAsignaciones] = useState(false);
    const [loadingEmpleadosAndFilters, setLoadingEmpleadosAndFilters] = useState(true);

    // Estados para el formulario de CREAR ASIGNACIÓN BASE
    const [showCreateAsignacionForm, setShowCreateAsignacionForm] = useState(false);
    const [newAsignacionEvaluacionId, setNewAsignacionEvaluacionId] = useState<number | null>(null);
    const [newAsignacionFechaInicio, setNewAsignacionFechaInicio] = useState('');
    const [newAsignacionFechaFin, setNewAsignacionFechaFin] = useState('');

    // Estados para el formulario de ASIGNAR MÁS EMPLEADOS
    // allEmployeesFetched: Contiene todos los empleados obtenidos de la API, sin filtros por rol.
    // employeesVisibleByRole: Contiene los empleados filtrados por el rol del usuario (admin-planta, admin-empresa).
    const [allEmployeesFetched, setAllEmployeesFetched] = useState<Empleado[]>([]);
    const [employeesVisibleByRole, setEmployeesVisibleByRole] = useState<Empleado[]>([]);
    const [plantas, setPlantas] = useState<Planta[]>([]);
    const [puestos, setPuestos] = useState<Puesto[]>([]);
    const [departamentos, setDepartamentos] = useState<Departamento[]>([]);

    const [searchTerm, setSearchTerm] = useState('');
    const [filterPlantaId, setFilterPlantaId] = useState<number | null>(null);
    const [filterPuestoId, setFilterPuestoId] = useState<number | null>(null);
    const [filterDepartamentoId, setFilterDepartamentoId] = useState<number | null>(null);
    const [selectedEmployeesForNewAssignment, setSelectedEmployeesForNewAssignment] = useState<number[]>([]);

    // Nuevo estado para controlar el tipo de asignación (individual, por planta, puesto, departamento)
    const [assignmentTargetType, setAssignmentTargetType] = useState<'employees' | 'plant' | 'puesto' | 'departamento'>('employees');
    const [selectedTargetId, setSelectedTargetId] = useState<number | null>(null); // Para planta_id, puesto_id, departamento_id

    const [showAssignFormForAsignacionId, setShowAssignFormForAsignacionId] = useState<number | null>(null);

    // ---------------------------------------------------------------------- //

    const [now, setNow] = useState('');

    useEffect(() => {
    const fecha = new Date();
    fecha.setSeconds(0, 0);
    setNow(fecha.toISOString().slice(0, 16));
    }, []);

    // Función para obtener asignaciones de la evaluación seleccionada
    const fetchAsignacionesForSelectedEvaluacion = useCallback(async () => {
        if (!selectedEvaluacion) {
            setAsignacionesBase([]);
            return;
        }
        setLoadingAsignaciones(true);
        try {
            const response = await evaluacionesAPI.getAsignaciones();
            let filteredAsignaciones = response.data.filter(a => a.evaluacion === selectedEvaluacion.evaluacion_id);

            // Filtrar por planta si es admin-planta
            if (userData.nivel_usuario === 'admin-planta' && userData.planta_id) {
                filteredAsignaciones = filteredAsignaciones.filter(asignacion =>
                    asignacion.asignaciones_empleado.some(ae =>
                        ae.empleado_planta_id === userData.planta_id
                    )
                );
            }

            filteredAsignaciones.sort((a, b) => new Date(b.fecha_inicio).getTime() - new Date(a.fecha_inicio).getTime());
            setAsignacionesBase(filteredAsignaciones);
        } catch (error) {
            alert('Error al obtener asignaciones para la evaluación seleccionada.');
            console.error('Error al obtener asignaciones para la evaluación seleccionada:', error);
        } finally {
            setLoadingAsignaciones(false);
        }
    }, [selectedEvaluacion, userData.nivel_usuario, userData.planta_id]);

    // Función para obtener evaluaciones iniciales
    useEffect(() => {
        const fetchInitialEvaluaciones = async () => {
            setLoadingEvaluaciones(true);
            try {
                const response = await evaluacionesAPI.getEvaluaciones();
                const allEvaluaciones = response.data;

                const filtered = allEvaluaciones.filter(evaluacion => {
                    if (userData.nivel_usuario === 'superadmin') {
                        return evaluacion.tipo_evaluacion === 'Normativa';
                    }
                    if (userData.nivel_usuario === 'admin-empresa' || userData.nivel_usuario === 'admin-planta') {
                        return (
                            evaluacion.tipo_evaluacion === 'Normativa' ||
                            (evaluacion.tipo_evaluacion === 'Interna' && evaluacion.empresa_nombre === userData.nombre_empresa)
                        );
                    }
                    return false;
                });
                setEvaluaciones(filtered);
            } catch (error) {
                console.error('Error al obtener evaluaciones:', error);
            } finally {
                setLoadingEvaluaciones(false);
            }
        };

        if (userData) {
            fetchInitialEvaluaciones();
        }
    }, [userData]);

    // Función para obtener empleados y datos de filtros (plantas, puestos, departamentos)
    useEffect(() => {
        const fetchEmployeesAndFilters = async () => {
            setLoadingEmpleadosAndFilters(true);
            try {
                // Construir URL para plantas con filtro de empresa si es admin-empresa
                let plantasUrl = '/plantas/listado-plantas';
                if (userData.nivel_usuario === 'admin-empresa' && userData.empresa_id) {
                    plantasUrl = `/plantas/listado-plantas?empresa_id=${userData.empresa_id}`;
                }

                const [empleadosRes, plantasRes, puestosRes, departamentosRes] = await Promise.all([
                    api.get<Empleado[]>('/empleados/'),
                    api.get<Planta[]>(plantasUrl),     // URL de plantas con posible filtro
                    api.get<Puesto[]>('/puestos/'),
                    api.get<Departamento[]>('/departamentos/'),
                ]);

                // Mapear empleados para añadir nombre_completo
                const employeesWithFullName = empleadosRes.data.map(emp => ({
                    ...emp,
                    nombre_completo: `${emp.nombre || ''} ${emp.apellido_paterno || ''} ${emp.apellido_materno || ''}`.trim()
                }));

                setAllEmployeesFetched(employeesWithFullName);

                let initialFilteredEmpleadosByRole = employeesWithFullName;

                if (userData.nivel_usuario === 'admin-planta' && userData.planta_id) {
                    initialFilteredEmpleadosByRole = employeesWithFullName.filter(empleado => empleado.planta_id === userData.planta_id);
                    setFilterPlantaId(userData.planta_id);
                } else if (userData.nivel_usuario === 'admin-empresa' && userData.empresa_id) {
                    initialFilteredEmpleadosByRole = employeesWithFullName.filter(empleado => empleado.empresa_id === userData.empresa_id);
                }

                setEmployeesVisibleByRole(initialFilteredEmpleadosByRole);

                // Filtrar plantas, puestos y departamentos al recibirlos de la API
                let filteredPlantas = plantasRes.data;
                let filteredPuestos = puestosRes.data;
                let filteredDepartamentos = departamentosRes.data;

                if (userData.nivel_usuario === 'admin-empresa' && userData.empresa_id) {
                    // Las plantas ya deberían venir filtradas por la URL, pero reforzamos
                    filteredPlantas = plantasRes.data.filter(p => p.empresa_id === userData.empresa_id);

                    const companyPlantaIds = new Set(filteredPlantas.map(p => p.planta_id));

                    // Filtrar departamentos de las plantas de la empresa
                    filteredDepartamentos = departamentosRes.data.filter(d => d.planta_id && companyPlantaIds.has(d.planta_id));

                    const companyDepartamentoIds = new Set(filteredDepartamentos.map(d => d.departamento_id));

                    // Filtrar puestos de los departamentos de las plantas de la empresa
                    filteredPuestos = puestosRes.data.filter(p => p.departamento_id && companyDepartamentoIds.has(p.departamento_id));

                } else if (userData.nivel_usuario === 'admin-planta' && userData.planta_id) {
                    // Filtrar plantas para la planta específica del admin-planta
                    filteredPlantas = plantasRes.data.filter(p => p.planta_id === userData.planta_id);

                    // Filtrar departamentos de la planta específica
                    filteredDepartamentos = departamentosRes.data.filter(d => d.planta_id === userData.planta_id);

                    const plantDepartamentoIds = new Set(filteredDepartamentos.map(d => d.departamento_id));

                    // Filtrar puestos de los departamentos de la planta específica
                    filteredPuestos = puestosRes.data.filter(p => p.departamento_id && plantDepartamentoIds.has(p.departamento_id));
                }
                // Si es superadmin, no se aplica ningún filtro aquí, se usan todos los datos.

                setPlantas(filteredPlantas);
                setPuestos(filteredPuestos);
                setDepartamentos(filteredDepartamentos);

            } catch (error) {
                console.error('Error al obtener empleados y filtros:', error);
            } finally {
                setLoadingEmpleadosAndFilters(false);
            }
        };

        if (userData) {
            fetchEmployeesAndFilters();
        }
    }, [userData]);

    // Este useEffect se encarga de recargar las asignaciones cuando cambia la evaluación seleccionada
    useEffect(() => {
        fetchAsignacionesForSelectedEvaluacion();
    }, [selectedEvaluacion, fetchAsignacionesForSelectedEvaluacion]);

    // ---------------------------------------------------------------------- //
    // --- Manejadores de Eventos ---

    const handleSelectEvaluacion = (evaluacion: Evaluacion) => {
        setSelectedEvaluacion(evaluacion);
        setShowAssignFormForAsignacionId(null); // Cerrar cualquier formulario de asignación abierto al cambiar de evaluación
    };

    const handleToggleBaseAsignacionStatus = async (asignacionId: number, estadoActual: boolean, fechaFin: string) => {
        const now = new Date();
        const endDate = new Date(fechaFin);

        if (estadoActual && now > endDate) {
            alert('No se puede desactivar una asignación que ya ha terminado.');
            return;
        }

        try {
            if (estadoActual) {
                await evaluacionesAPI.desactivarAsignacion(asignacionId);
                alert('Asignación base y sus asignaciones de empleados desactivadas.');
            } else {
                if (now > endDate) {
                    alert('No se puede activar una asignación cuya fecha de término ha sido excedida.');
                    return;
                }
                await evaluacionesAPI.activarAsignacion(asignacionId);
                alert('Asignación base y sus asignaciones de empleados activadas.');
            }
            fetchAsignacionesForSelectedEvaluacion(); // Recargar solo las asignaciones de la evaluación actual
        } catch (error: any) {
            console.error('Error al cambiar el estado de la asignación base:', error);
            alert(`Error: ${error.response?.data?.error || 'Error desconocido'}`);
        }
    };

    // const handleToggleEmpleadoAsignacionStatus = useCallback(async (asignacionEmpleadoId: number, status: string) => {
    //     if (status === 'Completada') {
    //         alert('No se puede modificar una asignación de empleado que ya ha sido completada.');
    //         return;
    //     }

    //     try {
    //         if (status === 'Activa') {
    //             // Si el estado actual es 'Activa', la vamos a desactivar
    //             await evaluacionesAPI.desactivarAsignacionEmpleado(asignacionEmpleadoId);
    //             alert(`La asignación de empleado (${asignacionEmpleadoId}) ha sido desactivada con éxito.`);
    //         } else if (status === 'Desactivada') {
    //             // Si el estado actual es 'Desactivada', la vamos a activar
    //             await evaluacionesAPI.activarAsignacionEmpleado(asignacionEmpleadoId);
    //             alert(`La asignación de empleado (${asignacionEmpleadoId}) ha sido activada con éxito.`);
    //         }
    //         // Recargar la lista de asignaciones para reflejar el cambio
    //         fetchAsignacionesForSelectedEvaluacion();
    //     } catch (error: any) {
    //         console.error('Error al cambiar el estado de la asignación de empleado:', error);
    //         // Mensaje de error más detallado si la API lo proporciona
    //         alert(`Error al cambiar el estado: ${error.response?.data?.detail || 'Error desconocido'}`);
    //     }
    // }, [fetchAsignacionesForSelectedEvaluacion]);


    const handleAssignMoreEmployees = async (asignacionId: number) => {
        const dataToAssign: { empleado_ids?: number[], planta_ids?: number[], puesto_ids?: number[], departamento_ids?: number[] } = {};

        // Validar si la asignación base ya ha pasado su fecha de fin
        const currentAsignacion = asignacionesBase.find(a => a.asignacion_id === asignacionId);
        if (currentAsignacion && new Date() > new Date(currentAsignacion.fecha_fin)) {
            alert('No se pueden asignar más empleados a una asignación que ya ha terminado.');
            setShowAssignFormForAsignacionId(null); // Cerrar formulario
            return;
        }

        if (assignmentTargetType === 'employees' && selectedEmployeesForNewAssignment.length > 0) {
            dataToAssign.empleado_ids = selectedEmployeesForNewAssignment;
        } else if (assignmentTargetType === 'plant' && selectedTargetId) {
            dataToAssign.planta_ids = [selectedTargetId];
        } else if (assignmentTargetType === 'puesto' && selectedTargetId) {
            dataToAssign.puesto_ids = [selectedTargetId];
        } else if (assignmentTargetType === 'departamento' && selectedTargetId) {
            dataToAssign.departamento_ids = [selectedTargetId];
        }

        if (Object.keys(dataToAssign).length === 0) {
            alert('Por favor, seleccione al menos un empleado o un filtro para asignar.');
            return;
        }


        try {
            console.log('ID de asignación a usar:', asignacionId);
            console.log('Datos a enviar:', dataToAssign);


            await evaluacionesAPI.asignarEmpleados(asignacionId, dataToAssign);
            alert('Empleados asignados con éxito.');
            // Limpiar estados después de la asignación
            setSelectedEmployeesForNewAssignment([]);
            setSearchTerm('');
            // Resetear filterPlantaId a la planta del admin-planta o null
            setFilterPlantaId(userData.nivel_usuario === 'admin-planta' && userData.planta_id ? userData.planta_id : null);
            setFilterPuestoId(null);
            setFilterDepartamentoId(null);
            setSelectedTargetId(null);
            setAssignmentTargetType('employees'); // Resetear a asignación individual por defecto
            setShowAssignFormForAsignacionId(null);
            fetchAsignacionesForSelectedEvaluacion(); // Recargar asignaciones
        } catch (error: any) {
            console.error('Error al asignar empleados:', error);
            alert(`Error al asignar empleados: ${error.response?.data?.error || 'Error desconocido'}`);
        }
    };

    const handleCreateBaseAsignacion = async () => {
        if (!newAsignacionEvaluacionId || !newAsignacionFechaInicio || !newAsignacionFechaFin) {
            alert('Por favor, complete todos los campos para crear la asignación base.');
            return;
        }

        const newAsignacion: AsignacionRequest = {
            evaluacion: newAsignacionEvaluacionId,
            fecha_inicio: newAsignacionFechaInicio,
            fecha_fin: newAsignacionFechaFin,
            status: true, // Por defecto activa al crear
        };

        try {
            await evaluacionesAPI.createAsignacion(newAsignacion);
            alert('Asignación base creada con éxito.');
            setShowCreateAsignacionForm(false);
            setNewAsignacionEvaluacionId(null);
            setNewAsignacionFechaInicio('');
            setNewAsignacionFechaFin('');
            fetchAsignacionesForSelectedEvaluacion(); // Recargar asignaciones para la evaluación seleccionada
        } catch (error: any) {
            console.error('Error al crear asignación base:', error);
            alert(`Error al crear asignación base: ${error.response?.data?.error || 'Error desconocido'}`);
        }
    };

    // Filtra los empleados disponibles para la selección individual
    const getFilteredEmployeesForAssignmentForm = useMemo(() => {
        let filtered = employeesVisibleByRole; // Esta es la lista base, ya filtrada por rol de usuario

        // Aplica el filtro de planta. Para admin-planta, filterPlantaId ya está pre-establecido.
        if (filterPlantaId) {
            filtered = filtered.filter(emp => emp.planta_id === filterPlantaId);
        }

        if (filterPuestoId) {
            filtered = filtered.filter(emp => emp.puesto_id === filterPuestoId);
        }
        if (filterDepartamentoId) {
            filtered = filtered.filter(emp => emp.departamento_id === filterDepartamentoId);
        }
        if (searchTerm) {
            filtered = filtered.filter(emp =>
                emp.nombre_completo.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }
        return filtered;
    }, [employeesVisibleByRole, searchTerm, filterPlantaId, filterPuestoId, filterDepartamentoId]);


    // Filtra las opciones de Planta para el dropdown (interdependiente con el rol del usuario)
    const filteredPlantasOptions = useMemo(() => {
        return plantas;
    }, [plantas]);

    // Filtra las opciones de Departamento para el dropdown (interdependiente)
    const filteredDepartamentosOptions = useMemo(() => {
        // Filtrar departamentos basados en las plantas que el usuario puede ver
        const relevantPlantaIds = new Set(filteredPlantasOptions.map(p => p.planta_id));
        let filtered = departamentos.filter(d => d.planta_id && relevantPlantaIds.has(d.planta_id));

        // Si hay un filtro de planta específico, aplicar
        if (filterPlantaId) {
            filtered = filtered.filter(d => d.planta_id === filterPlantaId);
        }

        // Si hay un filtro de puesto específico, filtrar departamentos que contengan esos puestos
        if (filterPuestoId) {
            const departmentsWithSelectedPuesto = new Set<number>();
            puestos.forEach(puesto => {
                if (puesto.puesto_id === filterPuestoId && puesto.departamento_id) {
                    departmentsWithSelectedPuesto.add(puesto.departamento_id);
                }
            });
            filtered = filtered.filter(d => departmentsWithSelectedPuesto.has(d.departamento_id));
        }

        return filtered.map(dpto => {
            const plantaAsociada = plantas.find(p => p.planta_id === dpto.planta_id);
            const plantaNombre = plantaAsociada ? plantaAsociada.nombre : 'Planta Desconocida';
            const empresaNombre = userData.nombre_empresa || 'Empresa Desconocida';
            return {
                ...dpto,
                nombre_display: `${dpto.nombre} (Planta: ${plantaNombre}, Empresa: ${empresaNombre})`
            };
        });
    }, [departamentos, filteredPlantasOptions, filterPlantaId, filterPuestoId, plantas, puestos, userData.nombre_empresa]);

    // Filtra las opciones de Puesto para el dropdown (interdependiente)
    const filteredPuestosOptions = useMemo(() => {
        // Filtrar puestos basados en los departamentos que el usuario puede ver
        const relevantDepartamentoIds = new Set(filteredDepartamentosOptions.map(d => d.departamento_id));
        let filtered = puestos.filter(p => p.departamento_id && relevantDepartamentoIds.has(p.departamento_id));

        // Si hay un filtro de planta específico, filtrar puestos que pertenezcan a departamentos de esa planta
        if (filterPlantaId) {
            const departmentsInSelectedPlanta = new Set(departamentos.filter(d => d.planta_id === filterPlantaId).map(d => d.departamento_id));
            filtered = filtered.filter(p => p.departamento_id && departmentsInSelectedPlanta.has(p.departamento_id));
        }

        // Si hay un filtro de departamento específico, aplicar
        if (filterDepartamentoId) {
            filtered = filtered.filter(p => p.departamento_id === filterDepartamentoId);
        }

        return filtered.map(puesto => {
            const departamentoAsociado = departamentos.find(d => d.departamento_id === puesto.departamento_id);
            const departamentoNombre = departamentoAsociado ? departamentoAsociado.nombre : 'Departamento Desconocido';
            const plantaAsociada = departamentoAsociado ? plantas.find(p => p.planta_id === departamentoAsociado.planta_id) : null;
            const plantaNombre = plantaAsociada ? plantaAsociada.nombre : 'Planta Desconocida';
            const empresaNombre = userData.nombre_empresa || 'Empresa Desconocida';
            return {
                ...puesto,
                nombre_display: `${puesto.nombre} (Depto: ${departamentoNombre}, Planta: ${plantaNombre}, Empresa: ${empresaNombre})`
            };
        });
    }, [puestos, filteredDepartamentosOptions, filterPlantaId, filterDepartamentoId, departamentos, plantas, userData.nombre_empresa]);


    // Función para agrupar asignaciones de empleados por puesto y departamento
    const groupAssignedEmployees = (assignedEmployees: AsignacionEmpleado[]) => {
        const grouped: { [key: string]: { [key: string]: AsignacionEmpleado[] } } = {}; // { departamento: { puesto: [empleados] } }

        assignedEmployees.forEach(ae => {
            const departamento = ae.empleado_departamento || 'Sin Departamento';
            const puesto = ae.empleado_puesto || 'Sin Puesto';

            if (!grouped[departamento]) {
                grouped[departamento] = {};
            }
            if (!grouped[departamento][puesto]) {
                grouped[departamento][puesto] = [];
            }
            grouped[departamento][puesto].push(ae);
        });
        return grouped;
    };


    // Agrupar asignaciones base por planta si es admin-empresa
    const groupedAsignacionesByPlanta = useMemo(() => {
        if (userData.nivel_usuario === 'admin-empresa') {
            const grouped: { [plantaName: string]: Asignacion[] } = {};
            asignacionesBase.forEach(asignacion => {
                const firstAssignedEmployee = asignacion.asignaciones_empleado[0];
                let plantaNombre = 'Sin Planta Asignada';
                if (firstAssignedEmployee) {
                    plantaNombre = firstAssignedEmployee.empleado_planta || 'Sin Planta Asignada';
                }

                if (!grouped[plantaNombre]) {
                    grouped[plantaNombre] = [];
                }
                grouped[plantaNombre].push(asignacion);
            });
            return grouped;
        }

        // Si es admin-planta, filtrar por la planta del usuario
        if (userData.nivel_usuario === 'admin-planta' && userData.planta_id) {
            const grouped: { [plantaName: string]: Asignacion[] } = {};
            const asignacionesForUserPlanta = asignacionesBase.filter(asignacion =>
                asignacion.asignaciones_empleado.some(ae => ae.empleado_planta_id === userData.planta_id)
            );
            const userPlantaName = plantas.find(p => p.planta_id === userData.planta_id)?.nombre || 'Mi Planta';
            grouped[userPlantaName] = asignacionesForUserPlanta;
            return grouped;
        }

        return { 'Todas las Asignaciones': asignacionesBase }; // Retorna un solo grupo si no es admin-empresa ni admin-planta
    }, [asignacionesBase, userData.nivel_usuario, userData.planta_id, plantas]);


    return (
        <div className="asignaciones-page-container">
            <div className="header-section">
                <h2>Gestión de Asignaciones</h2>
            </div>

            <div className="content-wrapper">
                {/* Panel Izquierdo: Lista de Evaluaciones */}
                <aside className="evaluaciones-list-panel card">
                    <h3>Evaluaciones Disponibles</h3>
                    {loadingEvaluaciones ? (
                        <p>Cargando evaluaciones...</p>
                    ) : evaluaciones.length === 0 ? (
                        <p>No hay evaluaciones disponibles para su perfil.</p>
                    ) : (
                        <ul className="evaluacion-selection-list">
                            {evaluaciones.map(evaluacion => (
                                <li
                                    key={evaluacion.evaluacion_id}
                                    className={`evaluacion-item ${selectedEvaluacion?.evaluacion_id === evaluacion.evaluacion_id ? 'selected' : ''}`}
                                    onClick={() => handleSelectEvaluacion(evaluacion)}
                                >
                                    {evaluacion.titulo} ({evaluacion.tipo_evaluacion})
                                    {evaluacion.tipo_evaluacion === 'Interna' && evaluacion.empresa_nombre && (
                                        <span className="evaluacion-empresa"> ({evaluacion.empresa_nombre})</span>
                                    )}
                                </li>
                            ))}
                        </ul>
                    )}
                    {(userData.nivel_usuario === 'admin-empresa' || userData.nivel_usuario === 'superadmin') && (
                        <button onClick={() => setShowCreateAsignacionForm(!showCreateAsignacionForm)} className="btn-primary create-base-asignacion-btn">
                            {showCreateAsignacionForm ? 'Cancelar Creación' : '➕ Crear Asignación Base'}
                        </button>
                    )}

                    {showCreateAsignacionForm && (
                        <div className="create-base-asignacion-form card">
                            <h4>Nueva Asignación Base</h4>
                            <div className="form-group">
                                <label htmlFor="newEvaluacionSelect">Evaluación:</label>
                                <select
                                    id="newEvaluacionSelect"
                                    value={newAsignacionEvaluacionId || ''}
                                    onChange={(e) => setNewAsignacionEvaluacionId(Number(e.target.value))}
                                >
                                    <option value="">Seleccione una evaluación</option>
                                    {evaluaciones.map(evaluacion => (
                                        <option key={evaluacion.evaluacion_id} value={evaluacion.evaluacion_id}>
                                            {evaluacion.titulo} ({evaluacion.tipo_evaluacion})
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className="form-group">
                                <label htmlFor="newFechaInicio">Fecha de Inicio:</label>
                                <input
                                    type="datetime-local"
                                    min={now}
                                    id="newFechaInicio"
                                    value={newAsignacionFechaInicio}
                                    onChange={(e) => setNewAsignacionFechaInicio(e.target.value)}
                                />
                            </div>
                            <div className="form-group">
                                <label htmlFor="newFechaFin">Fecha de Fin:</label>
                                <input
                                    type="datetime-local"
                                    min={now}
                                    id="newFechaFin"
                                    value={newAsignacionFechaFin}
                                    onChange={(e) => setNewAsignacionFechaFin(e.target.value)}
                                />
                            </div>
                            <button onClick={handleCreateBaseAsignacion} className="btn-primary">Crear Asignación</button>
                        </div>
                    )}
                </aside>

                {/* Panel Derecho: Detalles de Asignaciones */}
                <main className="asignaciones-details-panel card">
                    {selectedEvaluacion ? (
                        <>
                            <h3>Asignaciones para: {selectedEvaluacion.titulo}</h3>
                            {loadingAsignaciones ? (
                                <p>Cargando asignaciones...</p>
                            ) : Object.keys(groupedAsignacionesByPlanta).length === 0 ? (
                                <p>No hay asignaciones para esta evaluación.</p>
                            ) : (
                                Object.entries(groupedAsignacionesByPlanta).map(([plantaName, asignaciones]) => (
                                    <div key={plantaName} className="planta-group">
                                        {(userData.nivel_usuario === 'admin-empresa' || Object.keys(groupedAsignacionesByPlanta).length > 1) && (
                                            <h4>Planta: {plantaName}</h4>
                                        )}
                                        <ul className="asignaciones-base-list">
                                            {asignaciones.map(asignacion => (
                                                <li key={asignacion.asignacion_id} className="asignacion-base-item">
                                                    <div className="asignacion-base-header">
                                                        <h5>ID Asignación: {asignacion.asignacion_id}</h5>
                                                        <span className={`badge ${asignacion.status ? 'badge-active' : 'badge-inactive'}`}>
                                                            {asignacion.status ? 'Activa' : 'Inactiva'}
                                                        </span>
                                                    </div>
                                                    <p>Inicio: {new Date(asignacion.fecha_inicio).toLocaleString()}</p>
                                                    <p>Fin: {new Date(asignacion.fecha_fin).toLocaleString()}</p>

                                                    <div className="base-asignacion-actions">
                                                        <button
                                                            onClick={() => handleToggleBaseAsignacionStatus(asignacion.asignacion_id, asignacion.status, asignacion.fecha_fin)}
                                                            className={`btn-small ${asignacion.status ? 'btn-danger' : 'btn-success'}`}
                                                            disabled={new Date() > new Date(asignacion.fecha_fin) && asignacion.status}
                                                        >
                                                            {asignacion.status ? 'Desactivar Asignación Base' : 'Activar Asignación Base'}
                                                        </button>
                                                        <button
                                                            onClick={() => setShowAssignFormForAsignacionId(asignacion.asignacion_id === showAssignFormForAsignacionId ? null : asignacion.asignacion_id)}
                                                            className="btn-small btn-info"
                                                            disabled={new Date() > new Date(asignacion.fecha_fin)} // Deshabilitar si la fecha de fin ya pasó
                                                        >
                                                            {asignacion.asignacion_id === showAssignFormForAsignacionId ? 'Cerrar Formulario' : 'Asignar Más Empleados'}
                                                        </button>
                                                    </div>

                                                    {/* Formulario para asignar más empleados */}
                                                    {showAssignFormForAsignacionId === asignacion.asignacion_id && (
                                                        <div className="assign-more-employees-form card">
                                                            <h6>Asignar Empleados a esta Asignación</h6>
                                                            {loadingEmpleadosAndFilters ? (
                                                                <p>Cargando opciones de asignación...</p>
                                                            ) : (
                                                                <>
                                                                    <div className="form-group">
                                                                        <label>Tipo de Asignación:</label>
                                                                        <div className="radio-group">
                                                                            <label>
                                                                                <input
                                                                                    type="radio"
                                                                                    value="employees"
                                                                                    checked={assignmentTargetType === 'employees'}
                                                                                    onChange={() => { setAssignmentTargetType('employees'); setSelectedTargetId(null); setSearchTerm(''); setFilterPlantaId(userData.nivel_usuario === 'admin-planta' && userData.planta_id ? userData.planta_id : null); setFilterPuestoId(null); setFilterDepartamentoId(null); }}
                                                                                /> Individual
                                                                            </label>
                                                                            <label>
                                                                                <input
                                                                                    type="radio"
                                                                                    value="plant"
                                                                                    checked={assignmentTargetType === 'plant'}
                                                                                    onChange={() => { setAssignmentTargetType('plant'); setSelectedTargetId(null); setSearchTerm(''); setFilterPlantaId(null); setFilterPuestoId(null); setFilterDepartamentoId(null); }}
                                                                                    disabled={userData.nivel_usuario === 'admin-planta'} // Admin planta no asigna por planta completa
                                                                                /> Por Planta
                                                                            </label>
                                                                            <label>
                                                                                <input
                                                                                    type="radio"
                                                                                    value="puesto"
                                                                                    checked={assignmentTargetType === 'puesto'}
                                                                                    onChange={() => { setAssignmentTargetType('puesto'); setSelectedTargetId(null); setSearchTerm(''); setFilterPlantaId(null); setFilterPuestoId(null); setFilterDepartamentoId(null); }}
                                                                                /> Por Puesto
                                                                            </label>
                                                                            <label>
                                                                                <input
                                                                                    type="radio"
                                                                                    value="departamento"
                                                                                    checked={assignmentTargetType === 'departamento'}
                                                                                    onChange={() => { setAssignmentTargetType('departamento'); setSelectedTargetId(null); setSearchTerm(''); setFilterPlantaId(null); setFilterPuestoId(null); setFilterDepartamentoId(null); }}
                                                                                /> Por Departamento
                                                                            </label>
                                                                        </div>
                                                                    </div>

                                                                    {assignmentTargetType === 'employees' && (
                                                                        <>
                                                                            <div className="form-row">
                                                                                <div className="form-group">
                                                                                    <label htmlFor="searchTerm">Buscar Empleado</label>
                                                                                    <input
                                                                                        type="text"
                                                                                        id="searchTerm"
                                                                                        value={searchTerm}
                                                                                        onChange={(e) => setSearchTerm(e.target.value)}
                                                                                        placeholder="Nombre del empleado"
                                                                                    />
                                                                                </div>
                                                                                <div className="form-group">
                                                                                    <label htmlFor="filterPlanta">Filtrar por Planta</label>
                                                                                    <select
                                                                                        id="filterPlanta"
                                                                                        value={filterPlantaId || ''}
                                                                                        onChange={(e) => setFilterPlantaId(e.target.value ? Number(e.target.value) : null)}
                                                                                        disabled={userData.nivel_usuario === 'admin-planta'} // Deshabilitar para admin-planta
                                                                                    >
                                                                                        <option value="">Todas las Plantas</option>
                                                                                        {filteredPlantasOptions.map(p => (
                                                                                            <option key={p.planta_id} value={p.planta_id}>{p.nombre}</option>
                                                                                        ))}
                                                                                    </select>
                                                                                </div>
                                                                                <div className="form-group">
                                                                                    <label htmlFor="filterPuesto">Filtrar por Puesto</label>
                                                                                    <select
                                                                                        id="filterPuesto"
                                                                                        value={filterPuestoId || ''}
                                                                                        onChange={(e) => setFilterPuestoId(e.target.value ? Number(e.target.value) : null)}
                                                                                    >
                                                                                        <option value="">Todos los Puestos</option>
                                                                                        {filteredPuestosOptions.map(p => (
                                                                                            <option key={p.puesto_id} value={p.puesto_id}>{p.nombre_display}</option>
                                                                                        ))}
                                                                                    </select>
                                                                                </div>
                                                                                <div className="form-group">
                                                                                    <label htmlFor="filterDepartamento">Filtrar por Departamento</label>
                                                                                    <select
                                                                                        id="filterDepartamento"
                                                                                        value={filterDepartamentoId || ''}
                                                                                        onChange={(e) => setFilterDepartamentoId(e.target.value ? Number(e.target.value) : null)}
                                                                                    >
                                                                                        <option value="">Todos los Departamentos</option>
                                                                                        {filteredDepartamentosOptions.map(d => (
                                                                                            <option key={d.departamento_id} value={d.departamento_id}>{d.nombre_display}</option>
                                                                                        ))}
                                                                                    </select>
                                                                                </div>
                                                                            </div>
                                                                            <div className="form-group">
                                                                                <label>Seleccionar Empleados</label>
                                                                                <select
                                                                                    multiple
                                                                                    value={selectedEmployeesForNewAssignment.map(String)}
                                                                                    onChange={(e) =>
                                                                                        setSelectedEmployeesForNewAssignment(
                                                                                            Array.from(e.target.selectedOptions, (option) => Number(option.value))
                                                                                        )
                                                                                    }
                                                                                    className="select-multiple"
                                                                                    size={Math.min(getFilteredEmployeesForAssignmentForm.length, 8)}
                                                                                >
                                                                                    {getFilteredEmployeesForAssignmentForm.map((empleado) => (
                                                                                        <option key={empleado.empleado_id} value={empleado.empleado_id}>
                                                                                            {empleado.nombre_completo}
                                                                                        </option>
                                                                                    ))}
                                                                                </select>
                                                                            </div>
                                                                        </>
                                                                    )}

                                                                    {assignmentTargetType === 'plant' && userData.nivel_usuario === 'admin-empresa' && (
                                                                        <div className="form-group">
                                                                            <label htmlFor="selectPlanta">Seleccionar Planta</label>
                                                                            <select
                                                                                id="selectPlanta"
                                                                                value={selectedTargetId || ''}
                                                                                onChange={(e) => setSelectedTargetId(Number(e.target.value))}
                                                                            >
                                                                                <option value="">Seleccione una planta</option>
                                                                                {plantas.map(p => (
                                                                                    <option key={p.planta_id} value={p.planta_id}>{p.nombre}</option>
                                                                                ))}
                                                                            </select>
                                                                        </div>
                                                                    )}

                                                                    {assignmentTargetType === 'puesto' && (
                                                                        <div className="form-group">
                                                                            <label htmlFor="selectPuesto">Seleccionar Puesto</label>
                                                                            <select
                                                                                id="selectPuesto"
                                                                                value={selectedTargetId || ''}
                                                                                onChange={(e) => setSelectedTargetId(Number(e.target.value))}
                                                                            >
                                                                                <option value="">Seleccione un puesto</option>
                                                                                {filteredPuestosOptions.map(p => (
                                                                                    <option key={p.puesto_id} value={p.puesto_id}>{p.nombre_display}</option>
                                                                                ))}
                                                                            </select>
                                                                        </div>
                                                                    )}

                                                                    {assignmentTargetType === 'departamento' && (
                                                                        <div className="form-group">
                                                                            <label htmlFor="selectDepartamento">Seleccionar Departamento</label>
                                                                            <select
                                                                                id="selectDepartamento"
                                                                                value={selectedTargetId || ''}
                                                                                onChange={(e) => setSelectedTargetId(Number(e.target.value))}
                                                                            >
                                                                                <option value="">Seleccione un departamento</option>
                                                                                {filteredDepartamentosOptions.map(d => (
                                                                                    <option key={d.departamento_id} value={d.departamento_id}>{d.nombre_display}</option>
                                                                                ))}
                                                                            </select>
                                                                        </div>
                                                                    )}

                                                                    <button onClick={() => handleAssignMoreEmployees(asignacion.asignacion_id)} className="btn-primary">
                                                                        Asignar Seleccionados
                                                                    </button>
                                                                </>
                                                            )}
                                                        </div>
                                                    )}

                                                    {/* Listado de empleados asignados, agrupados por puesto y departamento */}
                                                    <div className="empleados-asignados-section">
                                                        <h6>Empleados Asignados ({asignacion.asignaciones_empleado.length}):</h6>
                                                        {asignacion.asignaciones_empleado.length === 0 ? (
                                                            <p>No hay empleados asignados a esta asignación base.</p>
                                                        ) : (
                                                            Object.entries(groupAssignedEmployees(asignacion.asignaciones_empleado)).map(([departamento, puestosGroup]) => (
                                                                <div key={departamento} className="departamento-group">
                                                                    <strong>Departamento: {departamento}</strong>
                                                                    {Object.entries(puestosGroup).map(([puesto, empleados]) => (
                                                                        <div key={puesto} className="puesto-group">
                                                                            <em>Puesto: {puesto}</em>
                                                                            <ul className="empleados-list-detail">
                                                                                {empleados.map(ae => (
                                                                                    <li key={ae.asignacion_empleado_id} className="empleado-asignado-item">
                                                                                        <span>{ae.empleado_nombre}</span>
                                                                                        <span>Token: {ae.token_acceso}</span>

                                                                                        <span className={`badge ${ae.status === 'Completada' ? 'badge-completed' : ae.status === 'Pendiente' ? 'badge-pending' : 'badge-inactive'}`}>
                                                                                            {ae.status}
                                                                                        </span>
                                                                                        {/* El botón de desactivar individual solo informa, no realiza la acción */}

                                                                                        {/* {ae.status !== 'Completada' && ae.status !== 'Expirada' && (
                                                                                            <button
                                                                                                onClick={() => handleToggleEmpleadoAsignacionStatus(ae.asignacion_empleado_id, ae.status)}
                                                                                                className={`btn-toggle ${(ae.status as string) === 'Activa' ? 'active' : 'inactive'}`}
                                                                                                title={(ae.status as string) === 'Activa' ? 'Desactivar asignación' : 'Activar asignación'}
                                                                                            >
                                                                                                {(ae.status as string) === 'Activa' ? '🟢' : '🔴'}
                                                                                            </button>
                                                                                        )} */}


                                                                                    </li>


                                                                                ))}
                                                                            </ul>

                                                                        </div>
                                                                    ))}
                                                                </div>
                                                            ))
                                                        )}
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ))
                            )}
                        </>
                    ) : (
                        <p className="select-evaluacion-message">Seleccione una evaluación de la lista para ver sus asignaciones.</p>
                    )}
                </main>
            </div>
        </div>
    );
};

export default AsignacionesDashboard;
