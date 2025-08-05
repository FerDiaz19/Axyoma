
import React, { useState, useEffect } from 'react';
import evaluacionesAPI, { Evaluacion, TipoEvaluacion } from '../../services/evaluacionesService';

import EvaluacionFormulario from './EvaluacionFormulario';
import AsignacionesModal from './AsignacionesModal';

// 👉 Importa el archivo CSS que acabas de crear
import './EvaluacionesDashboard.css';

// -------------------------------------------------------------------------- //

interface UserData {
    rol: string;
    empresa?: number;
}

const EvaluacionesDashboard: React.FC = () => {
    const [evaluaciones, setEvaluaciones] = useState<Evaluacion[]>([]);
    const [tiposEvaluacion, setTiposEvaluacion] = useState<TipoEvaluacion[]>([]);
    const [selectedEvaluacion, setSelectedEvaluacion] = useState<Evaluacion | null>(null);
    const [showForm, setShowForm] = useState(false);
    const [showAsignaciones, setShowAsignaciones] = useState(false);
    const [loading, setLoading] = useState(true);

    const [userData, setUserData] = useState<UserData | null>(null);

    // ---------------------------------------------------------------------- //
    // Nuevo useEffect para obtener los datos del usuario de localStorage
    useEffect(() => {
        console.log("🔄 EvaluacionesDashboard: Intentando obtener userData de localStorage...");
        const storedUserData = localStorage.getItem('userData');
        if (storedUserData) {
            try {
                const data = JSON.parse(storedUserData);
                // Verifica el campo del rol, que puede ser 'rol' o 'nivel_usuario'
                const userRole = data.rol || data.nivel_usuario;
                const normalizedUserData = {
                    rol: userRole?.replace('_', '-').toLowerCase(),
                    empresa: data.empresa,
                };
                setUserData(normalizedUserData);
                console.log("✅ EvaluacionesDashboard: userData cargado exitosamente:", normalizedUserData);
            } catch (error) {
                console.error("❌ Error al procesar los datos de usuario de localStorage:", error);
                setUserData(null);
            }
        } else {
            console.log("⚠️ EvaluacionesDashboard: No se encontró userData en localStorage.");
            setUserData(null);
            setLoading(false); // Detener el loading si no hay datos de usuario
        }
    }, []); // Se ejecuta solo una vez al montar el componente

    // ---------------------------------------------------------------------- //

    useEffect(() => {
        if (userData) {
            fetchEvaluaciones();
            fetchTiposEvaluacion();
        } else {
            // Si no hay userData, detener el estado de carga
            setLoading(false);
        }
    }, [userData]);

    // --------------------------------------------------------------------- //

    const fetchEvaluaciones = async () => {
        setLoading(true);
        try {
            const response = await evaluacionesAPI.getEvaluaciones();
            const allEvaluaciones = response.data;

            if (userData) {
                const filteredEvaluaciones = allEvaluaciones.filter(evaluacion => {
                    // Lógica de filtrado
                    if (userData.rol === 'superadmin') {
                        return evaluacion.tipo_evaluacion === 'Normativa';
                    }
                    if (userData.rol === 'admin-empresa' || userData.rol === 'admin-planta') {
                        return (
                            evaluacion.tipo_evaluacion === 'Normativa' ||
                            (evaluacion.tipo_evaluacion === 'Interna' && evaluacion.empresa === userData.empresa)
                        );
                    }
                    return false;
                });
                setEvaluaciones(filteredEvaluaciones);
            } else {
                setEvaluaciones(allEvaluaciones);
            }
        } catch (error) {
            console.error('Error al obtener evaluaciones:', error);
            setEvaluaciones([]);
        } finally {
            setLoading(false);
        }
    };

    // ---------------------------------------------------------------------- //

    const fetchTiposEvaluacion = async () => {
        try {
            const response = await evaluacionesAPI.getTipos();
            setTiposEvaluacion(response.data);
        } catch (error) {
            console.error('Error al obtener tipos de evaluación:', error);
            setTiposEvaluacion([]);
        }
    };

    // ---------------------------------------------------------------------- //

    const handleCreate = () => {
        if (!userData) return;
        setSelectedEvaluacion(null);
        setShowForm(true);
    };

    // ---------------------------------------------------------------------- //

    const handleEdit = (evaluacion: Evaluacion) => {
        if (!userData) return;
        if (userData.rol === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') {
            alert('Usted solamente posee permisos para editar evaluaciones normativas');
            return;
        }
        if ((userData.rol === 'admin-empresa' || userData.rol === 'admin-planta') && evaluacion.tipo_evaluacion === 'Normativa') {
            alert('Usted no posee permisos para editar evaluaciones normativas.');
            return;
        }
        setSelectedEvaluacion(evaluacion);
        setShowForm(true);
    };

    // ---------------------------------------------------------------------- //

    const handleToggleEstado = async (evaluacion: Evaluacion) => {
        try {
            if (evaluacion.estado) {
                await evaluacionesAPI.desactivarEvaluacion(evaluacion.evaluacion_id);
                alert('Evaluación desactivada con éxito.');
            } else {
                await evaluacionesAPI.activarEvaluacion(evaluacion.evaluacion_id);
                alert('Evaluación activada con éxito.');
            }
            fetchEvaluaciones();
        } catch (error) {
            console.error('Error al cambiar el estado:', error);
            alert('Ha ocurrido un error al cambiar el estado de la evaluación.');
        }
    };

    // ---------------------------------------------------------------------- //

    const handleAsignar = (evaluacion: Evaluacion) => {
        if (!userData) return;
        if (userData.rol === 'superadmin') {
            alert('Solamente las empresas clientes poseen permiso para realizar asignaciones.');
            return;
        }
        setSelectedEvaluacion(evaluacion);
        setShowAsignaciones(true);
    };

    // ---------------------------------------------------------------------- //

    return (
        <div className="dashboard-container">
            <h2>Gestión de evaluaciones</h2>
            <button onClick={handleCreate}
                className="btn-primary"
                disabled={!userData || (userData.rol !== 'superadmin' && userData.rol !== 'admin-empresa' && userData.rol !== 'admin-planta')}
                >➕ Crear evaluación
            </button>

            {loading ? (
                <p>Cargando evaluaciones...</p>
            ) : (
                <ul className="evaluaciones-list">
                    {evaluaciones.map(evaluacion => (
                        <li key={evaluacion.evaluacion_id} className="evaluacion-card">
                            <div>
                                <h4>{evaluacion.titulo}</h4>
                                <p><strong>Estado:</strong> {evaluacion.estado ? 'Activa' : 'Inactiva'}</p>
                            </div>

                            <div className="card-actions">
                                {/* Botón de enlace a contenido informativo. Asegúrate de tener una ruta o URL válida */}
                                {evaluacion.contenido_informativo && (
                                    <a href={evaluacion.contenido_informativo} className="btn-link" target="_blank" rel="noopener noreferrer">
                                        📜 Contenido informativo
                                    </a>
                                )}

                                <button onClick={() => handleEdit(evaluacion)}
                                    className="btn-secondary"
                                    disabled={
                                        (userData?.rol === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') ||
                                        ((userData?.rol === 'admin-empresa' || userData?.rol === 'admin-planta') && evaluacion.tipo_evaluacion === 'Normativa')
                                    }>✏️ Editar
                                </button>

                                <button
                                    onClick={() => handleToggleEstado(evaluacion)}
                                    className={`btn-${evaluacion.estado ? 'danger' : 'success'}`}
                                    disabled={
                                        // Superadmin no puede activar evaluaciones que no sean Normativa
                                        (userData?.rol === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') ||

                                        // Admins no pueden DESACTIVAR evaluaciones Normativa
                                        ((userData?.rol === 'admin-empresa' || userData?.rol === 'admin-planta') &&
                                        evaluacion.tipo_evaluacion === 'Normativa' &&
                                        evaluacion.estado === true)
                                    }
                                >
                                    {evaluacion.estado ? 'Desactivar' : 'Activar'}
                                </button>


                                {(userData?.rol === 'admin-empresa' || userData?.rol === 'admin-planta') && (
                                    <button onClick={() => handleAsignar(evaluacion)} className="btn-info">👥 Asignar evaluación</button>
                                )}
                            </div>
                        </li>
                    ))}
                </ul>
            )}

            {showForm && userData && (
                <EvaluacionFormulario
                    evaluacion={selectedEvaluacion}
                    onClose={() => {
                        setShowForm(false);
                        fetchEvaluaciones();
                    }}
                    tiposEvaluacion={tiposEvaluacion}
                    user={userData}
                />
            )}

            {showAsignaciones && selectedEvaluacion && (
                <AsignacionesModal
                    evaluacion={selectedEvaluacion}
                    onClose={() => setShowAsignaciones(false)}
                />
            )}
        </div>
    );
};

// -------------------------------------------------------------------------- //

export default EvaluacionesDashboard;

// -------------------------------------------------------------------------- //