"""
Agente AI in italiano.

Questo modulo implementa un agente AI che utilizza l'italiano come lingua base.
"""

class AgenteAI:
    """Classe base per un agente AI in italiano."""
    
    def __init__(self, nome: str, ruolo: str = "Assistente"):
        """
        Inizializza l'agente AI.
        
        Args:
            nome (str): Nome dell'agente.
            ruolo (str): Ruolo dell'agente (default: "Assistente").
        """
        self.nome = nome
        self.ruolo = ruolo
        self.stato = "attivo"
        
    def rispondi(self, messaggio: str) -> str:
        """
        Risponde a un messaggio in italiano.
        
        Args:
            messaggio (str): Messaggio da elaborare.
            
        Returns:
            str: Risposta dell'agente.
        """
        # Logica di base per la risposta
        risposta = f"{self.nome} ({self.ruolo}): Ho ricevuto il tuo messaggio: '{messaggio}'. Sto elaborando una risposta in italiano."
        return risposta
    
    def cambia_stato(self, nuovo_stato: str) -> None:
        """
        Cambia lo stato dell'agente.
        
        Args:
            nuovo_stato (str): Nuovo stato dell'agente.
        """
        self.stato = nuovo_stato
        print(f"{self.nome} ha cambiato stato in: {self.stato}")
    
    def __str__(self) -> str:
        """
        Rappresentazione testuale dell'agente.
        
        Returns:
            str: Descrizione dell'agente.
        """
        return f"AgenteAI(nome='{self.nome}', ruolo='{self.ruolo}', stato='{self.stato}')"


if __name__ == "__main__":
    # Esempio di utilizzo
    agente = AgenteAI(nome="Carlo", ruolo="Assistente Personale")
    print(agente)
    
    messaggio = "Ciao, come stai?"
    risposta = agente.rispondi(messaggio)
    print(risposta)
    
    agente.cambia_stato("inattivo")