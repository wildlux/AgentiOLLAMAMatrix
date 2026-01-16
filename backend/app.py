"""
Backend in Flask per gestire l'agente AI e il sistema MCP.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Aggiungi il percorso del modulo al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.agente_ai import AgenteAI
from mcp.mcp import MCP

app = Flask(__name__)

# Inizializza il sistema MCP
mcp = MCP()

@app.route('/')
def index():
    """Pagina principale."""
    return render_template('index.html')

@app.route('/api/agenti', methods=['GET'])
def get_agenti():
    """Restituisce la lista degli agenti."""
    agenti = [{'nome': nome, 'ruolo': agente.ruolo, 'stato': agente.stato} 
              for nome, agente in mcp.agenti.items()]
    return jsonify({'agenti': agenti})

@app.route('/api/agenti', methods=['POST'])
def aggiungi_agente():
    """Aggiunge un nuovo agente."""
    data = request.get_json()
    nome = data.get('nome')
    ruolo = data.get('ruolo', 'Assistente')
    
    if not nome:
        return jsonify({'error': 'Nome dell\'agente mancante'}), 400
    
    agente = AgenteAI(nome=nome, ruolo=ruolo)
    mcp.aggiungi_agente(agente)
    
    return jsonify({'message': f'Agente {nome} aggiunto con successo'}), 201

@app.route('/api/agenti/<nome>', methods=['DELETE'])
def rimuovi_agente(nome):
    """Rimuove un agente."""
    mcp.rimuovi_agente(nome)
    return jsonify({'message': f'Agente {nome} rimosso con successo'}), 200

@app.route('/api/messaggi', methods=['POST'])
def invia_messaggio():
    """Invia un messaggio a tutti gli agenti."""
    data = request.get_json()
    mittente = data.get('mittente')
    messaggio = data.get('messaggio')
    
    if not mittente or not messaggio:
        return jsonify({'error': 'Mittente o messaggio mancanti'}), 400
    
    mcp.invia_messaggio(mittente, messaggio)
    
    return jsonify({'message': 'Messaggio inviato con successo'}), 200

@app.route('/api/stanza', methods=['GET'])
def get_stanza():
    """Restituisce la cronologia della stanza."""
    return jsonify({'stanza': mcp.stanza})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)