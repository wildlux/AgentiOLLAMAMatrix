import ollama
import json
import logging
from typing import Dict, List, Optional, Union, Generator, Any
import time

# Assicurati che List sia disponibile
try:
    from typing import List
except ImportError:
    # Per Python < 3.9
    from typing import List

class OllamaInterface:
    """Interfaccia per l'API Ollama usando la libreria ufficiale"""

    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 120):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        # Configura il client ollama tramite variabile d'ambiente
        import os
        os.environ['OLLAMA_HOST'] = self.base_url
        
    def generate(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict] = None,
        stream: bool = False,
        keep_alive: Optional[int] = None
    ) -> Union[Dict, Generator[Any, None, None], None]:
        """
        Genera una risposta dal modello Ollama usando la libreria ufficiale

        Args:
            model: Nome del modello
            prompt: Testo di input
            options: Parametri di generazione
            stream: Se True, restituisce un generatore per lo streaming
            keep_alive: Durata in minuti per mantenere il modello in memoria

        Returns:
            Risposta del modello o None in caso di errore
        """
        try:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                stream=stream,
                options=options or {},
                keep_alive=keep_alive or "5m"
            )

            if stream:
                return response  # È già un generatore
            else:
                return response  # È già un dict

        except Exception as e:
            self.logger.error(f"Errore nella connessione a Ollama: {e}")
            return None
    
    def _handle_stream(self, response) -> Generator[str, None, None]:
        """Gestisce lo streaming della risposta usando la libreria ollama"""
        for chunk in response:
            if 'response' in chunk:
                yield chunk['response']
            if chunk.get('done', False):
                break
    
    def list_models(self) -> list:
        """Elenca tutti i modelli disponibili usando la libreria ollama"""
        try:
            response = ollama.list()
            models = response.get("models", [])
            # Converti in formato compatibile (lista di dict)
            return [{"name": m.model, "size": m.size, "modified_at": m.modified_at.isoformat() if m.modified_at else None, "digest": m.digest} for m in models]
        except Exception as e:
            print(f"Errore nel recupero dei modelli: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Recupera informazioni dettagliate su un modello specifico"""
        try:
            return ollama.show(model_name)
        except Exception as e:
            print(f"Errore nel recupero info modello: {e}")
            return None

    def show_model(self, model_name: str) -> bool:
        """Mostra informazioni su un modello"""
        try:
            ollama.show(model_name)
            return True
        except Exception as e:
            print(f"Errore nel caricamento del modello: {e}")
            return False

    def create_embedding(self, model: str, prompt: str) -> Optional[Dict]:
        """Crea un embedding dal testo"""
        try:
            return ollama.embeddings(model=model, prompt=prompt)
        except Exception as e:
            print(f"Errore nella creazione dell'embedding: {e}")
            return None

    def pull_model(self, model: str) -> bool:
        """Scarica un modello usando la libreria ollama"""
        try:
            ollama.pull(model)
            return True
        except Exception as e:
            print(f"Errore nel download del modello: {e}")
            return False