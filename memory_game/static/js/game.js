/**
 * Actualiza el DOM para reflejar el estado actual del tablero recibido del backend.
 */
function updateBoard(data) {
    const board = document.getElementById('board');
    const cards = board.getElementsByClassName('card');
    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const state = data.states[i];
        if (state === 0) {
            card.textContent = '';
            card.classList.remove('matched');
        } else {
            card.textContent = data.cards[i];
            if (state === 2) {
                card.classList.add('matched');
            }
        }
    }
    document.getElementById('moves').textContent = 'Movimientos: ' + data.moves;
    
    // Actualizar información de fase
    if (data.phase) {
        updatePhase(data.phase);
    }

    // Mostrar mensaje si el jugador gana
    if (data.win) {
        document.getElementById('message').style.display = 'block';
    }
}

/**
 * Cambia los elementos de la interfaz según la fase actual del juego.
 */
function updatePhase(phase) {
    const phaseElement = document.getElementById('current-phase');
    const instructionElement = document.getElementById('instruction-text');
    const startMemorizingBtn = document.getElementById('start-memorizing');
    const startPlayingBtn = document.getElementById('start-playing');
    
    switch(phase) {
        case 'setup':
            phaseElement.textContent = 'Preparación';
            instructionElement.textContent = 'Haz clic en "Comenzar Memorización" para ver todas las cartas y memorizar sus posiciones.';
            startMemorizingBtn.style.display = 'block';
            startPlayingBtn.style.display = 'none';
            break;
        case 'memorizing':
            phaseElement.textContent = 'Memorizando';
            instructionElement.textContent = 'Memoriza las posiciones de todas las cartas. Cuando estés listo, haz clic en "Comenzar Juego".';
            startMemorizingBtn.style.display = 'none';
            startPlayingBtn.style.display = 'block';
            break;
        case 'playing':
            phaseElement.textContent = 'Jugando';
            instructionElement.textContent = 'Haz clic en las cartas para encontrar pares iguales. ¡Usa tu memoria!';
            startMemorizingBtn.style.display = 'none';
            startPlayingBtn.style.display = 'none';
            break;
    }
}

/**
 * Solicita al backend voltear una carta y actualiza el tablero.
 */
function fetchFlip(index) {
    fetch('/flip/' + index + '/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
            if (data.mismatch) {
                setTimeout(() => {
                    // Resolver el error después de una pequeña pausa
                    fetch('/flip/-1/')
                        .then(r => r.json())
                        .then(updateBoard);
                }, 1000);
            }
        });
}

/** Inicia la fase de memorización vía AJAX. */
function startMemorizing() {
    fetch('/start-memorizing/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
        });
}

/** Inicia la fase de juego vía AJAX. */
function startPlaying() {
    fetch('/start-playing/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
        });
}

// Asigna los controladores de eventos una vez que el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            const index = card.getAttribute('data-index');
            fetchFlip(index);
        });
    });
    
    document.getElementById('restart').addEventListener('click', () => {
        window.location.href = '/restart/';
    });
    
    document.getElementById('start-memorizing').addEventListener('click', startMemorizing);
    document.getElementById('start-playing').addEventListener('click', startPlaying);
});
