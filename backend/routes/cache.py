from flask import Blueprint, request, jsonify
import psutil
import time
from backend.utils.logger import logger

cache_bp = Blueprint('cache', __name__)

# Cache semplice in memoria (TODO: Implementare Redis/memcached)
_cache = {}

@cache_bp.route('/api/cache/stats', methods=['GET'])
def cache_stats():
    """Statistiche cache"""
    return jsonify({
        "entries": len(_cache),
        "size_mb": sum(len(str(v)) for v in _cache.values()) / (1024*1024),
        "timestamp": time.time()
    })

@cache_bp.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Svuota cache"""
    _cache.clear()
    logger.info("Cache cleared")
    return jsonify({"status": "cleared", "entries_removed": 0})