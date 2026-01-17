"""
Configurazione di sicurezza per il backend.
"""

import os
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Configurazione API Keys
API_KEYS = os.getenv('API_KEYS', 'demo_key_123,admin_key_456,test_key_789').split(',')

# Configurazione CORS
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:8080,http://localhost:54324').split(',')

# Configurazione Rate Limiting
RATE_LIMITS = {
    'default': '200 per day; 50 per hour; 10 per minute',
    'get_agenti': '10 per minute',
    'post_agenti': '5 per minute',
    'delete_agente': '5 per minute',
    'post_messaggi': '10 per minute',
    'get_stanza': '15 per minute'
}

# Configurazione Content Security Policy
CSP_CONFIG = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'unsafe-inline'",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com"
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        "cdn.jsdelivr.net",
        "cdnjs.cloudflare.com"
    ],
    'img-src': ["'self'", "data:"],
    'connect-src': ["'self'"]
}

# Configurazione HTTPS
HTTPS_CONFIG = {
    'force_https': os.getenv('FORCE_HTTPS', 'true').lower() == 'true',
    'strict_transport_security': True,
    'session_cookie_secure': True,
    'hsts_max_age': 31536000,  # 1 anno
    'hsts_include_subdomains': True
}

# Configurazione Logging
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'file': 'logs/backend.log',
    'max_bytes': 10000,
    'backup_count': 3
}

# Configurazione Validazione Input
INPUT_VALIDATION = {
    'max_name_length': 50,
    'max_role_length': 100,
    'max_message_length': 1000,
    'max_stanza_length': 100  # Numero massimo di eventi restituiti
}

# Configurazione Cache
CACHE_CONFIG = {
    'type': 'SimpleCache',
    'default_timeout': 300,  # 5 minuti
    'threshold': 1000,
    'agenti_timeout': 60,  # 1 minuto
    'stanza_timeout': 30   # 30 secondi
}


def get_security_config():
    """Restituisce la configurazione di sicurezza completa"""
    return {
        'api_keys': {'count': len(API_KEYS), 'source': 'environment variable'},
        'allowed_origins': ALLOWED_ORIGINS,
        'rate_limits': RATE_LIMITS,
        'csp': CSP_CONFIG,
        'https': HTTPS_CONFIG,
        'logging': LOGGING_CONFIG,
        'input_validation': INPUT_VALIDATION,
        'cache': CACHE_CONFIG
    }