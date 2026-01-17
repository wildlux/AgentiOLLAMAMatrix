from flask import Blueprint, request, jsonify

agents_bp = Blueprint('agents', __name__)

# Mock agent registry (TODO: Implement real agent management)
AGENTS = {
    "general": {
        "id": "general",
        "name": "Chat Generale",
        "model": "qwen2.5:7b-instruct-q4_K_M",
        "capabilities": ["chat", "Q&A"],
        "status": "active"
    },
    "finance": {
        "id": "finance",
        "name": "Consulente Finanziario",
        "model": "qwen2.5:14b-instruct-q4_K_M",
        "capabilities": ["finance", "tax", "investment"],
        "status": "active"
    },
    "math": {
        "id": "math",
        "name": "Esperto Matematico",
        "model": "qwen2-math:latest",
        "capabilities": ["equations", "calculus", "algebra"],
        "status": "active"
    },
    "code": {
        "id": "code",
        "name": "Sviluppatore",
        "model": "qwen2.5-coder:7b",
        "capabilities": ["programming", "debugging", "refactoring"],
        "status": "active"
    }
}

@agents_bp.route('/api/agents', methods=['GET'])
def list_agents():
    """Lista agenti disponibili"""
    return jsonify({
        "agents": list(AGENTS.values()),
        "total": len(AGENTS)
    })

@agents_bp.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Dettagli agente specifico"""
    if agent_id not in AGENTS:
        return jsonify({"error": "Agente non trovato"}), 404

    return jsonify({"agent": AGENTS[agent_id]})

@agents_bp.route('/api/agents', methods=['POST'])
def create_agent():
    """Crea nuovo agente (placeholder)"""
    return jsonify({
        "error": "Creazione agenti non ancora implementata",
        "status": "planned"
    }), 501

@agents_bp.route('/api/agents/<agent_id>/chat', methods=['POST'])
def chat_with_agent(agent_id):
    """Chat con agente specifico (placeholder)"""
    if agent_id not in AGENTS:
        return jsonify({"error": "Agente non trovato"}), 404

    try:
        data = request.json
        message = data.get('text', '')

        # TODO: Implement actual agent chat
        response = {
            "response": f"Agente {AGENTS[agent_id]['name']} ricevuto: {message[:50]}...",
            "agent_id": agent_id,
            "timestamp": time.time()
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500