# Merged Agent Management System
# Combines Multi-Agent Ollama capabilities with Financial AI Assistant

# Import agent components
from agent.mcp_agent import MCPAgent
from agent.memory_manager import MemoryManager
from agent.task_manager import TaskManager
from agent.specialized_modules import SpecializedModules
from agent.model_mapping import ModelMapper
from agent.ollama_interface import OllamaInterface

# Import existing utilities
from server_utils import *
import json

def send_response(start_response, status, headers, body):
    """Send WSGI response"""
    start_response(status, headers)
    return [body.encode('utf-8')]

# Global agent registry
agents = {}

def get_or_create_agent(agent_id, config_path="backend/config/config.yaml"):
    if agent_id not in agents:
        agents[agent_id] = MCPAgent(config_path)
    return agents[agent_id]

def create_agent_endpoint(environ, start_response, body):
    """Create a new agent instance"""
    try:
        agent_id = f"agent_{len(agents) + 1}"
        agent = get_or_create_agent(agent_id)
        response = {"status": "success", "agent_id": agent_id, "message": "Agent created"}
        return json_response(response)
    except Exception as e:
        return json_response({"error": str(e)}, 500)

def list_agents_endpoint(environ, start_response, body):
    """List all active agents"""
    agent_list = [{"id": aid, "model": agent.current_model} for aid, agent in agents.items()]
    response = {"agents": agent_list}
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
    ]
    return send_response(start_response, status, headers, json.dumps(response))

def chat_with_agent_endpoint(environ, start_response, body):
    """Chat with a specific agent"""
    try:
        data = json.loads(body)
        agent_id = data.get('agent_id', 'default')
        text = data.get('text', '')
        mode = data.get('mode', 'general')
        
        agent = get_or_create_agent(agent_id)
        response = agent.think(prompt=text, mode=mode, use_memory=True)
        
        response_data = {"response": str(response) if response else "Errore: nessuna risposta dall'agente"}
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        ]
        return send_response(start_response, status, headers, json.dumps(response_data, ensure_ascii=False))
    except Exception as e:
        error_response = {"error": str(e)}
        status = '500 Internal Server Error'
        headers = [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
        ]
        return send_response(start_response, status, headers, json.dumps(error_response))

def json_response(data, status_code=200):
    """Helper to create JSON response - returns tuple for wsgi"""
    response_body = json.dumps(data, ensure_ascii=False)
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type, X-API-Key, Authorization')
    ]
    status = f'{status_code} OK' if status_code == 200 else f'{status_code} Error'
    return status, headers, response_body

# Add to existing wsgi_main.py routing