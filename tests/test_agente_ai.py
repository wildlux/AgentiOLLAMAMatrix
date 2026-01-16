"""
Test per l'agente AI.
"""

import sys
import os

# Aggiungi il percorso del modulo al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.agente_ai import AgenteAI


def test_agente_ai():
    """Test per la classe AgenteAI."""
    print("Test AgenteAI...")
    
    # Crea un agente
    agente = AgenteAI(nome="Test", ruolo="Tester")
    
    # Verifica l'inizializzazione
    assert agente.nome == "Test", "Nome dell'agente non corretto"
    assert agente.ruolo == "Tester", "Ruolo dell'agente non corretto"
    assert agente.stato == "attivo", "Stato dell'agente non corretto"
    
    # Test del metodo rispondi
    messaggio = "Ciao, come stai?"
    risposta = agente.rispondi(messaggio)
    assert messaggio in risposta, "Messaggio non presente nella risposta"
    assert agente.nome in risposta, "Nome dell'agente non presente nella risposta"
    
    # Test del metodo cambia_stato
    agente.cambia_stato("inattivo")
    assert agente.stato == "inattivo", "Stato dell'agente non aggiornato"
    
    print("Test AgenteAI completato con successo!\n")


if __name__ == "__main__":
    test_agente_ai()