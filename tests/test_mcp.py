"""
Test unitari per la classe MCP (Multi-Model Communication Protocol).
"""

import pytest
from src.mcp.mcp import MCP
from src.models.agente_ai import AgenteAI


def test_mcp_initialization():
    """Test inizializzazione MCP"""
    mcp = MCP()
    assert len(mcp.agenti) == 0
    assert len(mcp.stanza) == 0


def test_mcp_add_agent():
    """Test aggiunta di un agente al MCP"""
    mcp = MCP()
    agente = AgenteAI(nome="Carlo", ruolo="Assistente")
    
    mcp.aggiungi_agente(agente)
    
    assert len(mcp.agenti) == 1
    assert "Carlo" in mcp.agenti
    assert len(mcp.stanza) == 1
    assert "Carlo è entrato nella stanza" in mcp.stanza[0]


def test_mcp_add_duplicate_agent():
    """Test aggiunta di un agente duplicato"""
    mcp = MCP()
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente")
    agente2 = AgenteAI(nome="Carlo", ruolo="Esperto")
    
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    
    assert len(mcp.agenti) == 1  # Solo un agente con lo stesso nome


def test_mcp_remove_agent():
    """Test rimozione di un agente dal MCP"""
    mcp = MCP()
    agente = AgenteAI(nome="Carlo", ruolo="Assistente")
    
    mcp.aggiungi_agente(agente)
    assert len(mcp.agenti) == 1
    
    mcp.rimuovi_agente("Carlo")
    assert len(mcp.agenti) == 0
    assert len(mcp.stanza) == 2
    assert "Carlo è uscito dalla stanza" in mcp.stanza[1]


def test_mcp_remove_nonexistent_agent():
    """Test rimozione di un agente inesistente"""
    mcp = MCP()
    
    # Non dovrebbe sollevare eccezioni
    mcp.rimuovi_agente("Inesistente")
    assert len(mcp.agenti) == 0


def test_mcp_send_message():
    """Test invio di un messaggio tra agenti"""
    mcp = MCP()
    
    # Aggiungi agenti
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente")
    agente2 = AgenteAI(nome="Maria", ruolo="Esperta")
    
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    
    # Invia messaggio
    mcp.invia_messaggio("Carlo", "Ciao a tutti!")
    
    # Verifica che il messaggio sia stato aggiunto alla stanza
    assert len(mcp.stanza) == 3  # 2 ingressi + 1 messaggio
    assert "Carlo: Ciao a tutti!" in mcp.stanza[2]
    
    # Verifica che ci siano le risposte degli altri agenti
    assert len(mcp.stanza) > 3  # Dovrebbero esserci anche le risposte


def test_mcp_send_message_from_nonexistent():
    """Test invio di un messaggio da un agente inesistente"""
    mcp = MCP()
    
    # Aggiungi un agente
    agente = AgenteAI(nome="Carlo", ruolo="Assistente")
    mcp.aggiungi_agente(agente)
    
    # Prova a inviare messaggio da agente inesistente
    # Non dovrebbe sollevare eccezioni
    mcp.invia_messaggio("Inesistente", "Ciao")
    
    # Non dovrebbe essere aggiunto nulla alla stanza
    assert len(mcp.stanza) == 1  # Solo l'ingresso di Carlo


def test_mcp_room_history():
    """Test cronologia della stanza"""
    mcp = MCP()
    
    # Aggiungi agenti
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente")
    agente2 = AgenteAI(nome="Maria", ruolo="Esperta")
    
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    
    # Invia messaggi
    mcp.invia_messaggio("Carlo", "Ciao Maria!")
    mcp.invia_messaggio("Maria", "Ciao Carlo!")
    
    # Verifica cronologia
    assert len(mcp.stanza) >= 4  # Almeno 2 ingressi + 2 messaggi
    
    # Verifica che la cronologia contenga gli eventi principali
    assert any("è entrato nella stanza" in evento for evento in mcp.stanza)
    assert any("Carlo: Ciao Maria!" in evento for evento in mcp.stanza)
    assert any("Maria: Ciao Carlo!" in evento for evento in mcp.stanza)


def test_mcp_str_representation():
    """Test rappresentazione stringa del MCP"""
    mcp = MCP()
    
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente")
    agente2 = AgenteAI(nome="Maria", ruolo="Esperta")
    
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    
    str_repr = str(mcp)
    assert "MCP" in str_repr
    assert "agenti" in str_repr
    assert "eventi" in str_repr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])