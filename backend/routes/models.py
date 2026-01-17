from flask import Blueprint, request, jsonify
from pydantic import BaseModel, validator
import time

models_bp = Blueprint('models', __name__)

@models_bp.route('/api/models', methods=['GET'])
def list_available_models():
    """Lista modelli disponibili con ottimizzazioni"""
    try:
        # TODO: Implementare chiamata reale a Ollama API
        # Per ora mock data
        models = [
            {
                "name": "qwen2.5:7b-instruct-q4_K_M",
                "size": "4.7 GB",
                "category": "generale",
                "suggested_ctx": 4096,
                "capabilities": ["chat", "multilingual"]
            },
            {
                "name": "qwen2.5:14b-instruct-q4_K_M",
                "size": "9.0 GB",
                "category": "generale",
                "suggested_ctx": 8192,
                "capabilities": ["chat", "analysis", "finance"]
            },
            {
                "name": "qwen2.5-coder:7b",
                "size": "4.7 GB",
                "category": "codice",
                "suggested_ctx": 4096,
                "capabilities": ["programming", "debugging"]
            },
            {
                "name": "qwen2-math:latest",
                "size": "4.4 GB",
                "category": "matematica",
                "suggested_ctx": 4096,
                "capabilities": ["equations", "calculus"]
            }
        ]

        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)

        return jsonify({
            "models": models,
            "recommended": "qwen2.5:7b-instruct-q4_K_M",
            "system_info": {
                "ram_gb": round(ram_gb, 1),
                "default_context": 4096 if ram_gb >= 16 else 2048,
                "optimization_level": "high" if ram_gb >= 16 else "standard"
            },
            "optimization_note": f"Sistema ottimizzato per {ram_gb:.1f}GB RAM"
        })

    except Exception as e:
        return jsonify({"error": str(e), "models": []}), 500