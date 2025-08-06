import React from 'react';
import { Evaluacion, SeccionEval, SeccionPregunta, PosiblesRespuestas } from '../../services/evaluacionesService';
import './EvaluacionPrevia.css'; // Asegúrate de crear este archivo CSS

interface EvaluacionPreviaProps {
    evaluacion: Evaluacion;
    onClose: () => void;
}

const EvaluacionPrevia: React.FC<EvaluacionPreviaProps> = ({ evaluacion, onClose }) => {

    return (
        <div className="modal-overlay">
            <div className="modal-content preview-modal">
                <div className="modal-header-custom">
                    <h3 className="modal-title">👁️ Vista Previa de Evaluación: {evaluacion.titulo}</h3>
                    <div className="modal-actions-top">
                        <button type="button" className="btn-secondary btn-volver" onClick={onClose}>
                            <i className="fas fa-arrow-left"></i> Volver
                        </button>
                    </div>
                </div>

                <div className="preview-body">
                    <section className="preview-section">
                        <h4 className="preview-section-title">Información General</h4>
                        <p><strong>Título:</strong> {evaluacion.titulo}</p>
                        <p><strong>Descripción:</strong> {evaluacion.descripcion || 'N/A'}</p>
                        <p><strong>Instrucciones:</strong> {evaluacion.instrucciones || 'N/A'}</p>
                        <p><strong>Contenido Informativo:</strong>
                            {evaluacion.contenido_informativo ? (
                                <a href={evaluacion.contenido_informativo} target="_blank" rel="noopener noreferrer">
                                    Ver Enlace
                                </a>
                            ) : 'N/A'}
                        </p>
                        <p><strong>Tiempo Límite:</strong> {evaluacion.tiempo_limite ? `${evaluacion.tiempo_limite} minutos` : 'N/A'}</p>
                        <p><strong>Umbral de Aprobación:</strong> {evaluacion.umbral_aprobacion ? `${evaluacion.umbral_aprobacion}%` : 'N/A'}</p>
                        <p><strong>Estado:</strong> {evaluacion.estado ? 'Activa' : 'Inactiva'}</p>
                        <p><strong>Tipo de Evaluación:</strong> {evaluacion.tipo_evaluacion}</p>
                        {evaluacion.empresa_nombre && <p><strong>Empresa:</strong> {evaluacion.empresa_nombre}</p>}
                        {evaluacion.creado_por_nombre && <p><strong>Creado por:</strong> {evaluacion.creado_por_nombre}</p>}
                        {evaluacion.fecha_registro && <p><strong>Fecha de Registro:</strong> {new Date(evaluacion.fecha_registro).toLocaleDateString()}</p>}
                        {evaluacion.fecha_modificacion && <p><strong>Última Modificación:</strong> {new Date(evaluacion.fecha_modificacion).toLocaleDateString()}</p>}
                    </section>

                    <section className="preview-section">
                        <h4 className="preview-section-title">Secciones de la Evaluación</h4>
                        {evaluacion.secciones.length === 0 ? (
                            <p>Esta evaluación no tiene secciones definidas.</p>
                        ) : (
                            evaluacion.secciones
                                .sort((a, b) => a.numero_orden - b.numero_orden) // Asegura el orden
                                .map((seccion: SeccionEval, seccionIndex: number) => (
                                <div key={seccion.seccion_id || seccionIndex} className="seccion-preview-card card">
                                    <div className="seccion-preview-header">
                                        <h5>{seccion.numero_orden}. {seccion.nombre}</h5>
                                        <span className={`badge ${seccion.es_evaluable ? 'badge-evaluable' : 'badge-no-evaluable'}`}>
                                            {seccion.es_evaluable ? 'Evaluable' : 'No Evaluable'}
                                        </span>
                                    </div>
                                    {seccion.descripcion && <p className="seccion-description">{seccion.descripcion}</p>}

                                    <h6 className="preguntas-sub-title">Preguntas:</h6>

                                    {seccion.preguntas_seccion.length === 0 ? (
                                        <p>Esta sección no tiene preguntas.</p>
                                    ) : (
                                        <ul className="preguntas-preview-list">
                                            {seccion.preguntas_seccion
                                                .sort((a, b) => a.numero_orden - b.numero_orden) // Asegura el orden
                                                .map((sp: SeccionPregunta, preguntaIndex: number) => (
                                                <li key={sp.seccion_pregunta_id || preguntaIndex} className="pregunta-preview-item">
                                                    <p>
                                                        <strong>{sp.numero_orden}.</strong> {sp.pregunta.texto_pregunta}
                                                        <span className="pregunta-type"> ({sp.pregunta.tipo_pregunta})</span>
                                                        <span className={`badge ${sp.pregunta.es_obligatoria ? 'badge-obligatoria' : 'badge-opcional'}`}>
                                                            {sp.pregunta.es_obligatoria ? 'Obligatoria' : 'Opcional'}
                                                        </span>
                                                    </p>
                                                    {sp.conjunto_respuestas && sp.conjunto_respuestas.opciones && (
                                                        <div className="opciones-preview">
                                                            <strong>Opciones:</strong>
                                                            <ul>
                                                                {sp.conjunto_respuestas.opciones.map((opcion: PosiblesRespuestas) => (
                                                                    <li key={opcion.opcion_conjunto_id}>
                                                                        {opcion.texto_opcion}
                                                                        {/* Muestra "(Correcta)" si esta es la opción de respuesta correcta */}
                                                                        {sp.respuesta_correcta && sp.respuesta_correcta.opcion_conjunto_id === opcion.opcion_conjunto_id && (
                                                                            <span className="badge badge-correcta"> (Correcta)</span>
                                                                        )}
                                                                    </li>
                                                                ))}
                                                            </ul>
                                                        </div>
                                                    )}
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>
                            )))}
                    </section>
                </div>
            </div>
        </div>
    );
};

export default EvaluacionPrevia;
