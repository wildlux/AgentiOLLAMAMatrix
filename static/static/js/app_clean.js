// Assistente AI - Frontend JavaScript
// Versione: 4.0

// Per accesso da cellulare, usa l'IP del computer invece di localhost
const API_URL = 'http://localhost:54324';
const API_KEY = 'demo_key_123';
=======
// ==================== CONFIGURAZIONE ====================
// Per accesso da cellulare, usa l'IP del computer invece di localhost
const API_URL = 'http://localhost:54324';
const API_KEY = 'demo_key_123';====================
// Per accesso da cellulare, usa l'IP del computer invece di localhost
const API_URL = 'http://localhost:54324';

// Leggi API_KEY dall'URL se presente
const urlParams = new URLSearchParams(window.location.search);
let API_KEY = urlParams.get('api_key') || 'demo_key_123';

// Rileva se è un dispositivo mobile
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
const isAndroid = /Android/i.test(navigator.userAgent);

// Ottimizzazioni per Android
if (isAndroid) {
    console.log('📱 Dispositivo Android rilevato - applico ottimizzazioni');
}

// ==================== FUNZIONI PRINCIPALI ====================

// Funzione per accedere
function login() {
    window.location.href = 'login_simple.html';
}

// Funzione per accedere con la demo
function useDemoKey() {
    window.location.href = 'index.html?api_key=demo_key_123';
}

// Funzione per mostrare un messaggio
function showMessage(message, isError = false) {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.style.color = isError ? '#ff4444' : '#4CAF50';
    }
}

// Nascondi login modal se API_KEY è presente nell'URL
if (urlParams.has('api_key')) {
    const loginModal = document.getElementById('loginModal');
    if (loginModal) {
        loginModal.style.display = 'none';
    }
}

// Funzione per connettersi al backend
async function connectToBackend() {
    try {
        const response = await fetch(`${API_URL}/api/health?api_key=${API_KEY}`, {
            method: 'GET',
            mode: 'cors',
            cache: 'no-store',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error('Backend non raggiungibile');
        
        const data = await response.json();
        console.log('Backend connesso:', data);
        return true;
    } catch (error) {
        console.error('Errore di connessione:', error);
        showMessage(`Errore: ${error.message}`, true);
        return false;
    }
}

// ==================== INIZIALIZZAZIONE ====================

// Avvia l'applicazione quando la pagina è caricata
window.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Assistente AI avviato');
    connectToBackend();
});

// Esporta le funzioni per l'uso in altri file
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        login,
        useDemoKey,
        showMessage,
        connectToBackend
    };
}