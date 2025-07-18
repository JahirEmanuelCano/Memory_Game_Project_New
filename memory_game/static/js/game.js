/**
 * Actualiza el DOM para reflejar el estado actual del tablero recibido del backend.
 */

function setDifficulty(level) {
    fetch(`/set-difficulty/${level}/`)
        .then(response => response.json())
        .then(data => {
              window.location.href = '/restart/';
                    updateBoard(data);
        });
}

function updateBoard(data) {
    const board = document.getElementById('board');
    const cards = board.getElementsByClassName('card');
    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const state = data.states[i];
        const cardContent = card.querySelector('.card-content');
        
        if (state === 0) {
            // Carta oculta - mostrar reverso
            cardContent.innerHTML = '<div class="card-back">❓</div>';
            card.classList.remove('matched', 'flipped');
        } else {
            // Carta visible - mostrar imagen
            const image = data.cards[i];
            if (image.startsWith('/static/')) {
                // Si es una ruta de imagen
                cardContent.innerHTML = `<img src="${image}" alt="Carta" class="card-image">`;
            } else {
                // Si es un emoji
                cardContent.innerHTML = `<div class="card-emoji">${image}</div>`;
            }
            
            card.classList.add('flipped');
            if (state === 2) {
                card.classList.add('matched');
            }
        }
    }
    document.getElementById('moves').textContent = 'Movimientos: ' + data.moves;
    
        if (data.phase) {
        updatePhase(data.phase);
     }

         if (data.win) {
        document.getElementById('message').style.display = 'block';
     } 
         if (data.lose){
        document.getElementById('message2').style.display = 'block';
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

function cambiarColumnas(columnas) {
  const board = document.getElementById("board");
  board.style.gridTemplateColumns = `repeat(${columnas}, 160px)`;
  /* (Opcional) generar celdas para ver el efecto
  board.innerHTML = ''; // limpiar
  for (let i = 0; i < filas * 4; i++) {
    const celda = document.createElement("div");
    celda.textContent = i + 1;
    board.appendChild(celda);
  }*/
}


