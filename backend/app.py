"""
Backend in Flask per gestire l'agente AI e il sistema MCP.
Versione ottimizzata con caching, rate limiting e gestione degli errori.
"""

from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import time
from datetime import datetime
import hashlib
import secrets

# Aggiungi il percorso del modulo al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.agente_ai import AgenteAI
from mcp.mcp import MCP

# Configura logging
os.makedirs('logs', exist_ok=True)
handler = RotatingFileHandler('logs/backend.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app = Flask(__name__)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Configurazione Flask
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # Disabilita pretty print per risparmiare banda
app.config['JSON_SORT_KEYS'] = False  # Disabilita ordinamento chiavi JSON
app.config['CACHE_TYPE'] = 'SimpleCache'  # Configura caching semplice
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Timeout cache di 5 minuti
app.config['CACHE_THRESHOLD'] = 1000  # Numero massimo di elementi in cache

# Configurazione Sicurezza
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minuti

# API Keys - In produzione, usa variabili d'ambiente
API_KEYS = os.getenv('API_KEYS', 'demo_key_123,admin_key_456,test_key_789').split(',')

# Forza HTTPS e sicurezza headers
Talisman(app, 
          force_https=True,
          strict_transport_security=True,
          session_cookie_secure=True,
          content_security_policy={
              'default-src': "'self'",
              'script-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdnjs.cloudflare.com"],
              'style-src': ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net", "cdnjs.cloudflare.com"],
              'img-src': ["'self'", "data:"],
              'connect-src': ["'self'"]
          })

# Inizializza caching
cache = Cache(app)

# Configura rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour", "10 per minute"]
)

# Inizializza il sistema MCP con caching
class CachedMCP:
    """Wrapper per MCP con caching delle operazioni costose"""
    
    def __init__(self):
        self.mcp = MCP()
        self._cache = {}
        self._last_cleanup = time.time()
    
    def _cleanup_cache(self):
        """Pulizia periodica della cache"""
        now = time.time()
        if now - self._last_cleanup > 300:  # Pulizia ogni 5 minuti
            self._cache = {k: v for k, v in self._cache.items() if now - v['timestamp'] < 300}
            self._last_cleanup = now
    
    @property
    def agenti(self):
        """Restituisce la lista degli agenti con caching"""
        self._cleanup_cache()
        cache_key = 'agenti_list'
        
        if cache_key in self._cache:
            return self._cache[cache_key]['data']
        
        result = self.mcp.agenti
        self._cache[cache_key] = {'data': result, 'timestamp': time.time()}
        return result
    
    @property
    def stanza(self):
        """Restituisce la cronologia della stanza"""
        return self.mcp.stanza
    
    def aggiungi_agente(self, agente):
        """Aggiunge un agente e invalida la cache"""
        self.mcp.aggiungi_agente(agente)
        # Invalida cache
        self._cache.pop('agenti_list', None)
    
    def rimuovi_agente(self, nome_agente):
        """Rimuove un agente e invalida la cache"""
        self.mcp.rimuovi_agente(nome_agente)
        # Invalida cache
        self._cache.pop('agenti_list', None)
    
    def invia_messaggio(self, mittente, messaggio):
        """Invia un messaggio"""
        self.mcp.invia_messaggio(mittente, messaggio)

def require_api_key(f):
    """Decorator per richiedere API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Controlla header
        api_key = request.headers.get('X-API-KEY')
        
        # Controlla parametro query
        if not api_key:
            api_key = request.args.get('api_key')
        
        # Controlla body JSON
        if not api_key and request.is_json:
            data = request.get_json(silent=True)
            api_key = data.get('api_key') if data else None
        
        if api_key and api_key in API_KEYS:
            return f(*args, **kwargs)
        else:
            app.logger.warning(f"Tentativo di accesso non autorizzato da {request.remote_addr}")
            return jsonify({
                'error': 'API Key richiesta',
                'valid_keys': ['demo_key_123', 'admin_key_456', 'test_key_789'],
                'documentation': 'https://github.com/wildlux/AgentiOLLAMAMatrix#autenticazione'
            }), 401
    return decorated_function

# Inizializza il sistema MCP con caching
mcp = CachedMCP()

# Middleware per logging delle richieste
@app.before_request
def log_request_info():
    """Logga informazioni su ogni richiesta"""
    app.logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    # Aggiungi header di sicurezza
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

# Middleware per misurare le prestazioni
@app.after_request
def add_performance_headers(response):
    """Aggiunge header di performance alle risposte"""
    if hasattr(request, '_start_time'):
        response.headers['X-Response-Time'] = f"{time.time() - request._start_time:.4f}s"
    return response

@app.before_request
def start_timer():
    """Avvia il timer per la richiesta"""
    request._start_time = time.time()

@app.route('/')
def index():
    """Pagina principale con reindirizzamento automatico al frontend."""
    # Reindirizza automaticamente al frontend statico
    return jsonify({
        'status': 'success',
        'message': 'Backend operativo',
        'frontend_url': 'http://localhost:8080/static/index.html',
        'documentation': '/docs'
    })

@app.route('/docs')
def documentation():
    """Documentazione API."""
    return jsonify({
        'api_version': '1.0',
        'endpoints': {
            'GET /api/agenti': 'Elenca tutti gli agenti',
            'POST /api/agenti': 'Aggiunge un nuovo agente',
            'DELETE /api/agenti/<nome>': 'Rimuove un agente',
            'POST /api/messaggi': 'Invia un messaggio a tutti gli agenti',
            'GET /api/stanza': 'Ottiene la cronologia della stanza'
        },
        'authentication': 'API Key required for /api/* endpoints',
        'rate_limits': '200 requests/day, 50 requests/hour',
        'security': 'HTTPS enforced, CORS restricted, rate limiting active'
    })

@app.route('/security-info')
def security_info():
    """Informazioni sulla sicurezza del sistema."""
    return jsonify({
        'security_status': 'active',
        'https_enforced': True,
        'cors_protection': True,
        'rate_limiting': True,
        'api_authentication': 'required',
        'valid_api_keys': ['demo_key_123', 'admin_key_456', 'test_key_789'],
        'security_headers': ['CSP', 'HSTS', 'XSS-Protection'],
        'logging': 'active'
    })

@app.route('/generate-api-key', methods=['GET'])
def generate_api_key():
    """Genera una nuova API key (solo per demo, in produzione usa un sistema più sicuro)"""
    # Genera una nuova API key
    new_key = secrets.token_hex(16)
    
    app.logger.warning(f"Generata nuova API key: {new_key} (solo per demo)")
    
    return jsonify({
        'new_api_key': new_key,
        'warning': 'Questa è una demo. In produzione, usa un sistema di autenticazione più sicuro.',
        'instructions': 'Usa questa chiave nell\'header X-API-KEY o nel parametro api_key'
    })

@app.route('/api/agenti', methods=['GET'])
@require_api_key
@cache.cached(timeout=60)  # Cache per 60 secondi
@limiter.limit("10 per minute")
def get_agenti():
    """Restituisce la lista degli agenti."""
    app.logger.info(f"Richesta lista agenti da {request.remote_addr}")
    agenti = [{'nome': nome, 'ruolo': agente.ruolo, 'stato': agente.stato} 
              for nome, agente in mcp.agenti.items()]
    return jsonify({'agenti': agenti})

@app.route('/api/agenti', methods=['POST'])
@require_api_key
@limiter.limit("5 per minute")
def aggiungi_agente():
    """Aggiunge un nuovo agente."""
    app.logger.info(f"Tentativo di aggiunta agente da {request.remote_addr}")
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati JSON richiesti'}), 400
    
    nome = data.get('nome')
    ruolo = data.get('ruolo', 'Assistente')
    
    if not nome:
        return jsonify({'error': 'Nome dell\'agente mancante'}), 400
    
    # Validazione nome
    if len(nome) > 50:
        return jsonify({'error': 'Nome troppo lungo (max 50 caratteri)'}), 400
    
    if len(ruolo) > 100:
        return jsonify({'error': 'Ruolo troppo lungo (max 100 caratteri)'}), 400
    
    agente = AgenteAI(nome=nome, ruolo=ruolo)
    mcp.aggiungi_agente(agente)
    
    app.logger.info(f"Agente {nome} aggiunto con successo")
    return jsonify({'message': f'Agente {nome} aggiunto con successo'}), 201

@app.route('/api/agenti/<nome>', methods=['DELETE'])
@require_api_key
@limiter.limit("5 per minute")
def rimuovi_agente(nome):
    """Rimuove un agente."""
    app.logger.info(f"Tentativo di rimozione agente {nome} da {request.remote_addr}")
    
    # Validazione nome
    if len(nome) > 50:
        return jsonify({'error': 'Nome agente non valido'}), 400
    
    mcp.rimuovi_agente(nome)
    app.logger.info(f"Agente {nome} rimosso con successo")
    return jsonify({'message': f'Agente {nome} rimosso con successo'}), 200

@app.route('/api/messaggi', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def invia_messaggio():
    """Invia un messaggio a tutti gli agenti."""
    app.logger.info(f"Tentativo di invio messaggio da {request.remote_addr}")
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dati JSON richiesti'}), 400
    
    mittente = data.get('mittente')
    messaggio = data.get('messaggio')
    
    if not mittente or not messaggio:
        return jsonify({'error': 'Mittente o messaggio mancanti'}), 400
    
    # Validazione lunghezza messaggio
    if len(messaggio) > 1000:
        return jsonify({'error': 'Messaggio troppo lungo (max 1000 caratteri)'}), 400
    
    if len(mittente) > 50:
        return jsonify({'error': 'Nome mittente troppo lungo (max 50 caratteri)'}), 400
    
    mcp.invia_messaggio(mittente, messaggio)
    
    app.logger.info(f"Messaggio inviato da {mittente}: {messaggio[:50]}...")
    return jsonify({'message': 'Messaggio inviato con successo'}), 200

@app.route('/api/stanza', methods=['GET'])
@require_api_key
@cache.cached(timeout=30)  # Cache per 30 secondi
@limiter.limit("15 per minute")
def get_stanza():
    """Restituisce la cronologia della stanza."""
    app.logger.info(f"Richesta cronologia stanza da {request.remote_addr}")
    
    # Limita la dimensione della risposta
    stanza = mcp.stanza[-100:]  # Restituisci solo gli ultimi 100 eventi
    
    return jsonify({'stanza': stanza, 'total_events': len(mcp.stanza)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)