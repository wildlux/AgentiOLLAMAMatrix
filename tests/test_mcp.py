"""
Test per il sistema MCP.
"""

import sys
import os

# Aggiungi il percorso del modulo al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.agente_ai import AgenteAI
from mcp.mcp import MCP


def test_mcp():
    """Test per la classe MCP."""
    print("Test MCP...")
    
    # Crea un sistema MCP
    mcp = MCP()
    
    # Crea alcuni agenti
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente")
    agente2 = AgenteAI(nome="Sofia", ruolo="Esperta")
    
    # Test aggiungi_agente
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    
    assert len(mcp.agenti) == 2, "Numero di agenti non corretto"
    assert "Carlo" in mcp.agenti, "Agente Carlo non aggiunto"
    assert "Sofia" in mcp.agenti, "Agente Sofia non aggiunto"
    
    # Test invia_messaggio
    mcp.invia_messaggio("Carlo", "Ciao Sofia!")
    
    # Verifica che il messaggio sia stato aggiunto alla stanza
    assert len(mcp.stanza) >= 1, "Nessun evento nella stanza"
    assert any("Carlo: Ciao Sofia!" in evento for evento in mcp.stanza), "Messaggio non trovato nella stanza"
    
    # Test rimuovi_agente
    mcp.rimuovi_agente("Sofia")
    
    assert len(mcp.agenti) == 1, "Agente Sofia non rimosso"
    assert "Sofia" not in mcp.agenti, "Agente Sofia ancora presente"
    
    print("Test MCP completato con successo!\n")


if __name__ == "__main__":
    test_mcp()