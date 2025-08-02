
import { showModalMessage, backToTop } from './main.js';

// -------------------------------------------------------------------------- //

// Primero que nada, vamo' a asegurarnos que todo suceda tras cargar bien el contenido.
document.addEventListener('DOMContentLoaded', function() {

    // Botoncillos de navegación entre secciones.
    const tabButtons = document.querySelectorAll('.section-button');
    // Contenido de cada una de las secciones.
    const sectionContents = document.querySelectorAll('.section-content');

    // Botones de avanzar a la siguiente sección.
    const nextButtons = document.querySelectorAll('.next-section');
    // Botones para regresar a la sección anterior.
    const prevButtons = document.querySelectorAll('.prev-section');

    // Progreso de avance a lo largo de la evaluación.
    const sectionLabel = document.getElementById('section-label');
    const sectionPercent = document.getElementById('section-percent');
    const sectionProgressFill = document.getElementById('section-progress');

    // Preguntillas que dependen del resultado de otra.
    const dependentQuestions = document.querySelectorAll('.question-block[data-parent-question-id]');

    // * -------------------------------------------------------------------- //

    /*
        Esta función actualiza la etiqueta de sección y la barra de progreso.
    */
    function updateSectionProgress() {

        // Sección actual.
        const currentSection = document.querySelector('.section-content:not(.hidden)');
        if (!currentSection) return;

        // Índice actual de la sección.
        const currentSectionIndex = Array.from(sectionContents).indexOf(currentSection);
        const totalSections = sectionContents.length;

        // Actualizamo' la etiqueta de la sección.
        if (sectionLabel) {
            sectionLabel.textContent = `Sección ${currentSectionIndex + 1} de ${totalSections}`;
        };

        // Porcentaje de avance inicial.
        let progressPercentage = 0;

        // Cálculo sencillo de avance actual.
        if (totalSections > 0) {
            progressPercentage = (currentSectionIndex / totalSections) * 100;
        };

        // Actualizamo' el texto del porcentaje.
        if (sectionPercent) {
            sectionPercent.textContent = `${Math.round(progressPercentage)}%`;
        };

        // Y, por último, actualizamo' la barra de progreso.
        if (sectionProgressFill) {
            sectionProgressFill.style.width = `${progressPercentage}%`;
        };
    };

    // * -------------------------------------------------------------------- //

    /*
        Esta función muestra una sección específica y oculta el resto.
        * @param {string} sectionId - Hace referencia al ID de la sección a mostrar.

        Adicionalmente se actualiza el estado del botoncillo de la sección.
    */
    function showSection(sectionId) {

        // Primero ocultamo' todas las secciones.
        sectionContents.forEach(section => {
            section.classList.add('hidden');
        });

        // Posteriormente mostramos la sección especificada.
        document.getElementById(sectionId).classList.remove('hidden');

        // Marca cada uno de los botones como desactivados.
        tabButtons.forEach(button => {
            button.classList.remove('active');
        });

        // Y después, se marca como activo el botón de la sección mostrada.
        document.querySelector(`[data-section-id="${sectionId}"]`).classList.add('active');
        updateSectionProgress();
        backToTop();
    };

    // * -------------------------------------------------------------------- //

    /*
        Esta función valida todos los campos obligatorios dentro de una sección dada.
        * @param {HTMLElement} sectionElement - El elemento DOM de la sección a validar.
        * @returns {boolean} - True si todos los campos obligatorios son válidos, false en caso contrario.

        Adicionalmente, marca las preguntas obligatorias no respondidas.
    */
    function validateSectionFields(sectionElement) {

        // Campos obligatorios dentro de la sección dada.
        const requiredFields = sectionElement.querySelectorAll('[required]');
        let allFieldsValid = true; // Validez de los campos obligatorios.

        // Primero, limpiamos los errorcillos marcados con anterioridad.a
        sectionElement.querySelectorAll('.question-text').forEach(question => {
            question.classList.remove('error-field');
        });

        // -------------------------------------------------------------- //

        // Ahora lo bueno, realizar la validación en cada uno de los campos.
        requiredFields.forEach(field => {

            // Vamo' a obtener el elemetno que tiene el texto de la pregunta.
            const questionBlock = field.closest('.question-block');
            const questionText = questionBlock.querySelector('.question-text');

            // -------------------------------------------------------------- //

            // Asegura que los 'textarea' obligatoriros no estén vacíos.
            if (field.type === 'textarea' && field.value.trim() === '') {
                allFieldsValid = false;
                questionText.classList.add('error-field');
            }

            // Asegura que los campos 'radio y/o 'checkbox' obligatorios sean completados.
            else if ((field.type === 'radio' || field.type === 'checkbox') &&
                    !sectionElement.querySelector(`input[name="${field.name}"]:checked`)) {

                allFieldsValid = false;
                questionText.classList.add('error-field');
            };
        });

        return allFieldsValid;
    };

    // * -------------------------------------------------------------------- //

    // Se añade un pequeño 'EventListener' a los botones de navegación entre secciones.
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {

            // Obtén la sección actualmente visible antes de cambiar.
            const currentActiveSection = document.querySelector('.section-content:not(.hidden)');

            // Sección a la que se desea ir.
            const targetSection = document.getElementById(this.dataset.sectionId);

            // Sección actual y sección a la que se desea ir.
            const currentIndex = Array.from(sectionContents).indexOf(currentActiveSection);
            const targetIndex = Array.from(sectionContents).indexOf(targetSection);

            if (targetIndex > currentIndex) {
                if (!validateSectionFields(currentActiveSection)) {
                    showModalMessage('Por favor, conteste todas las preguntas obligatorias antes de avanzar.');
                    return;
                }
            }

            // Cuando se hace clic, muestra la sección correspondiente al ' del botón.
            showSection(this.dataset.sectionId); // Como parámetro pasa su dataset (data-section-id)
        });
    });

    // Hehe, tremendos los daataset.

    // * -------------------------------------------------------------------- //

    // Añade un 'event listener' a cada botón usado para avanzar a la siguiente sección.
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {

            // Sección actual (la cual contiene el botoncillo.)
            const currentSection = this.closest('.section-content');

            // De haber campos obligatorios no respondidos, muestra un mensajillo de error.
            if (!validateSectionFields(currentSection)) {
                showModalMessage('Por favor, conteste todas las preguntas obligatorias antes de continuar.');
                return;
            };

            // Si todos los campos son válidos, busca la siguiente sección.
            const nextSection = currentSection.nextElementSibling;
            // Y, de existir una siguiente sección, la muestra.
            if (nextSection && nextSection.classList.contains('section-content')) {
                showSection(nextSection.id);
            };

        });
    });

    // * -------------------------------------------------------------------- //

    // Añade un 'event listener' a cada botón usado para regresar a la sección anterior.
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {

            // Sección actual (la cual contiene el botoncillo.)
            const currentSection = this.closest('.section-content');
            // Sección previa a la mostrada.
            const prevSection = currentSection.previousElementSibling;

            // De haber una sección anterior, la muestra.
            if (prevSection && prevSection.classList.contains('section-content')) {
                showSection(prevSection.id);
            };
        });
    });

    // * -------------------------------------------------------------------- //

    // Al cargar el chutmul, se muestra la primera sección (de haber secciones, por supuesto).
    if (sectionContents.length > 0) {
        showSection(sectionContents[0].id);
    };

    // * -------------------------------------------------------------------- //

    // Oculta todas las preguntas dependientes al acceder a la sección.
    dependentQuestions.forEach(question => {
        question.style.display = 'none';
    });


    /*
        Esta función maneja la visibilidad de las preguntas dependientes.
    */
    function handleQuestionVisibility() {
        dependentQuestions.forEach(question => {

            // Pregunta padre y valor activador.
            const parentQuestionId = question.getAttribute('data-parent-question-id');
            const activatorValue = question.getAttribute('data-parent-activator-value');

            // Input de la pregunta padre.
            const parentInputName = `pregunta_${parentQuestionId}`;
            const parentInputs = document.querySelectorAll(`[name="${parentInputName}"]`);

            let parentValue = null;

            if (parentInputs.length > 0) {
                const parentType = parentInputs[0].type;

                switch(parentType) {
                    case 'radio':
                        const selectedRadio = document.querySelector(`input[name="${parentInputName}"]:checked`);
                        if (selectedRadio) {
                        parentValue = selectedRadio.value;
                        }
                        break;
                    case 'textarea':
                        parentValue = parentInputs[0].value;
                        break;
                }
            }

            if (parentValue === activatorValue) {
                question.style.display = 'block';
            } else {
                question.style.display = 'none';

            // Limpia la preguntas dependientes al ocultarlas.
            const childInput = question.querySelector('textarea, input:checked');
                if (childInput) {
                    if (childInput.type === 'textarea') {
                        childInput.value = '';
                    } else if (childInput.type === 'radio') {
                        childInput.checked = false;
                    }
                }
            }
        });
    }

    handleQuestionVisibility();

    const surveyForm = document.querySelector('.survey-form');
    if (surveyForm) {
        surveyForm.addEventListener('change', handleQuestionVisibility);
        surveyForm.addEventListener('input', handleQuestionVisibility);
    }
});

// -------------------------------------------------------------------------- //
