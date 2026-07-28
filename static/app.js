// static/app.js

const PIECE_SVGS = {
    P: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <circle cx="22.5" cy="12" r="6"/>
            <path d="M 22.5,18 C 17,21 16,33 13,38 L 32,38 C 29,33 28,21 22.5,18 z" />
            <path d="M 11,38 L 34,38 L 34,41 L 11,41 z" />
        </svg>
    `,
    R: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <path d="M 9,39 L 36,39 L 36,42 L 9,42 z" />
            <path d="M 12,36 L 33,36 L 31,18 L 14,18 z" />
            <path d="M 9,15 L 36,15 L 36,18 L 9,18 z" />
            <path d="M 9,9 L 14,9 L 14,12 L 19,12 L 19,9 L 26,9 L 26,12 L 31,12 L 31,9 L 36,9 L 36,15 L 9,15 z" />
        </svg>
    `,
    N: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <path d="M 33,28.5 C 33,38 31,39 29.5,39 C 28,39 26,38 24,37 C 20.5,39.5 14,39.5 12,38 C 12,36 11,34.5 13,34 C 13,34 9.5,33.5 11,30 C 12.5,26.5 14,26 14,26 C 14,26 12,23 15,16 C 18,9 25.5,9.5 28,12 C 30.5,14.5 31.5,17 31.5,17 C 31.5,17 33,18.5 32,23.5 C 31,28.5 33,28.5 33,28.5 z" />
            <path d="M 11.5,30 C 15,29 17.5,31 18.5,34" fill="none" stroke="${stroke}" stroke-width="1.5" />
            <circle cx="25" cy="15" r="1.5" fill="${stroke}"/>
        </svg>
    `,
    B: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <circle cx="22.5" cy="8" r="2" fill="${stroke}"/>
            <path d="M 9,36 L 36,36 L 36,39 L 9,39 z" />
            <path d="M 15,32 L 30,32 C 32.5,26 31.5,16 22.5,11 C 13.5,16 12.5,26 15,32 z" />
            <path d="M 22.5,11 L 22.5,32 M 17,21 L 28,21" fill="none" stroke="${stroke}" stroke-width="1.5" />
        </svg>
    `,
    Q: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <path d="M 9,38 L 36,38 L 36,41 L 9,41 z" />
            <path d="M 11.5,30 C 16,34 29,34 33.5,30 C 37,24 37,18 33.5,15 C 30,12 25.5,15 22.5,17 C 19.5,15 15,12 11.5,15 C 8,18 8,24 11.5,30 z" />
            <circle cx="11.5" cy="13" r="1.5" fill="${stroke}"/>
            <circle cx="22.5" cy="11.5" r="1.5" fill="${stroke}"/>
            <circle cx="33.5" cy="13" r="1.5" fill="${stroke}"/>
        </svg>
    `,
    K: (fill, stroke) => `
        <svg viewBox="0 0 45 45" fill="${fill}" stroke="${stroke}" stroke-width="2">
            <path d="M 9,38 L 36,38 L 36,41 L 9,41 z" />
            <path d="M 11.5,30 C 16,34 29,34 33.5,30 C 36,25 35.5,18 30.5,18 C 26.5,18 25,23.5 22.5,23.5 C 20,23.5 18.5,18 14.5,18 C 9.5,18 9,25 11.5,30 z" />
            <path d="M 22.5,9 L 22.5,15 M 19.5,12 L 25.5,12" fill="none" stroke="${stroke}" stroke-width="1.5" />
        </svg>
    `
};

let gameState = {
    squares: [],
    turn: 'w',
    evaluation: 0,
    legal_moves: [],
    history: [],
    game_over: false
};

let selectedSquare = null;
let activeDestinations = [];
let aiThinking = false;
let lastHumanMove = null;
let lastAiMove = null;

// Initialize Elements
const boardEl = document.getElementById('board');
const turnLightEl = document.getElementById('turn-light');
const turnTextEl = document.getElementById('turn-text');
const evalValEl = document.getElementById('eval-value');
const evalBarWhiteEl = document.getElementById('eval-bar-white');
const moveListEl = document.getElementById('move-list');
const btnUndo = document.getElementById('btn-undo');
const btnReset = document.getElementById('btn-reset');
const gameOverOverlay = document.getElementById('game-over');
const gameOverSubtitle = document.getElementById('game-over-subtitle');
const btnRestart = document.getElementById('btn-restart');

// Fetch Board State
async function fetchState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();
        updateState(data);
    } catch (err) {
        console.error('Error fetching state:', err);
    }
}

// Update UI state
function updateState(data) {
    gameState = data;
    selectedSquare = null;
    activeDestinations = [];
    
    // Check moves history to get last move highlights
    if (data.human_move) {
        lastHumanMove = data.human_move;
    } else {
        lastHumanMove = null;
    }
    
    if (data.ai_move) {
        lastAiMove = data.ai_move;
    } else {
        lastAiMove = null;
    }

    renderBoard();
    updatePanel();
}

// Render Chess Board Grid
function renderBoard() {
    boardEl.innerHTML = '';
    
    // Chess indices: rows 7 down to 0, cols 0 up to 7
    for (let r = 7; r >= 0; r--) {
        for (let c = 0; c < 8; c++) {
            const squareEl = document.createElement('div');
            squareEl.classList.add('square');
            
            // Light/dark tile layout
            const isLight = (r + c) % 2 !== 0;
            squareEl.classList.add(isLight ? 'light' : 'dark');
            squareEl.dataset.row = r;
            squareEl.dataset.col = c;
            
            // Highlight selected square
            if (selectedSquare && selectedSquare.row === r && selectedSquare.col === c) {
                squareEl.classList.add('selected');
            }
            
            // Highlight last move squares
            if (lastHumanMove && (
                (lastHumanMove.start_row === r && lastHumanMove.start_col === c) ||
                (lastHumanMove.end_row === r && lastHumanMove.end_col === c)
            )) {
                squareEl.classList.add('last-move');
            }
            if (lastAiMove && (
                (lastAiMove.start_row === r && lastAiMove.start_col === c) ||
                (lastAiMove.end_row === r && lastAiMove.end_col === c)
            )) {
                squareEl.classList.add('last-move');
            }
            
            // Highlight valid destination circles
            const destMove = activeDestinations.find(m => m.end_row === r && m.end_col === c);
            if (destMove) {
                squareEl.classList.add('dest');
                const piece = gameState.squares[r][c];
                if (piece) {
                    squareEl.classList.add('has-piece');
                }
                
                // Clicking destinations makes the move
                squareEl.addEventListener('click', (e) => {
                    e.stopPropagation();
                    executeMove(destMove);
                });
            } else {
                // Clicking regular squares handles piece selections
                squareEl.addEventListener('click', () => handleSquareClick(r, c));
            }
            
            // Render Piece SVGs
            const piece = gameState.squares[r][c];
            if (piece) {
                const pieceEl = document.createElement('div');
                pieceEl.classList.add('piece');
                
                let fillColor = piece.color === 'w' ? '#ffffff' : '#0f172a';
                let strokeColor = piece.color === 'w' ? '#1e293b' : '#06b6d4'; // glowing cyan stroke for dark pieces!
                
                if (PIECE_SVGS[piece.type]) {
                    pieceEl.innerHTML = PIECE_SVGS[piece.type](fillColor, strokeColor);
                } else {
                    // Fallback to text representation
                    pieceEl.innerText = piece.color === 'w' ? piece.type : piece.type.toLowerCase();
                    pieceEl.style.fontSize = '2rem';
                    pieceEl.style.fontWeight = 'bold';
                    pieceEl.style.color = piece.color === 'w' ? '#ffffff' : '#000000';
                }
                
                squareEl.appendChild(pieceEl);
            }
            
            boardEl.appendChild(squareEl);
        }
    }
}

// Update Dashboard Statistics
function updatePanel() {
    // 1. Turn indicator
    if (aiThinking) {
        turnLightEl.className = 'turn-light ai-thinking';
        turnTextEl.innerText = 'AI THINKING...';
        btnUndo.disabled = true;
        btnReset.disabled = true;
    } else {
        btnUndo.disabled = gameState.history.length === 0;
        btnReset.disabled = false;
        if (gameState.turn === 'w') {
            turnLightEl.className = 'turn-light your-turn';
            turnTextEl.innerText = 'YOUR TURN';
        } else {
            turnLightEl.className = 'turn-light ai-thinking';
            turnTextEl.innerText = 'AI THINKING...';
        }
    }

    // 2. Evaluation values
    const scoreVal = gameState.evaluation / 100.0;
    const formattedScore = scoreVal > 0 ? `+${scoreVal.toFixed(2)}` : scoreVal.toFixed(2);
    evalValEl.innerText = formattedScore;
    
    if (scoreVal > 0) {
        evalValEl.className = 'metric-value plus';
    } else if (scoreVal < 0) {
        evalValEl.className = 'metric-value minus';
    } else {
        evalValEl.className = 'metric-value';
    }
    
    // Evaluation Bar height (White advantage fills the bar more, i.e., larger percentage)
    // Map score range [-8.00, +8.00] to percentage [5%, 95%]
    let percent = 50 + (scoreVal * 5.6); // 5.6 percent per pawn advantage
    percent = Math.max(5, Math.min(95, percent));
    evalBarWhiteEl.style.height = `${percent}%`;

    // 3. Move Log List
    moveListEl.innerHTML = '';
    for (let i = 0; i < gameState.history.length; i += 2) {
        const moveRow = document.createElement('div');
        moveRow.classList.add('move-row');
        
        const numSpan = document.createElement('span');
        numSpan.classList.add('move-row-num');
        numSpan.innerText = `${Math.floor(i / 2) + 1}.`;
        
        const whiteSpan = document.createElement('span');
        whiteSpan.classList.add('move-row-white');
        whiteSpan.innerText = gameState.history[i];
        
        const blackSpan = document.createElement('span');
        blackSpan.classList.add('move-row-black');
        blackSpan.innerText = gameState.history[i + 1] || '';
        
        moveRow.appendChild(numSpan);
        moveRow.appendChild(whiteSpan);
        moveRow.appendChild(blackSpan);
        
        moveListEl.appendChild(moveRow);
    }
    
    // Scroll move log to the bottom
    moveListEl.scrollTop = moveListEl.scrollHeight;

    // 4. Game Over Handling
    if (gameState.game_over) {
        gameOverOverlay.classList.add('visible');
        // Let's decide who won
        if (gameState.turn === 'w') {
            gameOverSubtitle.innerText = 'AI Wins! You are in checkmate or have no moves.';
        } else {
            gameOverSubtitle.innerText = 'Congratulations, you Win!';
        }
    } else {
        gameOverOverlay.classList.remove('visible');
    }
}

// Handle clicking of board tile
function handleSquareClick(r, c) {
    if (aiThinking || gameState.game_over) return;
    
    const clickedPiece = gameState.squares[r][c];
    
    // If selecting a friendly piece
    if (clickedPiece && clickedPiece.color === gameState.turn) {
        selectedSquare = { row: r, col: c };
        
        // Filter legal moves originating from this square
        activeDestinations = gameState.legal_moves.filter(
            m => m.start_row === r && m.start_col === c
        );
        
        renderBoard();
    } else {
        // Clear selection
        selectedSquare = null;
        activeDestinations = [];
        renderBoard();
    }
}

// Handle pawn promotion logic
async function executeMove(move) {
    if (aiThinking) return;
    let promotion = null;
    
    // Detect pawn promotion: White pawn moving to row 7
    const piece = gameState.squares[move.start_row][move.start_col];
    if (piece && piece.type === 'P' && move.end_row === 7) {
        // Ask for promotion choice in a nice browser prompt
        const choice = prompt("Promote pawn to (Q/R/B/N):", "Q");
        if (choice && ['q', 'r', 'b', 'n', 'Q', 'R', 'B', 'N'].includes(choice)) {
            promotion = choice.toLowerCase();
        } else {
            promotion = 'q'; // Default to Queen
        }
    }

    aiThinking = true;
    updatePanel();
    renderBoard();

    try {
        const response = await fetch('/api/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start_row: move.start_row,
                start_col: move.start_col,
                end_row: move.end_row,
                end_col: move.end_col,
                promotion: promotion
            })
        });

        if (!response.ok) {
            const errData = await response.json();
            alert(errData.error || "Illegal move!");
            aiThinking = false;
            fetchState();
            return;
        }

        const data = await response.json();
        aiThinking = false;
        updateState(data);
    } catch (err) {
        console.error('Error executing move:', err);
        aiThinking = false;
        fetchState();
    }
}

// Undo Button Clicked
btnUndo.addEventListener('click', async () => {
    if (aiThinking) return;
    try {
        const response = await fetch('/api/undo', { method: 'POST' });
        const data = await response.json();
        updateState(data);
    } catch (err) {
        console.error('Error undoing move:', err);
    }
});

// Reset Button Clicked
btnReset.addEventListener('click', async () => {
    if (aiThinking) return;
    if (!confirm("Are you sure you want to reset the game?")) return;
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const data = await response.json();
        updateState(data);
    } catch (err) {
        console.error('Error resetting board:', err);
    }
});

// Restart after Game Over Clicked
btnRestart.addEventListener('click', async () => {
    gameOverOverlay.classList.remove('visible');
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const data = await response.json();
        updateState(data);
    } catch (err) {
        console.error('Error resetting board:', err);
    }
});

// Start application
fetchState();
