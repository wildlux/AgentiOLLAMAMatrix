import os
from datetime import timedelta

class Config:
    """Configurazione base"""
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))

    # Ollama
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '300'))

    # Modelli
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'qwen2.5:7b-instruct-q4_K_M')
    FINANCE_MODEL = os.getenv('FINANCE_MODEL', 'qwen2.5:14b-instruct-q4_K_M')
    CODE_MODEL = os.getenv('CODE_MODEL', 'qwen2.5-coder:7b')
    MATH_MODEL = os.getenv('MATH_MODEL', 'qwen2-math:latest')
    WRITING_MODEL = os.getenv('WRITING_MODEL', 'qwen2.5:14b-instruct-q4_K_M')
    STORY_MODEL = os.getenv('STORY_MODEL', 'deepseek-r1:latest')
    ORCHESTRATOR_MODEL = os.getenv('ORCHESTRATOR_MODEL', 'adrienbrault/nous-hermes2pro:Q4_K_M')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'embeddinggemma:latest')

    # Context Window
    DEFAULT_NUM_CTX = int(os.getenv('DEFAULT_NUM_CTX', '4096'))
    FINANCE_CTX = int(os.getenv('FINANCE_CTX', '8192'))
    MATH_CTX = int(os.getenv('MATH_CTX', '4096'))
    CODE_CTX = int(os.getenv('CODE_CTX', '4096'))
    WRITING_CTX = int(os.getenv('WRITING_CTX', '8192'))
    STORY_CTX = int(os.getenv('STORY_CTX', '8192'))

    # Generazione
    DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', '0.7'))
    DEFAULT_TOP_P = float(os.getenv('DEFAULT_TOP_P', '0.9'))
    DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '2048'))

    # Sicurezza
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16*1024*1024))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080').split(',')
    VALID_API_KEYS = os.getenv('VALID_API_KEYS', 'demo_key_123,admin_key_456,test_key_789').split(',')

    # Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = os.getenv('RATE_LIMIT', '100/hour')

    # Session
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', '7200')))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/assistente_ai.log')
    LOG_MAX_SIZE_MB = int(os.getenv('LOG_MAX_SIZE_MB', '10'))
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '3'))

    # Cache
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TTL_MINUTES = int(os.getenv('CACHE_TTL_MINUTES', '30'))
    CACHE_MAX_SIZE_MB = int(os.getenv('CACHE_MAX_SIZE_MB', '100'))

    # Features
    ENABLE_VOICE_SYNTHESIS = os.getenv('ENABLE_VOICE_SYNTHESIS', 'true').lower() == 'true'
    ENABLE_CODE_EXECUTION = os.getenv('ENABLE_CODE_EXECUTION', 'true').lower() == 'true'
    ENABLE_CHART_GENERATION = os.getenv('ENABLE_CHART_GENERATION', 'true').lower() == 'true'
    ENABLE_NEWS_FEED = os.getenv('ENABLE_NEWS_FEED', 'true').lower() == 'true'

    # Monitoring
    METRICS_ENABLED = os.getenv('METRICS_ENABLED', 'true').lower() == 'true'
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', '30'))


class DevelopmentConfig(Config):
    """Configurazione per sviluppo"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configurazione per produzione"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

    # Headers di sicurezza
    SECURITY_HEADERS = {
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }


class TestingConfig(Config):
    """Configurazione per testing"""
    DEBUG = True
    TESTING = True
    RATELIMIT_ENABLED = False
    CACHE_ENABLED = False


# Mappa delle configurazioni
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}