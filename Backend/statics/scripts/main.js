
// -------------------------------------------------------------------------- //

/*
    Esta función envía al usuario a la parte superior de la página.
*/
export function backToTop() {
    document.body.scrollTop = 0; // Safari.
    document.documentElement.scrollTop = 0; // Chrome, Firefox, IE and Opera.
};


/*
    Esta función muestra el modal con un mensaje específico.
    * @param {string} message - Hace referencia al mensaje a mostrar.
*/
export function showModalMessage(message) {
    // Modal para mostrar mensajillos.
    const mainModal = document.getElementById('main-modal');
    // Elemento para mostrar mensajillos en la modal.
    const modalMessage = document.getElementById('main-modal-message');

    modalMessage.textContent = message;
    mainModal.showModal();
};

// -------------------------------------------------------------------------- //
