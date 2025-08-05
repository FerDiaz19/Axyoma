
import React, { useState, useEffect } from 'react';
import '../../css/modal.css';

import evaluacionesAPI, { Asignacion, AsignacionRequest, Evaluacion, AsignacionEmpleado } from '../../services/evaluacionesService';


interface AsignacionesModalProps {
    evaluacion: Evaluacion;
    onClose: () => void;
}

const AsignacionesModal: React.FC<AsignacionesModalProps> = ({ evaluacion, onClose }) => {
    const [asignacionesBase, setAsignacionesBase] = useState<Asignacion[]>([]);
    const [loading, setLoading] = useState(true);
    const [asignacionData, setAsignacionData] = useState<AsignacionRequest>({
        evaluacion: evaluacion.evaluacion_id,
        fecha_inicio: '',
        fecha_fin: '',
    });
    const [empleadosToAssign, setEmpleadosToAssign] = useState<{ empleado_ids: number[] }>({ empleado_ids: [] });

    const fetchAsignaciones = async () => {
        setLoading(true);
        try {
        const response = await evaluacionesAPI.getAsignaciones();
        // Filtrar por la evaluación actual
        const filtered = response.data.filter(a => a.evaluacion === evaluacion.evaluacion_id);
        setAsignacionesBase(filtered);
        } catch (error) {
        console.error('Error al obtener asignaciones:', error);
        } finally {
        setLoading(false);
        }
    };

    useEffect(() => {
        fetchAsignaciones();
    }, [evaluacion]);

    const handleCreateAsignacion = async () => {
        try {
        const newAsignacion = await evaluacionesAPI.createAsignacion(asignacionData);
        alert('Asignación base creada con éxito.');

        // Si hay empleados seleccionados, asignarlos inmediatamente
        if (empleadosToAssign.empleado_ids.length > 0) {
            await evaluacionesAPI.asignarEmpleados(newAsignacion.data.asignacion_id, empleadosToAssign);
            alert('Empleados asignados con éxito.');
        }

        fetchAsignaciones();
        } catch (error) {
        console.error('Error al crear la asignación:', error);
        alert('Error al crear la asignación.');
        }
    };

    const handleToggleEstadoAsignacion = async (asignacionId: number, estadoActual: boolean) => {
        try {
        if (estadoActual) {
            await evaluacionesAPI.desactivarAsignacion(asignacionId);
            alert('Asignación desactivada.');
        } else {
            await evaluacionesAPI.activarAsignacion(asignacionId);
            alert('Asignación activada.');
        }
        fetchAsignaciones();
        } catch (error: any) {
        console.error('Error al cambiar el estado:', error);
        alert(`Error: ${error.response?.data?.error || 'Error desconocido'}`);
        }
    };

    const handleToggleEstadoEmpleado = async (asignacionEmpleadoId: number, estadoActual: string) => {
        // Nota: El API no tiene endpoints directos para activar/desactivar asignaciones individuales,
        // se gestionan a través de la asignación base. Aquí podríamos mostrar un mensaje o
        // usar el endpoint de actualización si existiera.
        console.warn(`Función no implementada por la API: Cambiar estado del empleado ${asignacionEmpleadoId}`);
        alert('Esta acción solo puede realizarse a nivel de la asignación base.');
    };

    return (
        <div className="modal-overlay">
        <div className="modal-content">
            <h3>Gestión de Asignaciones para: {evaluacion.titulo}</h3>

            {/* Formulario para crear una nueva asignación base */}
            <div className="form-section">
            <h4>Crear Nueva Asignación</h4>
            <div className="form-group">
                <label>Fecha de Inicio</label>
                <input type="datetime-local" value={asignacionData.fecha_inicio} onChange={(e) => setAsignacionData({...asignacionData, fecha_inicio: e.target.value})} />
            </div>
            <div className="form-group">
                <label>Fecha de Término</label>
                <input type="datetime-local" value={asignacionData.fecha_fin} onChange={(e) => setAsignacionData({...asignacionData, fecha_fin: e.target.value})} />
            </div>
            <button onClick={handleCreateAsignacion} className="btn-primary">Crear Asignación Base</button>
            </div>

            <hr />

            {/* Listado de asignaciones base existentes */}
            <div className="list-section">
            <h4>Asignaciones Existentes</h4>
            {loading ? (
                <p>Cargando asignaciones...</p>
            ) : (
                <ul className="asignaciones-list">
                {asignacionesBase.map(asignacion => (
                    <li key={asignacion.asignacion_id} className="asignacion-item">
                    <p>ID Asignación: **{asignacion.asignacion_id}**</p>
                    <p>Estado Base: **{asignacion.status ? 'Activa' : 'Inactiva'}**</p>
                    <button onClick={() => handleToggleEstadoAsignacion(asignacion.asignacion_id, asignacion.status)} className={`btn-${asignacion.status ? 'danger' : 'success'}`}>
                        {asignacion.status ? 'Desactivar' : 'Activar'}
                    </button>

                    <div className="empleados-list">
                        <h5>Empleados Asignados ({asignacion.asignaciones_empleado.length}):</h5>
                        <ul>
                        {asignacion.asignaciones_empleado.map(emp => (
                            <li key={emp.asignacion_empleado_id}>
                            {emp.empleado_nombre} - Estado: {emp.status}
                            </li>
                        ))}
                        </ul>
                    </div>
                    </li>
                ))}
                </ul>
            )}
            </div>

            <div className="modal-actions">
            <button onClick={onClose} className="btn-secondary">Cerrar</button>
            </div>
        </div>
        </div>
    );
};

export default AsignacionesModal;