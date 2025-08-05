import React, { useState, useEffect } from 'react';
import './EvaluacionFormulario.css';


import evaluacionesAPI, {
    Evaluacion,
    EvaluacionRequest,
    TipoEvaluacion,
    Pregunta,
    PreguntaRequest,
    SeccionEval,
    SeccionEvalRequest,
    SeccionPregunta,
    SeccionPreguntaRequest,
    ConjuntoRespuestas,
    PosiblesRespuestas,
    ConjuntoRespuestasRequest,
    PosiblesRespuestasRequest,
} from '../../services/evaluacionesService';

// Interfaces actualizadas para reflejar la estructura del formulario
interface OpcionRespuestaForm {
    texto_opcion: string;
    valor_booleano?: boolean | null;
    valor_numerico?: number | null;
    valor_decimal?: number | null;
    numero_orden?: number;
}

// Definimos los tipos literales para tipo_pregunta basados en tus modelos de Django
type TipoPreguntaLiteral = "Abierta" | "Múltiple" | "Escala" | "Bool";

interface PreguntaFormState {
    texto_pregunta: string;
    tipo_pregunta: TipoPreguntaLiteral; // Usamos el tipo literal aquí
    es_obligatoria: boolean;
    // Para preguntas de tipo Múltiple/Escala/Bool, este ID se llenará
    // ya sea con un conjunto predefinido o con uno nuevo creado
    conjunto_respuestas_id: number | null;
    opciones_nuevas: OpcionRespuestaForm[]; // Para crear un nuevo conjunto (tipo Múltiple)
    respuesta_correcta: string | number | null; // Acepta string (para nuevas opciones) o number (para IDs)
}

// -------------------------------------------------------------------------- //
// Componente para crear una nueva pregunta
// -------------------------------------------------------------------------- //
interface AgregarPreguntaFormProps {
    seccionIndex: number;
    // onAddPregunta ahora recibe la pregunta creada por la API y la SeccionPreguntaRequest
    onAddPregunta: (seccionIndex: number, preguntaDataToCreate: PreguntaRequest, seccionPregunta: SeccionPreguntaRequest) => void;
    conjuntosDisponibles: ConjuntoRespuestas[];
    onCloseForm: () => void; // Para cerrar el formulario de agregar pregunta
}

const AgregarPreguntaForm: React.FC<AgregarPreguntaFormProps> = ({
    seccionIndex,
    onAddPregunta,
    conjuntosDisponibles,
    onCloseForm,
}) => {
    const [preguntaForm, setPreguntaForm] = useState<PreguntaFormState>({
        texto_pregunta: '',
        tipo_pregunta: 'Abierta',
        es_obligatoria: true,
        conjunto_respuestas_id: null,
        opciones_nuevas: [],
        respuesta_correcta: null,
    });
    const [isSaving, setIsSaving] = useState(false);

    // Efecto para manejar la lógica de conjunto de respuestas según el tipo de pregunta
    useEffect(() => {
        const updateConjuntoId = () => {
            let newConjuntoId: number | null = null;
            if (preguntaForm.tipo_pregunta === 'Escala') {
                newConjuntoId = 1; // ID para 'Escala'
            } else if (preguntaForm.tipo_pregunta === 'Bool') {
                newConjuntoId = 2; // ID para 'Bool' (Sí/No)
            }
            setPreguntaForm(prev => ({
                ...prev,
                conjunto_respuestas_id: newConjuntoId,
                opciones_nuevas: [], // Resetear opciones si cambia a tipo con conjunto predefinido
                respuesta_correcta: null,
            }));
        };

        updateConjuntoId();
    }, [preguntaForm.tipo_pregunta]);

    const handlePreguntaInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        // Manejar 'checked' solo si el target es un HTMLInputElement (para checkboxes)
        const checked = (e.target instanceof HTMLInputElement && e.target.type === 'checkbox') ? e.target.checked : undefined;

        setPreguntaForm(prev => ({
            ...prev,
            [name]: typeof checked === 'boolean' ? checked : value,
        }));
    };

    const handleAddOpcion = () => {
        setPreguntaForm(prev => ({
            ...prev,
            opciones_nuevas: [...prev.opciones_nuevas, { texto_opcion: '', numero_orden: prev.opciones_nuevas.length + 1 }],
        }));
    };

    const handleOpcionChange = (index: number, value: string) => {
        const updatedOpciones = [...preguntaForm.opciones_nuevas];
        updatedOpciones[index].texto_opcion = value;
        setPreguntaForm(prev => ({ ...prev, opciones_nuevas: updatedOpciones }));
    };

    const handleRemoveOpcion = (index: number) => {
        const updatedOpciones = preguntaForm.opciones_nuevas.filter((_, i) => i !== index);
        setPreguntaForm(prev => ({ ...prev, opciones_nuevas: updatedOpciones.map((opt, i) => ({ ...opt, numero_orden: i + 1 })) }));
    };

    const handleSavePregunta = async () => {
        setIsSaving(true);
        try {
            const { texto_pregunta, tipo_pregunta, es_obligatoria, conjunto_respuestas_id, opciones_nuevas, respuesta_correcta } = preguntaForm;

            if (!texto_pregunta) {
                // Reemplazado alert con un mensaje en la consola o un modal personalizado
                console.error('El texto de la pregunta es obligatorio.');
                // Aquí podrías mostrar un modal o un mensaje en el UI
                setIsSaving(false);
                return;
            }

            let finalConjuntoRespuestasId = conjunto_respuestas_id;
            let finalRespuestaCorrectaId: number | null = null;

            // Lógica para crear un nuevo conjunto de respuestas si el tipo es 'Múltiple'
            if (tipo_pregunta === 'Múltiple' && opciones_nuevas.length > 0) {
                const newConjuntoData: ConjuntoRespuestasRequest = {
                    nombre: `Respuestas a pregunta: ${texto_pregunta.substring(0, 50)}...`, // Nombre descriptivo
                    descripcion: `Conjunto de respuestas para la pregunta: "${texto_pregunta}"`,
                    opciones: opciones_nuevas.map((op, idx) => ({ ...op, numero_orden: idx + 1 })),
                };
                const createdConjunto = await evaluacionesAPI.createConjuntoRespuestas(newConjuntoData);
                finalConjuntoRespuestasId = createdConjunto.data.conjunto_id;

                // Si se seleccionó una respuesta correcta de las nuevas opciones, encontrar su ID
                if (typeof respuesta_correcta === 'string' && createdConjunto.data.opciones) {
                    const foundOption = createdConjunto.data.opciones.find(opt => opt.texto_opcion === respuesta_correcta);
                    finalRespuestaCorrectaId = foundOption?.opcion_conjunto_id || null;
                }
            } else if (['Múltiple', 'Escala', 'Bool'].includes(tipo_pregunta) && !finalConjuntoRespuestasId) {
                // Reemplazado alert con un mensaje en la consola o un modal personalizado
                console.error('Debe seleccionar o crear un conjunto de respuestas para este tipo de pregunta.');
                // Aquí podrías mostrar un modal o un mensaje en el UI
                setIsSaving(false);
                return;
            } else if (typeof respuesta_correcta === 'number') {
                // Si la respuesta correcta ya es un ID (para conjuntos predefinidos)
                finalRespuestaCorrectaId = respuesta_correcta;
            }


            const newPreguntaData: PreguntaRequest = {
                texto_pregunta,
                tipo_pregunta,
                es_obligatoria,
                pregunta_padre: null,
                activador_padre: null,
            };

            const tempSeccionPregunta: SeccionPreguntaRequest = {
                pregunta_id: -1, // Placeholder, el ID real se asignará después de crear la pregunta
                numero_orden: 0, // Placeholder, el orden real se asignará en el padre
                conjunto_respuestas_id: finalConjuntoRespuestasId,
                respuesta_correcta: finalRespuestaCorrectaId, // Usar el ID final aquí
            };

            // Llamar a la función del padre para añadir la pregunta
            onAddPregunta(seccionIndex, newPreguntaData, tempSeccionPregunta);
            onCloseForm(); // Cerrar el formulario de agregar pregunta
        } catch (error) {
            console.error('Error al guardar la pregunta o el conjunto de respuestas:', error);
            // Aquí podrías mostrar un modal o un mensaje en el UI
        } finally {
            setIsSaving(false);
        }
    };

    const opcionesParaRespuestaCorrecta = preguntaForm.conjunto_respuestas_id
        ? conjuntosDisponibles.find(c => c.conjunto_id === preguntaForm.conjunto_respuestas_id)?.opciones || []
        : preguntaForm.opciones_nuevas; // Si es un nuevo conjunto, usar las opciones que el usuario está creando

    return (
        <div className="add-pregunta-form-container">
            <h4 className="form-section-title">Nueva Pregunta</h4>
            <div className="form-row">
                <div className="form-group flex-grow">
                    <label htmlFor="preguntaTexto">Texto de la Pregunta</label>
                    <textarea
                        id="preguntaTexto"
                        name="texto_pregunta"
                        value={preguntaForm.texto_pregunta}
                        onChange={handlePreguntaInputChange}
                        required
                        rows={3}
                    />
                </div>
            </div>
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="tipoPregunta">Tipo de Pregunta</label>
                    <select id="tipoPregunta" name="tipo_pregunta" value={preguntaForm.tipo_pregunta} onChange={handlePreguntaInputChange}>
                        <option value="Abierta">Abierta</option>
                        <option value="Múltiple">Múltiple</option>
                        <option value="Escala">Escala</option>
                        <option value="Bool">Sí/No</option>
                    </select>
                </div>
                <div className="form-group boolean-toggle">
                    <label htmlFor="esObligatoria">Obligatoria</label>
                    <label className="switch">
                        <input
                            type="checkbox"
                            id="esObligatoria"
                            name="es_obligatoria"
                            checked={preguntaForm.es_obligatoria}
                            onChange={handlePreguntaInputChange}
                        />
                        <span className="slider round"></span>
                    </label>
                </div>
            </div>

            {/* Campos para Conjuntos de Respuestas (Múltiple, Escala, Bool) */}
            {['Múltiple', 'Escala', 'Bool'].includes(preguntaForm.tipo_pregunta) && (
                <div className="options-section">
                    {preguntaForm.tipo_pregunta === 'Múltiple' ? (
                        <div className="form-group">
                            <label>Opciones de Respuesta Personalizadas</label>
                            <div className="opciones-container">
                                {preguntaForm.opciones_nuevas.map((opcion, index) => (
                                    <div key={index} className="form-group-inline option-item">
                                        <input
                                            type="text"
                                            value={opcion.texto_opcion}
                                            onChange={(e) => handleOpcionChange(index, e.target.value)}
                                            placeholder={`Opción ${index + 1}`}
                                            required
                                        />
                                        <button type="button" className="btn-icon-remove" onClick={() => handleRemoveOpcion(index)}>
                                            <i className="fas fa-minus-circle"></i>
                                        </button>
                                    </div>
                                ))}
                                <button type="button" className="btn-add-option" onClick={handleAddOpcion}>
                                    ➕ Agregar Opción
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="form-group">
                            <label>Conjunto de Respuestas Predefinido</label>
                            <input
                                type="text"
                                value={conjuntosDisponibles.find(c => c.conjunto_id === preguntaForm.conjunto_respuestas_id)?.nombre || ''}
                                disabled
                                className="disabled-input"
                            />
                        </div>
                    )}

                    {/* Selector de Respuesta Correcta */}
                    {opcionesParaRespuestaCorrecta.length > 0 && (
                        <div className="form-group">
                            <label htmlFor="respuestaCorrecta">Respuesta Correcta</label>
                            <select
                                id="respuestaCorrecta"
                                name="respuesta_correcta"
                                value={preguntaForm.respuesta_correcta || ''}
                                onChange={handlePreguntaInputChange}
                            >
                                <option value="">Seleccione...</option>
                                {opcionesParaRespuestaCorrecta.map((opcion: PosiblesRespuestas | OpcionRespuestaForm, index: number) => (
                                    <option
                                        key={(opcion as PosiblesRespuestas).opcion_conjunto_id || index}
                                        value={(opcion as PosiblesRespuestas).opcion_conjunto_id || (opcion as OpcionRespuestaForm).texto_opcion}
                                    >
                                        {opcion.texto_opcion}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}
                </div>
            )}

            <div className="form-actions-small">
                <button type="button" className="btn-primary" onClick={handleSavePregunta} disabled={isSaving}>
                    {isSaving ? 'Guardando...' : 'Guardar Pregunta'}
                </button>
                <button type="button" className="btn-secondary" onClick={onCloseForm} disabled={isSaving}>
                    Cancelar
                </button>
            </div>
        </div>
    );
};

// -------------------------------------------------------------------------- //
// Componente para manejar la visualización y edición de preguntas ya añadidas
// -------------------------------------------------------------------------- //
interface PreguntaFormItemProps {
    pregunta: SeccionPreguntaRequest;
    preguntaData: Pregunta;
    conjuntosDisponibles: ConjuntoRespuestas[];
    onUpdate: (updatedPregunta: SeccionPreguntaRequest) => void;
    onRemove: () => void;
}

const PreguntaFormItem: React.FC<PreguntaFormItemProps> = ({
    pregunta,
    preguntaData,
    conjuntosDisponibles,
    onUpdate,
    onRemove,
}) => {
    const conjuntoRespuestas = conjuntosDisponibles.find(c => c.conjunto_id === pregunta.conjunto_respuestas_id);

    const handleRespuestaCorrectaChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedOptionId = e.target.value === '' ? null : Number(e.target.value);
        onUpdate({
            ...pregunta,
            respuesta_correcta: selectedOptionId,
        });
    };

    // Obtener el texto de la respuesta correcta si está seleccionada
    const respuestaCorrectaTexto = conjuntoRespuestas?.opciones?.find(
        opt => opt.opcion_conjunto_id === pregunta.respuesta_correcta
    )?.texto_opcion || '';

    return (
        <li className="pregunta-form-item card"> {/* Añadimos la clase 'card' */}
            <div className="pregunta-header">
                <span className="pregunta-order">{pregunta.numero_orden}.</span>
                <span className="pregunta-text">{preguntaData.texto_pregunta}</span>
                <span className="pregunta-type">({preguntaData.tipo_pregunta})</span>
                <button type="button" className="btn-icon-remove" onClick={onRemove}>
                    <i className="fas fa-trash"></i>
                </button>
            </div>

            {conjuntoRespuestas && conjuntoRespuestas.opciones && conjuntoRespuestas.opciones.length > 0 && (
                <div className="pregunta-details">
                    <div className="form-group-inline">
                        <label>Respuesta Correcta:</label>
                        <select
                            value={pregunta.respuesta_correcta || ''}
                            onChange={handleRespuestaCorrectaChange}
                        >
                            <option value="">Seleccione...</option>
                            {conjuntoRespuestas.opciones.map((opcion: PosiblesRespuestas) => (
                                <option key={opcion.opcion_conjunto_id} value={opcion.opcion_conjunto_id}>
                                    {opcion.texto_opcion}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            )}
            {/* Mostrar el estado de obligatoria de manera elegante */}
            <div className="pregunta-meta">
                <span className={`badge ${preguntaData.es_obligatoria ? 'badge-obligatoria' : 'badge-opcional'}`}>
                    {preguntaData.es_obligatoria ? 'Obligatoria' : 'Opcional'}
                </span>
                {respuestaCorrectaTexto && (
                    <span className="badge badge-correcta">
                        Correcta: {respuestaCorrectaTexto}
                    </span>
                )}
            </div>
        </li>
    );
};

// -------------------------------------------------------------------------- //
// Componente principal del formulario
// -------------------------------------------------------------------------- //
interface EvaluacionFormularioProps {
    evaluacion: Evaluacion | null;
    onClose: () => void;
    tiposEvaluacion: TipoEvaluacion[];
    user: { nivel_usuario: string; empresa_id?: number; user_id?: number };
}

const EvaluacionFormulario: React.FC<EvaluacionFormularioProps> = ({ evaluacion, onClose, tiposEvaluacion, user }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<Partial<EvaluacionRequest>>({
        titulo: '',
        descripcion: '',
        tipo_evaluacion_id: undefined,
        secciones: [],
    });
    const [conjuntosDisponibles, setConjuntosDisponibles] = useState<ConjuntoRespuestas[]>([]);
    const [preguntasDeEvaluacion, setPreguntasDeEvaluacion] = useState<{ [key: number]: Pregunta }>({});
    const [showAddPreguntaFormIndex, setShowAddPreguntaFormIndex] = useState<number | null>(null);

    useEffect(() => {
        const fetchRecursos = async () => {
            try {
                const conjuntosRes = await evaluacionesAPI.getConjuntosRespuestas();
                setConjuntosDisponibles(conjuntosRes.data);
            } catch (error) {
                console.error('Error al obtener conjuntos:', error);
            }
        };
        fetchRecursos();
    }, []);

    useEffect(() => {
        if (evaluacion) {
            const nuevasPreguntasMap: { [key: number]: Pregunta } = {};
            evaluacion.secciones.forEach((seccion: SeccionEval) => {
                seccion.preguntas_seccion.forEach((sp: SeccionPregunta) => {
                    nuevasPreguntasMap[sp.pregunta.pregunta_id] = sp.pregunta;
                });
            });
            setPreguntasDeEvaluacion(nuevasPreguntasMap);

            setFormData({
                titulo: evaluacion.titulo,
                descripcion: evaluacion.descripcion,
                instrucciones: evaluacion.instrucciones,
                contenido_informativo: evaluacion.contenido_informativo,
                tiempo_limite: evaluacion.tiempo_limite,
                umbral_aprobacion: evaluacion.umbral_aprobacion,
                estado: evaluacion.estado,
                tipo_evaluacion_id: evaluacion.tipo_evaluacion_id,
                secciones: evaluacion.secciones.map((seccion: SeccionEval) => ({
                    seccion_id: seccion.seccion_id,
                    nombre: seccion.nombre,
                    descripcion: seccion.descripcion,
                    numero_orden: seccion.numero_orden,
                    es_evaluable: seccion.es_evaluable,
                    preguntas_seccion: seccion.preguntas_seccion.map((sp: SeccionPregunta) => ({
                        seccion_pregunta_id: sp.seccion_pregunta_id,
                        pregunta_id: sp.pregunta.pregunta_id,
                        numero_orden: sp.numero_orden,
                        conjunto_respuestas_id: sp.conjunto_respuestas?.conjunto_id || null,
                        respuesta_correcta: sp.respuesta_correcta,
                    })),
                })),
                // Al editar, los IDs de empresa y creado_por ya vienen en el objeto evaluacion
                // y no necesitan ser enviados en el PUT a menos que se cambien.
                // Sin embargo, para consistencia con la interfaz, podemos incluirlos si están presentes.
                empresa_id: evaluacion.empresa_id,
                creado_por_id: user?.user_id,
            });
        } else {
            const tipoPornivel_usuario = user?.nivel_usuario === 'superadmin'
                ? tiposEvaluacion.find((t: TipoEvaluacion) => t.nombre.toLowerCase() === 'normativa')?.tipo_evaluacion_id
                : tiposEvaluacion.find((t: TipoEvaluacion) => t.nombre.toLowerCase() === 'interna')?.tipo_evaluacion_id;

            setFormData({
                titulo: '',
                descripcion: '',
                instrucciones: '',
                contenido_informativo: '',
                tiempo_limite: null,
                umbral_aprobacion: null,
                estado: true,
                tipo_evaluacion_id: tipoPornivel_usuario,
                secciones: [],
                // Al crear, estos campos se establecen por el nivel de usuario
                empresa_id: user?.nivel_usuario !== 'superadmin' ? user?.empresa_id : null,
                creado_por_id: user?.user_id,
            });
            setPreguntasDeEvaluacion({});
        }
    }, [evaluacion, tiposEvaluacion, user]);


    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>, field: keyof EvaluacionRequest) => {
        let value: string | number | boolean | null = e.target.value;
        if (field === 'tiempo_limite' || field === 'umbral_aprobacion') {
            value = value === '' ? null : Number(value);
        } else if (field === 'estado') {
            value = (e.target as HTMLInputElement).checked;
        }
        setFormData({ ...formData, [field]: value });
    };

    const handleSeccionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>, seccionIndex: number, field: keyof SeccionEvalRequest) => {
        const updatedSecciones = [...formData.secciones!];
        let value: string | number | boolean | null;

        if (field === 'es_evaluable') {
            value = (e.target as HTMLInputElement).checked;
        } else {
            value = e.target.value;
        }
        updatedSecciones[seccionIndex] = {
            ...updatedSecciones[seccionIndex],
            [field]: value,
        };
        setFormData({ ...formData, secciones: updatedSecciones });
    };

    const handleAddSeccion = () => {
        const newSeccion: SeccionEvalRequest = {
            nombre: `Nueva Sección ${formData.secciones!.length + 1}`,
            numero_orden: formData.secciones!.length + 1,
            es_evaluable: true,
            preguntas_seccion: [],
        };
        setFormData({
            ...formData,
            secciones: [...formData.secciones!, newSeccion],
        });
    };

    const handleRemoveSeccion = (seccionIndex: number) => {
        const updatedSecciones = formData.secciones!.filter((_, index) => index !== seccionIndex);
        setFormData({ ...formData, secciones: updatedSecciones.map((s, i) => ({ ...s, numero_orden: i + 1 })) });
    };

    const handleAddPreguntaToSection = async (seccionIndex: number, newPreguntaData: PreguntaRequest, tempSeccionPregunta: SeccionPreguntaRequest) => {
        try {
            const res = await evaluacionesAPI.createPregunta(newPreguntaData);
            const preguntaCreada: Pregunta = res.data;

            setPreguntasDeEvaluacion(prev => ({
                ...prev,
                [preguntaCreada.pregunta_id]: preguntaCreada,
            }));

            const updatedSecciones = [...formData.secciones!];
            updatedSecciones[seccionIndex].preguntas_seccion.push({
                ...tempSeccionPregunta,
                pregunta_id: preguntaCreada.pregunta_id,
                numero_orden: updatedSecciones[seccionIndex].preguntas_seccion.length + 1,
            });
            setFormData({ ...formData, secciones: updatedSecciones });
            setShowAddPreguntaFormIndex(null);
        } catch (error) {
            console.error('Error al crear la pregunta y añadirla a la sección:', error);
            // Aquí podrías mostrar un modal o un mensaje en el UI
        }
    };

    const handleUpdatePregunta = (seccionIndex: number, preguntaIndex: number, updatedPregunta: SeccionPreguntaRequest) => {
        const updatedSecciones = [...formData.secciones!];
        updatedSecciones[seccionIndex].preguntas_seccion[preguntaIndex] = updatedPregunta;
        setFormData({ ...formData, secciones: updatedSecciones });
    };

    const handleRemovePregunta = (seccionIndex: number, preguntaIndex: number) => {
        const updatedSecciones = [...formData.secciones!];
        updatedSecciones[seccionIndex].preguntas_seccion = updatedSecciones[seccionIndex].preguntas_seccion.filter((_, index) => index !== preguntaIndex);
        updatedSecciones[seccionIndex].preguntas_seccion = updatedSecciones[seccionIndex].preguntas_seccion.map((p, i) => ({ ...p, numero_orden: i + 1 }));
        setFormData({ ...formData, secciones: updatedSecciones });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Se crea una copia mutable de formData para añadir los IDs
            const dataToSubmit: EvaluacionRequest = { ...formData } as EvaluacionRequest;

            // Lógica para asignar empresa_id y creado_por_id
            if (user.nivel_usuario === 'superadmin') {
                dataToSubmit.creado_por_id = user.user_id;
                dataToSubmit.empresa_id = null; // Las evaluaciones normativas no están ligadas a una empresa específica
            } else if (user.nivel_usuario === 'admin-empresa' || user.nivel_usuario === 'admin-planta') {
                dataToSubmit.creado_por_id = user.user_id;
                dataToSubmit.empresa_id = user.empresa_id || null; // Asegura que empresa_id se envíe si está disponible
            }
            // Si el usuario es de otro tipo o no está autenticado, estos campos pueden ser null o no enviados
            // según la lógica de tu backend y si son obligatorios o no.

            const seccionesSinPreguntas = dataToSubmit.secciones?.some(s => s.es_evaluable && s.preguntas_seccion.length === 0);
            if (seccionesSinPreguntas) {
                // Reemplazado alert con un mensaje en la consola o un modal personalizado
                console.error('Las secciones evaluables deben tener al menos una pregunta.');
                // Aquí podrías mostrar un modal o un mensaje en el UI
                setLoading(false);
                return;
            }

            if (evaluacion && evaluacion.evaluacion_id) {
                await evaluacionesAPI.updateEvaluacion(evaluacion.evaluacion_id, dataToSubmit);
                // Reemplazado alert con un mensaje en la consola o un modal personalizado
                console.log('Evaluación actualizada con éxito.');
            } else {
                await evaluacionesAPI.createEvaluacion(dataToSubmit);
                // Reemplazado alert con un mensaje en la consola o un modal personalizado
                console.log('Evaluación creada con éxito.');
            }
            onClose();
        } catch (error) {
            console.error('Error al guardar la evaluación:', error);
            // Aquí podrías mostrar un modal o un mensaje en el UI
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header-custom">
                    <h3 className="modal-title">{evaluacion ? '✏️ Editar Evaluación' : '➕ Crear Evaluación'}</h3>
                    <div className="modal-actions-top">
                        <button type="button" className="btn-secondary btn-volver" onClick={onClose}>
                            <i className="fas fa-arrow-left"></i> Volver
                        </button>
                        <button type="submit" className="btn-primary btn-guardar" form="evaluacionForm" disabled={loading}>
                            {loading ? 'Guardando...' : 'Guardar'}
                        </button>
                    </div>
                </div>
                <form id="evaluacionForm" onSubmit={handleSubmit}>
                    <section className="form-section">
                        <h4 className="form-section-title">Información General</h4>
                        <div className="form-row">
                            <div className="form-group flex-grow">
                                <label htmlFor="titulo">Nombre de la Evaluación</label>
                                <input type="text" id="titulo" value={formData.titulo || ''} onChange={(e) => handleInputChange(e, 'titulo')} required />
                            </div>
                            <div className="form-group">
                                <label htmlFor="tipoEvaluacion">Tipo de Evaluación</label>
                                <input
                                    type="text"
                                    id="tipoEvaluacion"
                                    value={tiposEvaluacion.find((t: TipoEvaluacion) => t.tipo_evaluacion_id === formData.tipo_evaluacion_id)?.nombre || ''}
                                    disabled
                                    className="disabled-input"
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label htmlFor="descripcion">Descripción</label>
                            <textarea id="descripcion" value={formData.descripcion || ''} onChange={(e) => handleInputChange(e, 'descripcion')} rows={3} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="instrucciones">Instrucciones</label>
                            <textarea id="instrucciones" value={formData.instrucciones || ''} onChange={(e) => handleInputChange(e, 'instrucciones')} rows={3} />
                        </div>
                        <div className="form-row">
                            <div className="form-group flex-grow">
                                <label htmlFor="contenidoInformativo">Contenido Informativo (URL)</label>
                                <input type="text" id="contenidoInformativo" value={formData.contenido_informativo || ''} onChange={(e) => handleInputChange(e, 'contenido_informativo')} />
                            </div>
                            <div className="form-group">
                                <label htmlFor="tiempoLimite">Tiempo Límite (minutos)</label>
                                <input type="number" id="tiempoLimite" min={0} max={240} value={formData.tiempo_limite || ''} onChange={(e) => handleInputChange(e, 'tiempo_limite')} />
                            </div>
                            <div className="form-group">
                                <label htmlFor="umbralAprobacion">Umbral de Aprobación (%)</label>
                                <input type="number" id="umbralAprobacion" min={0} max={100} value={formData.umbral_aprobacion || ''} onChange={(e) => handleInputChange(e, 'umbral_aprobacion')} />
                            </div>
                            <div className="form-group boolean-toggle">
                                <label htmlFor="estadoEvaluacion">Estado</label>
                                <label className="switch">
                                    <input type="checkbox" id="estadoEvaluacion" checked={formData.estado || false} onChange={(e) => handleInputChange(e, 'estado')} />
                                    <span className="slider round"></span>
                                </label>
                            </div>
                        </div>
                    </section>

                    <section className="form-section">
                        <h4 className="form-section-title">Secciones <button type="button" onClick={handleAddSeccion} className="btn-add-seccion">➕ Agregar Sección</button></h4>
                        {formData.secciones?.map((seccion, seccionIndex) => (
                            <div key={seccionIndex} className="seccion-container card">
                                <div className="seccion-header">
                                    <input
                                        type="text"
                                        className="seccion-title"
                                        value={seccion.nombre}
                                        onChange={(e) => handleSeccionChange(e, seccionIndex, 'nombre')}
                                        required
                                    />
                                    <button type="button" onClick={() => handleRemoveSeccion(seccionIndex)} className="btn-icon-remove">
                                        <i className="fas fa-trash"></i>
                                    </button>
                                </div>
                                <div className="form-row">
                                    <div className="form-group flex-grow">
                                        <label htmlFor={`descripcionSeccion-${seccionIndex}`}>Descripción de Sección (Opcional)</label>
                                        <textarea
                                            id={`descripcionSeccion-${seccionIndex}`}
                                            value={seccion.descripcion || ''}
                                            onChange={(e) => handleSeccionChange(e as React.ChangeEvent<HTMLTextAreaElement>, seccionIndex, 'descripcion')}
                                            placeholder="Descripción de la sección (opcional)"
                                            rows={2}
                                        />
                                    </div>
                                    <div className="form-group boolean-toggle">
                                        <label htmlFor={`esEvaluable-${seccionIndex}`}>Es evaluable</label>
                                        <label className="switch">
                                            <input
                                                type="checkbox"
                                                id={`esEvaluable-${seccionIndex}`}
                                                checked={seccion.es_evaluable}
                                                onChange={(e) => handleSeccionChange(e, seccionIndex, 'es_evaluable')}
                                            />
                                            <span className="slider round"></span>
                                        </label>
                                    </div>
                                </div>

                                <ul className="preguntas-list">
                                    {seccion.preguntas_seccion.map((pregunta, preguntaIndex) => {
                                        const preguntaData = preguntasDeEvaluacion[pregunta.pregunta_id];
                                        if (!preguntaData) return null;
                                        return (
                                            <PreguntaFormItem
                                                key={pregunta.pregunta_id}
                                                pregunta={pregunta}
                                                preguntaData={preguntaData}
                                                conjuntosDisponibles={conjuntosDisponibles}
                                                onUpdate={(updatedPregunta) => handleUpdatePregunta(seccionIndex, preguntaIndex, updatedPregunta)}
                                                onRemove={() => handleRemovePregunta(seccionIndex, preguntaIndex)}
                                            />
                                        );
                                    })}
                                </ul>

                                {showAddPreguntaFormIndex === seccionIndex ? (
                                    <AgregarPreguntaForm
                                        seccionIndex={seccionIndex}
                                        onAddPregunta={handleAddPreguntaToSection}
                                        conjuntosDisponibles={conjuntosDisponibles}
                                        onCloseForm={() => setShowAddPreguntaFormIndex(null)}
                                    />
                                ) : (
                                    <button type="button" className="btn-add-pregunta" onClick={() => setShowAddPreguntaFormIndex(seccionIndex)}>
                                        ➕ Agregar Pregunta
                                    </button>
                                )}
                            </div>
                        ))}
                    </section>
                </form>
            </div>
        </div>
    );
};

export default EvaluacionFormulario;
