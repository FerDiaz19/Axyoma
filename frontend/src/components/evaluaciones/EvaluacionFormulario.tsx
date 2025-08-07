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
    numero_orden: number;
}

type TipoPreguntaLiteral = "Abierta" | "Múltiple" | "Escala" | "Bool";

interface PreguntaFormState {
    texto_pregunta: string;
    tipo_pregunta: TipoPreguntaLiteral;
    es_obligatoria: boolean;
    // Ahora puede ser ConjuntoRespuestas (con ID) o ConjuntoRespuestasRequest (sin ID)
    conjunto_respuestas?: ConjuntoRespuestasRequest | ConjuntoRespuestas;
    opciones_nuevas: OpcionRespuestaForm[];
    // Ahora puede ser PosiblesRespuestas (con ID) o PosiblesRespuestasRequest (sin ID)
    respuesta_correcta?: PosiblesRespuestas | OpcionRespuestaForm | null;
}

// -------------------------------------------------------------------------- //
// Componente para crear una nueva pregunta
// -------------------------------------------------------------------------- //
interface AgregarPreguntaFormProps {
    seccionIndex: number;
    onAddPregunta: (seccionIndex: number, seccionPregunta: SeccionPreguntaRequest) => void;
    conjuntosDisponibles: ConjuntoRespuestas[];
    onCloseForm: () => void;
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
        conjunto_respuestas: undefined,
        opciones_nuevas: [],
        respuesta_correcta: null,
    });
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        const updateConjunto = () => {
            let newConjunto: ConjuntoRespuestas | undefined;
            if (preguntaForm.tipo_pregunta === 'Escala') {
                newConjunto = conjuntosDisponibles.find(c => c.nombre.toLowerCase().includes('escala'));
            } else if (preguntaForm.tipo_pregunta === 'Bool') {
                newConjunto = conjuntosDisponibles.find(c => c.nombre.toLowerCase().includes('sí/no') || c.nombre.toLowerCase().includes('si/no'));
            }
            setPreguntaForm(prev => ({
                ...prev,
                conjunto_respuestas: newConjunto, // Asignamos el objeto ConjuntoRespuestas completo
                opciones_nuevas: [],
                respuesta_correcta: null,
            }));
        };

        updateConjunto();
    }, [preguntaForm.tipo_pregunta, conjuntosDisponibles]);

    const handlePreguntaInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
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

    const handleRespuestaCorrectaChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedValue = e.target.value;
        const opciones = preguntaForm.conjunto_respuestas?.opciones || preguntaForm.opciones_nuevas;

        const selectedOption = opciones.find(op => {
            // Si tiene opcion_conjunto_id (es una PosiblesRespuestas), compara por ID o texto
            if ((op as PosiblesRespuestas).opcion_conjunto_id !== undefined) {
                return String((op as PosiblesRespuestas).opcion_conjunto_id) === selectedValue || (op as PosiblesRespuestas).texto_opcion === selectedValue;
            }
            // Si no, es una OpcionRespuestaForm (nueva), compara por texto
            return (op as OpcionRespuestaForm).texto_opcion === selectedValue;
        });

        setPreguntaForm(prev => ({
            ...prev,
            respuesta_correcta: selectedOption || null,
        }));
    };

    const handleSavePregunta = () => {
        setIsSaving(true);
        try {
            const { texto_pregunta, tipo_pregunta, es_obligatoria, opciones_nuevas, respuesta_correcta, conjunto_respuestas } = preguntaForm;

            if (!texto_pregunta) {
                console.error('El texto de la pregunta es obligatorio.');
                setIsSaving(false);
                return;
            }

            const newPreguntaData: PreguntaRequest = {
                texto_pregunta,
                tipo_pregunta,
                es_obligatoria,
                pregunta_padre: null,
                activador_padre: null,
            };

            let finalConjuntoRespuestas: ConjuntoRespuestasRequest | ConjuntoRespuestas | null = null;
            let finalRespuestaCorrecta: PosiblesRespuestasRequest | PosiblesRespuestas | null = null;

            if (tipo_pregunta === 'Múltiple') {
                if (opciones_nuevas.length === 0) {
                    console.error('Las preguntas de tipo Múltiple deben tener al menos una opción.');
                    setIsSaving(false);
                    return;
                }
                // Para Múltiple, siempre creamos un nuevo ConjuntoRespuestasRequest
                finalConjuntoRespuestas = {
                    nombre: `Respuestas a pregunta: ${texto_pregunta.substring(0, 50)}...`,
                    descripcion: `Conjunto de respuestas para la pregunta: "${texto_pregunta}"`,
                    opciones: opciones_nuevas.map(op => ({
                        texto_opcion: op.texto_opcion,
                        valor_booleano: op.valor_booleano,
                        valor_numerico: op.valor_numerico,
                        valor_decimal: op.valor_decimal,
                        numero_orden: op.numero_orden,
                    })),
                };
                if (respuesta_correcta) {
                    // Para Múltiple, la respuesta correcta es una nueva PosiblesRespuestasRequest
                    const { texto_opcion, valor_booleano, valor_numerico, valor_decimal, numero_orden } = respuesta_correcta as OpcionRespuestaForm;
                    finalRespuestaCorrecta = { texto_opcion, valor_booleano, valor_numerico, valor_decimal, numero_orden: numero_orden || 0 };
                }
            } else if (['Escala', 'Bool'].includes(tipo_pregunta)) {
                if (!conjunto_respuestas) {
                    console.error(`No se encontró un conjunto de respuestas predefinido para el tipo "${tipo_pregunta}".`);
                    setIsSaving(false);
                    return;
                }
                // Para Escala/Bool, usamos el ConjuntoRespuestas predefinido directamente (con su ID y predefinido: true)
                finalConjuntoRespuestas = conjunto_respuestas as ConjuntoRespuestas;

                if (respuesta_correcta) {
                    // Para Escala/Bool, la respuesta correcta es una PosiblesRespuestas existente (con su ID)
                    finalRespuestaCorrecta = respuesta_correcta as PosiblesRespuestas;
                }
            }

            const seccionPreguntaToSubmit: SeccionPreguntaRequest = {
                pregunta: newPreguntaData,
                numero_orden: 0,
                conjunto_respuestas: finalConjuntoRespuestas,
                respuesta_correcta: finalRespuestaCorrecta,
            };

            onAddPregunta(seccionIndex, seccionPreguntaToSubmit);
            onCloseForm();
        } catch (error) {
            console.error('Error al preparar la pregunta:', error);
        } finally {
            setIsSaving(false);
        }
    };

    const opcionesParaRespuestaCorrecta = preguntaForm.tipo_pregunta === 'Múltiple'
        ? preguntaForm.opciones_nuevas
        : preguntaForm.conjunto_respuestas?.opciones || [];

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
                            onChange={(e) => setPreguntaForm(prev => ({ ...prev, es_obligatoria: e.target.checked }))}
                        />
                        <span className="slider round"></span>
                    </label>
                </div>
            </div>

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
                                value={preguntaForm.conjunto_respuestas?.nombre || ''}
                                disabled
                                className="disabled-input"
                            />
                        </div>
                    )}

                    {opcionesParaRespuestaCorrecta.length > 0 && (
                        <div className="form-group">
                            <label htmlFor="respuestaCorrecta">Respuesta Correcta</label>
                            <select
                                id="respuestaCorrecta"
                                name="respuesta_correcta"
                                value={preguntaForm.respuesta_correcta?.texto_opcion || ''}
                                onChange={handleRespuestaCorrectaChange}
                            >
                                <option value="">Seleccione...</option>
                                {opcionesParaRespuestaCorrecta.map((opcion: PosiblesRespuestas | OpcionRespuestaForm, index: number) => (
                                    <option
                                        key={(opcion as PosiblesRespuestas).opcion_conjunto_id || index}
                                        value={opcion.texto_opcion}
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
    conjuntosDisponibles: ConjuntoRespuestas[];
    onUpdate: (updatedPregunta: SeccionPreguntaRequest) => void;
    onRemove: () => void;
}

const PreguntaFormItem: React.FC<PreguntaFormItemProps> = ({
    pregunta,
    conjuntosDisponibles,
    onUpdate,
    onRemove,
}) => {
    // Cuando se edita, el conjunto_respuestas ya viene como ConjuntoRespuestasRequest si fue creado nuevo,
    // o como ConjuntoRespuestas si fue cargado de la API.
    // Necesitamos manejar ambos casos para mostrar las opciones correctamente.
    const conjuntoRespuestas = (pregunta.conjunto_respuestas as ConjuntoRespuestas) ||
        conjuntosDisponibles.find(c => c.conjunto_id === (pregunta.conjunto_respuestas as ConjuntoRespuestas)?.conjunto_id);

    const opcionesParaRespuestaCorrecta = conjuntoRespuestas?.opciones || [];

    const handleRespuestaCorrectaChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedValue = e.target.value;
        // Encuentra la opción seleccionada por su texto_opcion
        const selectedOption = opcionesParaRespuestaCorrecta.find(op => op.texto_opcion === selectedValue);

        // Crea un nuevo objeto de respuesta correcta en el formato PosiblesRespuestasRequest
        // Si el conjunto es predefinido, la opción también lo será y tendrá su ID
        let newRespuestaCorrecta: PosiblesRespuestasRequest | PosiblesRespuestas | null = null;
        if (selectedOption) {
            // Si la opción tiene opcion_conjunto_id, es una PosiblesRespuestas existente
            if ((selectedOption as PosiblesRespuestas).opcion_conjunto_id !== undefined) {
                newRespuestaCorrecta = selectedOption as PosiblesRespuestas;
            } else {
                // Si no, es una OpcionRespuestaForm (nueva), mapeamos a PosiblesRespuestasRequest
                const { texto_opcion, valor_booleano, valor_numerico, valor_decimal, numero_orden } = selectedOption;
                newRespuestaCorrecta = { texto_opcion, valor_booleano, valor_numerico, valor_decimal, numero_orden };
            }
        }

        onUpdate({
            ...pregunta,
            respuesta_correcta: newRespuestaCorrecta,
        });
    };

    // Obtener el texto de la respuesta correcta si está seleccionada
    const respuestaCorrectaTexto = (pregunta.respuesta_correcta as PosiblesRespuestas)?.texto_opcion || '';

    return (
        <li className="pregunta-form-item card">
            <div className="pregunta-header">
                <span className="pregunta-order">{pregunta.numero_orden}.</span>
                <span className="pregunta-text">{pregunta.pregunta.texto_pregunta}</span>
                <span className="pregunta-type">({pregunta.pregunta.tipo_pregunta})</span>
                <button type="button" className="btn-icon-remove" onClick={onRemove}>
                    <i className="fas fa-trash"></i>
                </button>
            </div>

            {opcionesParaRespuestaCorrecta.length > 0 && (
                <div className="pregunta-details">
                    <div className="form-group-inline">
                        <label>Respuesta Correcta:</label>
                        <select
                            value={(pregunta.respuesta_correcta as PosiblesRespuestas)?.texto_opcion || ''}
                            onChange={handleRespuestaCorrectaChange}
                        >
                            <option value="">Seleccione...</option>
                            {opcionesParaRespuestaCorrecta.map((opcion: PosiblesRespuestas) => (
                                <option key={opcion.opcion_conjunto_id} value={opcion.texto_opcion}>
                                    {opcion.texto_opcion}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            )}
            <div className="pregunta-meta">
                <span className={`badge ${pregunta.pregunta.es_obligatoria ? 'badge-obligatoria' : 'badge-opcional'}`}>
                    {pregunta.pregunta.es_obligatoria ? 'Obligatoria' : 'Opcional'}
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
    darkTheme?: boolean;
}

const EvaluacionFormulario: React.FC<EvaluacionFormularioProps> = ({ evaluacion, onClose, tiposEvaluacion, user, darkTheme = false }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<Partial<EvaluacionRequest>>({
        titulo: '',
        descripcion: '',
        tipo_evaluacion_id: undefined,
        secciones: [],
    });
    const [conjuntosDisponibles, setConjuntosDisponibles] = useState<ConjuntoRespuestas[]>([]);
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
                    seccion_id: seccion.seccion_id, // Mantener el ID para la edición
                    nombre: seccion.nombre,
                    descripcion: seccion.descripcion,
                    numero_orden: seccion.numero_orden,
                    es_evaluable: seccion.es_evaluable,
                    preguntas_seccion: seccion.preguntas_seccion.map((sp: SeccionPregunta) => ({
                        // CORRECCIÓN CLAVE: Ahora asignamos directamente los objetos completos
                        // ya que las interfaces *Request permiten los tipos completos (con IDs)
                        pregunta: sp.pregunta, // Ya es Pregunta, que extiende PreguntaRequest
                        numero_orden: sp.numero_orden,
                        conjunto_respuestas: sp.conjunto_respuestas, // Ya es ConjuntoRespuestas, que extiende ConjuntoRespuestasRequest
                        respuesta_correcta: sp.respuesta_correcta, // Ya es PosiblesRespuestas, que extiende PosiblesRespuestasRequest
                    })),
                })),
                empresa_id: evaluacion.empresa_id,
                creado_por_id: evaluacion.creado_por_id, // Mantener el creador original
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
                empresa_id: user?.nivel_usuario !== 'superadmin' ? user?.empresa_id : null,
                creado_por_id: user?.user_id,
            });
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

    const handleAddPreguntaToSection = (seccionIndex: number, newSeccionPregunta: SeccionPreguntaRequest) => {
        const updatedSecciones = [...formData.secciones!];
        newSeccionPregunta.numero_orden = updatedSecciones[seccionIndex].preguntas_seccion.length + 1;
        updatedSecciones[seccionIndex].preguntas_seccion.push(newSeccionPregunta);

        setFormData({ ...formData, secciones: updatedSecciones });
        setShowAddPreguntaFormIndex(null);
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
            const dataToSubmit: EvaluacionRequest = { ...formData,
                secciones: formData.secciones || [],
                titulo: formData.titulo || '',
                estado: formData.estado || false,
                tipo_evaluacion_id: formData.tipo_evaluacion_id || -1,
            };

            const seccionesSinPreguntas = dataToSubmit.secciones.some(s => s.es_evaluable && s.preguntas_seccion.length === 0);
            if (seccionesSinPreguntas) {
                console.error('Las secciones evaluables deben tener al menos una pregunta.');
                setLoading(false);
                return;
            }

            if (evaluacion && evaluacion.evaluacion_id) {
                await evaluacionesAPI.updateEvaluacion(evaluacion.evaluacion_id, dataToSubmit);
                console.log('Evaluación actualizada con éxito.');
            } else {
                await evaluacionesAPI.createEvaluacion(dataToSubmit);
                console.log('Evaluación creada con éxito.');
            }
            onClose();
        } catch (error) {
            console.error('Error al guardar la evaluación:', error);
            // Mostrar más detalles del error para debugging
            if (error instanceof Error && 'response' in error) {
                const axiosError = error as any;
                if (axiosError.response?.data) {
                    console.error('Detalles del error:', axiosError.response.data);
                }
                if (axiosError.response?.status === 400) {
                    console.error('Error 400 - Datos inválidos. Revisa los campos requeridos.');
                }
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={`modal-overlay ${darkTheme ? 'super-admin-theme' : ''}`}>
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
                        <div className="form-group">
                            <label htmlFor="contenido_informativo">Contenido informativo</label>
                            <textarea id="contenido_informativo" value={formData.contenido_informativo || ''} onChange={(e) => handleInputChange(e, 'contenido_informativo')} rows={3} />
                        </div>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="tiempo_limite">Tiempo Límite (minutos)</label>
                                <input type="number" id="tiempo_limite" value={formData.tiempo_limite || ''} onChange={(e) => handleInputChange(e, 'tiempo_limite')} />
                            </div>
                            <div className="form-group">
                                <label htmlFor="umbral_aprobacion">Umbral de Aprobación (%)</label>
                                <input type="number" id="umbral_aprobacion" value={formData.umbral_aprobacion || ''} onChange={(e) => handleInputChange(e, 'umbral_aprobacion')} />
                            </div>
                        </div>
                    </section>

                    <section className="form-section">
                        <h4 className="form-section-title">Secciones de la Evaluación</h4>
                        {formData.secciones!.map((seccion, seccionIndex) => (
                            <div key={seccionIndex} className="seccion-container card">
                                <div className="seccion-header">
                                    <div className="form-group flex-grow">
                                        <label>Nombre de la Sección</label>
                                        <input
                                            type="text"
                                            value={seccion.nombre}
                                            onChange={(e) => handleSeccionChange(e, seccionIndex, 'nombre')}
                                            required
                                        />
                                    </div>
                                    <button type="button" className="btn-icon-remove" onClick={() => handleRemoveSeccion(seccionIndex)}>
                                        <i className="fas fa-trash"></i>
                                    </button>
                                </div>
                                <div className="form-group">
                                    <label>Descripción de la Sección</label>
                                    <textarea
                                        value={seccion.descripcion || ''}
                                        onChange={(e) => handleSeccionChange(e, seccionIndex, 'descripcion')}
                                        rows={2}
                                    />
                                </div>
                                <div className="form-group boolean-toggle">
                                    <label htmlFor={`es_evaluable-${seccionIndex}`}>Es Evaluable</label>
                                    <label className="switch">
                                        <input
                                            type="checkbox"
                                            id={`es_evaluable-${seccionIndex}`}
                                            checked={seccion.es_evaluable}
                                            onChange={(e) => handleSeccionChange(e, seccionIndex, 'es_evaluable')}
                                        />
                                        <span className="slider round"></span>
                                    </label>
                                </div>

                                <div className="preguntas-section">
                                    <h5 className="form-section-title">Preguntas</h5>
                                    {seccion.preguntas_seccion.length > 0 ? (
                                        <ul className="preguntas-list">
                                            {seccion.preguntas_seccion.map((pregunta, preguntaIndex) => (
                                                <PreguntaFormItem
                                                    key={preguntaIndex}
                                                    pregunta={pregunta}
                                                    conjuntosDisponibles={conjuntosDisponibles}
                                                    onUpdate={(updatedPregunta) => handleUpdatePregunta(seccionIndex, preguntaIndex, updatedPregunta)}
                                                    onRemove={() => handleRemovePregunta(seccionIndex, preguntaIndex)}
                                                />
                                            ))}
                                        </ul>
                                    ) : (
                                        <p className="no-items-message">Esta sección no tiene preguntas.</p>
                                    )}
                                    {showAddPreguntaFormIndex !== seccionIndex && (
                                        <button type="button" className="btn-add-pregunta" onClick={() => setShowAddPreguntaFormIndex(seccionIndex)}>
                                            ➕ Añadir Pregunta
                                        </button>
                                    )}
                                    {showAddPreguntaFormIndex === seccionIndex && (
                                        <AgregarPreguntaForm
                                            seccionIndex={seccionIndex}
                                            onAddPregunta={handleAddPreguntaToSection}
                                            conjuntosDisponibles={conjuntosDisponibles}
                                            onCloseForm={() => setShowAddPreguntaFormIndex(null)}
                                        />
                                    )}
                                </div>
                            </div>
                        ))}
                        <button type="button" className="btn-add-seccion" onClick={handleAddSeccion}>
                            ➕ Añadir Sección
                        </button>
                    </section>
                </form>
            </div>
        </div>
    );
};

export default EvaluacionFormulario;
