// Funciones auxiliares copiadas de main.js
function showModalMessage(message) {
    const mainModal = document.getElementById('main-modal');
    const modalMessage = document.getElementById('main-modal-message');
    if (modalMessage) modalMessage.textContent = message;
    if (mainModal) mainModal.showModal();
}

function backToTop() {
    document.body.scrollTop = 0; // Safari.
    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE and Opera.
}

// -------------------------------------------------------------------------- //

// Primero que nada, vamo' a asegurarnos que todo suceda tras cargar bien el contenido.
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔥 JavaScript de evaluación cargado correctamente');

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
    const sectionProgress = document.getElementById('section-progress');

    // Variable para hacer el seguimiento de la sección actual.
    let currentSectionIndex = 0;

    console.log('Elementos encontrados:', {
        tabButtons: tabButtons.length,
        sectionContents: sectionContents.length,
        nextButtons: nextButtons.length,
        prevButtons: prevButtons.length
    });

    // Función para mostrar una sección específica
    function showSection(sectionIndex) {
        console.log('🔄 Cambiando a sección:', sectionIndex);
        
        // Ocultar todas las secciones
        sectionContents.forEach(section => {
            section.classList.add('hidden');
            section.style.display = 'none';
        });

        // Mostrar la sección actual
        if (sectionContents[sectionIndex]) {
            sectionContents[sectionIndex].classList.remove('hidden');
            sectionContents[sectionIndex].style.display = 'block';
        }

        // Actualizar botones activos
        tabButtons.forEach(button => button.classList.remove('active'));
        if (tabButtons[sectionIndex]) {
            tabButtons[sectionIndex].classList.add('active');
        }

        // Actualizar progreso
        const progress = ((sectionIndex + 1) / sectionContents.length) * 100;
        if (sectionLabel) sectionLabel.textContent = `Sección ${sectionIndex + 1} de ${sectionContents.length}`;
        if (sectionPercent) sectionPercent.textContent = `${Math.round(progress)}%`;
        if (sectionProgress) sectionProgress.style.width = `${progress}%`;

        currentSectionIndex = sectionIndex;
    }

    // Event listeners para botones de sección
    tabButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            console.log('🔘 Click en botón de sección:', index);
            showSection(index);
        });
    });

    // Event listeners para botones "Siguiente"
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('➡️ Click en botón siguiente');
            if (currentSectionIndex < sectionContents.length - 1) {
                showSection(currentSectionIndex + 1);
            }
        });
    });

    // Event listeners para botones "Anterior"
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('⬅️ Click en botón anterior');
            if (currentSectionIndex > 0) {
                showSection(currentSectionIndex - 1);
            }
        });
    });

    // Mostrar la primera sección al cargar
    console.log('🚀 Mostrando primera sección...');
    showSection(0);

    // Validación personalizada del formulario
    const form = document.querySelector('.survey-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📋 Validando formulario antes de enviar...');
            
            // Obtener todas las preguntas requeridas
            const allRequiredInputs = form.querySelectorAll('input[required]');
            const preguntasNoRespondidas = [];
            
            // Agrupar por nombre de pregunta
            const preguntaGroups = {};
            allRequiredInputs.forEach(input => {
                const preguntaName = input.name;
                if (!preguntaGroups[preguntaName]) {
                    preguntaGroups[preguntaName] = [];
                }
                preguntaGroups[preguntaName].push(input);
            });
            
            // Verificar que cada grupo de pregunta tenga al menos una respuesta
            Object.keys(preguntaGroups).forEach(preguntaName => {
                const inputs = preguntaGroups[preguntaName];
                const isAnswered = inputs.some(input => input.checked);
                
                if (!isAnswered) {
                    preguntasNoRespondidas.push(preguntaName);
                }
            });
            
            if (preguntasNoRespondidas.length > 0) {
                e.preventDefault();
                console.log('❌ Preguntas sin responder:', preguntasNoRespondidas.length);
                
                // Mostrar mensaje de error
                const mensaje = `Por favor, responde todas las preguntas antes de finalizar la evaluación.\n\nPreguntas sin responder: ${preguntasNoRespondidas.length}`;
                
                if (typeof showModalMessage === 'function') {
                    showModalMessage(mensaje);
                } else {
                    alert(mensaje);
                }
                
                return false;
            }
            
            console.log('✅ Todas las preguntas respondidas, enviando formulario...');
            return true;
        });
    }

    // Hacer la función showSection disponible globalmente para debug
    window.showSection = showSection;
    console.log('✅ Función showSection disponible globalmente');
});
