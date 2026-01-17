from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from pydantic import BaseModel, validator
import time
from backend.services.cache_service import cache

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint per Docker e monitoring"""
    try:
        # Check Ollama connectivity
        import requests
        ollama_url = request.host_url.replace(request.host_url.split(':')[-1], '11434')
        response = requests.get(f"{ollama_url}/api/tags", timeout=3)

        checks = {
            "flask": "ok",
            "ollama": "ok" if response.status_code == 200 else "error",
            "cache": "ok",
            "timestamp": time.time()
        }

        status = "healthy" if all(v == "ok" for v in checks.values() if isinstance(v, str)) else "degraded"

        return jsonify({
            "status": status,
            "checks": checks,
            "version": "1.0.0",
            "uptime": time.time()  # TODO: Implement real uptime tracking
        }), 200 if status == "healthy" else 503

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 503

@health_bp.route('/api/metrics', methods=['GET'])
def metrics():
    """Endpoint metriche per Prometheus (base implementation)"""
    return jsonify({
        "total_requests": 0,  # TODO: Implement real metrics
        "active_connections": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "avg_response_time": 0.0
    })

@health_bp.route('/api/status', methods=['GET'])
def system_status():
    """Status dettagliato del sistema"""
    import psutil

    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        },
        "ollama_models": [],  # TODO: Get from Ollama API
        "active_agents": 0    # TODO: Track active agents
    })