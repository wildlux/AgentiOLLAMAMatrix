"""
Test unitari per la classe AgenteAI.
"""

import pytest
from src.models.agente_ai import AgenteAI


def test_agente_ai_creation():
    """Test creazione agente AI con parametri di default"""
    agente = AgenteAI(nome="Test")
    assert agente.nome == "Test"
    assert agente.ruolo == "Assistente"
    assert agente.stato == "attivo"


def test_agente_ai_custom_role():
    """Test creazione agente AI con ruolo personalizzato"""
    agente = AgenteAI(nome="Finanza", ruolo="Esperto Finanziario")
    assert agente.nome == "Finanza"
    assert agente.ruolo == "Esperto Finanziario"
    assert agente.stato == "attivo"


def test_agente_ai_risposta():
    """Test metodo rispondi dell'agente AI"""
    agente = AgenteAI(nome="Carlo")
    risposta = agente.rispondi("Ciao, come stai?")
    assert "Carlo" in risposta
    assert "Ciao, come stai?" in risposta
    assert "Assistente" in risposta


def test_agente_ai_cambia_stato():
    """Test metodo cambia_stato dell'agente AI"""
    agente = AgenteAI(nome="Test")
    agente.cambia_stato("inattivo")
    assert agente.stato == "inattivo"


def test_agente_ai_str_representation():
    """Test rappresentazione stringa dell'agente AI"""
    agente = AgenteAI(nome="Mario", ruolo="Analista")
    str_repr = str(agente)
    assert "Mario" in str_repr
    assert "Analista" in str_repr
    assert "AgenteAI" in str_repr


def test_agente_ai_multiple_state_changes():
    """Test multipli cambi di stato"""
    agente = AgenteAI(nome="Test")
    assert agente.stato == "attivo"
    
    agente.cambia_stato("occupato")
    assert agente.stato == "occupato"
    
    agente.cambia_stato("inattivo")
    assert agente.stato == "inattivo"
    
    agente.cambia_stato("attivo")
    assert agente.stato == "attivo"


def test_agente_ai_empty_message():
    """Test risposta a messaggio vuoto"""
    agente = AgenteAI(nome="Test")
    risposta = agente.rispondi("")
    assert "Test" in risposta
    assert "" in risposta


def test_agente_ai_special_characters():
    """Test risposta con caratteri speciali"""
    agente = AgenteAI(nome="Test")
    messaggio = "Ciao! Come va? 😊 #test"
    risposta = agente.rispondi(messaggio)
    assert "Test" in risposta
    assert "😊" in risposta
    assert "#test" in risposta


if __name__ == "__main__":
    pytest.main([__file__, "-v"])