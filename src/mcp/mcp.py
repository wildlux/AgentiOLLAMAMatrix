"""
Multi-Model Communication Protocol (MCP).

Questo modulo implementa un sistema per far comunicare più modelli AI
come se fossero nella stessa stanza.
"""

from typing import Dict, List
import sys
import os

# Aggiungi il percorso del modulo al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.agente_ai import AgenteAI


class MCP:
    """Classe per gestire la comunicazione tra più agenti AI."""
    
    def __init__(self):
        """Inizializza il sistema MCP."""
        self.agenti: Dict[str, AgenteAI] = {}
        self.stanza: List[str] = []
        
    def aggiungi_agente(self, agente: AgenteAI) -> None:
        """
        Aggiunge un agente al sistema MCP.
        
        Args:
            agente (AgenteAI): Agente da aggiungere.
        """
        if agente.nome not in self.agenti:
            self.agenti[agente.nome] = agente
            self.stanza.append(f"{agente.nome} è entrato nella stanza.")
            print(f"{agente.nome} è stato aggiunto al sistema MCP.")
        else:
            print(f"{agente.nome} è già presente nel sistema MCP.")
        
    def rimuovi_agente(self, nome_agente: str) -> None:
        """
        Rimuove un agente dal sistema MCP.
        
        Args:
            nome_agente (str): Nome dell'agente da rimuovere.
        """
        if nome_agente in self.agenti:
            del self.agenti[nome_agente]
            self.stanza.append(f"{nome_agente} è uscito dalla stanza.")
            print(f"{nome_agente} è stato rimosso dal sistema MCP.")
        else:
            print(f"{nome_agente} non è presente nel sistema MCP.")
        
    def invia_messaggio(self, mittente: str, messaggio: str) -> None:
        """
        Invia un messaggio da un agente a tutti gli altri agenti.
        
        Args:
            mittente (str): Nome dell'agente mittente.
            messaggio (str): Messaggio da inviare.
        """
        if mittente not in self.agenti:
            print(f"{mittente} non è presente nel sistema MCP.")
            return
        
        self.stanza.append(f"{mittente}: {messaggio}")
        
        for nome, agente in self.agenti.items():
            if nome != mittente:
                risposta = agente.rispondi(messaggio)
                self.stanza.append(risposta)
        
    def visualizza_stanza(self) -> None:
        """Visualizza la cronologia della stanza."""
        print("\n--- Cronologia della stanza ---")
        for evento in self.stanza:
            print(evento)
        print("--- Fine cronologia ---\n")
        
    def __str__(self) -> str:
        """
        Rappresentazione testuale del sistema MCP.
        
        Returns:
            str: Descrizione del sistema MCP.
        """
        return f"MCP(agenti={list(self.agenti.keys())}, eventi={len(self.stanza)})"


if __name__ == "__main__":
    # Esempio di utilizzo
    mcp = MCP()
    
    # Crea alcuni agenti
    agente1 = AgenteAI(nome="Carlo", ruolo="Assistente Personale")
    agente2 = AgenteAI(nome="Sofia", ruolo="Esperta di Lingue")
    agente3 = AgenteAI(nome="Marco", ruolo="Analista Dati")
    
    # Aggiungi gli agenti al sistema MCP
    mcp.aggiungi_agente(agente1)
    mcp.aggiungi_agente(agente2)
    mcp.aggiungi_agente(agente3)
    
    print(mcp)
    
    # Invia un messaggio
    mcp.invia_messaggio("Carlo", "Ciao a tutti! Come state?")
    
    # Visualizza la cronologia della stanza
    mcp.visualizza_stanza()
    
    # Rimuovi un agente
    mcp.rimuovi_agente("Marco")
    
    # Visualizza la cronologia aggiornata
    mcp.visualizza_stanza()