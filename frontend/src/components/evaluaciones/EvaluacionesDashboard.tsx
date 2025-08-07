
// -------------------------------------------------------------------------- //

import React, { useState, useEffect } from 'react';
import evaluacionesAPI, { Evaluacion, TipoEvaluacion } from '../../services/evaluacionesService';

import EvaluacionFormulario from './EvaluacionFormulario';
import EvaluacionPrevia from './EvaluacionPrevia';


import './EvaluacionesDashboard.css';

// -------------------------------------------------------------------------- //

interface UserData {
    usuario: string;
    user_id?: number;
    profile_id?: number; // ID del perfil de usuario para creado_por_id
    nivel_usuario: string;

    empresa_id?: number;
    nombre_empresa?: string;
    planta_id?: number;
}

// -------------------------------------------------------------------------- //

const EvaluacionesDashboard: React.FC<{ userData: UserData | null }> = ({ userData }) => {
    const [evaluaciones, setEvaluaciones] = useState<Evaluacion[]>([]);
    const [tiposEvaluacion, setTiposEvaluacion] = useState<TipoEvaluacion[]>([]);
    const [selectedEvaluacion, setSelectedEvaluacion] = useState<Evaluacion | null>(null);
    const [showForm, setShowForm] = useState(false);
    // const [showAsignaciones, setShowAsignaciones] = useState(false);
    const [loading, setLoading] = useState(true);
    const [showPreview, setShowPreview] = useState(false);


    // ---------------------------------------------------------------------- //

    useEffect(() => {
        if (userData) {
            fetchEvaluaciones();
            fetchTiposEvaluacion();
        } else {
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

                    if (userData.nivel_usuario === 'superadmin') {
                        return evaluacion.tipo_evaluacion === 'Normativa';
                    }

                    if (userData.nivel_usuario === 'admin-empresa' || userData.nivel_usuario === 'admin-planta') {
                        return (
                            evaluacion.tipo_evaluacion === 'Normativa' || (evaluacion.tipo_evaluacion === 'Interna' &&
                                evaluacion.empresa_nombre === userData.nombre_empresa)
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
        if (userData.nivel_usuario === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') {
            alert('Usted solamente posee permisos para editar evaluaciones normativas');
            return;
        }
        if ((userData.nivel_usuario === 'admin-empresa' || userData.nivel_usuario === 'admin-planta') && evaluacion.tipo_evaluacion === 'Normativa') {
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

    const handlePreview = (evaluacion: Evaluacion) => {
        console.log('en proceso...')
        setSelectedEvaluacion(evaluacion);
        setShowPreview(true);
    };

    // ---------------------------------------------------------------------- //

    return (
        <div className={`dashboard-container ${userData?.nivel_usuario === 'superadmin' ? 'super-admin-theme' : ''}`}>
            <h2>Gestión de evaluaciones</h2>
            <button onClick={handleCreate}
                className="btn-primary"
                disabled={!userData || (userData.nivel_usuario !== 'superadmin' && userData.nivel_usuario !== 'admin-empresa' && userData.nivel_usuario !== 'admin-planta')}
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
                                        (userData?.nivel_usuario === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') ||
                                        ((userData?.nivel_usuario === 'admin-empresa' || userData?.nivel_usuario === 'admin-planta') && evaluacion.tipo_evaluacion === 'Normativa')
                                    }>✏️ Editar
                                </button>

                                <button
                                    onClick={() => handleToggleEstado(evaluacion)}
                                    className={`btn-${evaluacion.estado ? 'danger' : 'success'}`}
                                    disabled={
                                        // Superadmin no puede activar evaluaciones que no sean Normativa
                                        (userData?.nivel_usuario === 'superadmin' && evaluacion.tipo_evaluacion !== 'Normativa') ||

                                        // Admins no pueden DESACTIVAR evaluaciones Normativa
                                        ((userData?.nivel_usuario === 'admin-empresa' || userData?.nivel_usuario === 'admin-planta') &&
                                        evaluacion.tipo_evaluacion === 'Normativa' &&
                                        evaluacion.estado === true)
                                    }
                                >
                                    {evaluacion.estado ? 'Desactivar' : 'Activar'}
                                </button>

                                <button onClick={() => handlePreview(evaluacion)} className="btn-info">
                                    👁️ Vista Previa
                                </button>
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
                    darkTheme={userData?.nivel_usuario === 'superadmin'}
                />
            )}

            {showPreview && selectedEvaluacion && (
                <EvaluacionPrevia
                    evaluacion={selectedEvaluacion}
                    onClose={() => setShowPreview(false)}
                    darkTheme={userData?.nivel_usuario === 'superadmin'}
                />
            )}
        </div>
    );
};

// -------------------------------------------------------------------------- //

export default EvaluacionesDashboard;

// -------------------------------------------------------------------------- //
