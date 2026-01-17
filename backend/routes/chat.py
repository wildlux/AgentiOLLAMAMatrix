from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from pydantic import BaseModel, validator
import time

chat_bp = Blueprint('chat', __name__)

class ChatRequest(BaseModel):
    message: str
    agent: str = "general"
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 2000

    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Il messaggio non può essere vuoto')
        if len(v) > 10000:
            raise ValueError('Il messaggio è troppo lungo')
        return v

    @validator('temperature')
    def temperature_range(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError('La temperatura deve essere tra 0.0 e 2.0')
        return v

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint chat principale con validazione e sicurezza"""
    try:
        # Parse JSON request
        data = ChatRequest(**request.json)

        # Log request (senza dati sensibili)
        print(f"📝 Chat request: agent={data.agent}, model={data.model}, msg_len={len(data.message)}")

        # TODO: Implement actual chat logic
        # For now, return a mock response
        response = {
            "response": f"Ricevuto messaggio per agente '{data.agent}': {data.message[:50]}...",
            "agent": data.agent,
            "model": data.model or "default",
            "timestamp": time.time()
        }

        return jsonify(response)

    except ValueError as e:
        return jsonify({"error": str(e), "type": "validation_error"}), 400
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({"error": "Errore interno del server", "type": "server_error"}), 500

@chat_bp.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Endpoint streaming chat (placeholder)"""
    # TODO: Implement streaming
    return jsonify({"error": "Streaming non ancora implementato"}), 501