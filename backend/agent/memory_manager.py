import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

class MemoryManager:
    """Gestione avanzata della memoria per l'agente MCP"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.short_term_memory: List[Dict] = []
        self.long_term_memory_file = config['memory']['long_term_file']
        self.short_term_limit = config['memory']['short_term_limit']
        
        # Carica la memoria a lungo termine se esiste
        self.long_term_memory = self._load_long_term_memory()
    
    def _load_long_term_memory(self) -> List[Dict]:
        """Carica la memoria a lungo termine dal file"""
        if os.path.exists(self.long_term_memory_file):
            try:
                with open(self.long_term_memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Errore nel caricamento della memoria a lungo termine: {e}")
        return []
    
    def _save_long_term_memory(self) -> bool:
        """Salva la memoria a lungo termine su file"""
        try:
            with open(self.long_term_memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.long_term_memory, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Errore nel salvataggio della memoria a lungo termine: {e}")
            return False
    
    def add_to_memory(self, interaction: Dict) -> None:
        """Aggiunge un'interazione alla memoria"""
        # Aggiungi timestamp e ID univoco
        interaction['timestamp'] = datetime.now().isoformat()
        interaction['id'] = str(uuid.uuid4())
        
        # Aggiungi alla memoria a breve termine
        self.short_term_memory.append(interaction)
        
        # Mantieni solo gli ultimi N elementi
        if len(self.short_term_memory) > self.short_term_limit:
            self.short_term_memory = self.short_term_memory[-self.short_term_limit:]
        
        # Aggiungi anche alla memoria a lungo termine
        self.long_term_memory.append(interaction)
        
        # Salva periodicamente la memoria a lungo termine
        if len(self.long_term_memory) % 5 == 0:  # Salva ogni 5 interazioni
            self._save_long_term_memory()
    
    def get_short_term_memory(self) -> List[Dict]:
        """Restituisce la memoria a breve termine"""
        return self.short_term_memory.copy()
    
    def get_long_term_memory(self) -> List[Dict]:
        """Restituisce la memoria a lungo termine"""
        return self.long_term_memory.copy()
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Cerca nella memoria interazioni rilevanti"""
        # Implementazione semplice - cerca il testo nella query
        results = []
        
        # Cerca nella memoria a breve termine
        for item in self.short_term_memory:
            if (query.lower() in item.get('prompt', '').lower() or
                query.lower() in item.get('response', '').lower()):
                results.append(item)
                if len(results) >= limit:
                    break
        
        # Se non abbastanza risultati, cerca nella memoria a lungo termine
        if len(results) < limit:
            for item in reversed(self.long_term_memory):  # Dal più recente
                if (query.lower() in item.get('prompt', '').lower() or
                    query.lower() in item.get('response', '').lower()):
                    if item not in results:  # Evita duplicati
                        results.append(item)
                        if len(results) >= limit:
                            break
        
        return results
    
    def get_memory_context(self, query: Optional[str] = None) -> str:
        """Restituisce un contesto formattato dalla memoria"""
        if query:
            relevant_memories = self.search_memory(query)
        else:
            relevant_memories = self.short_term_memory[-3:]  # Ultimi 3 elementi
        
        context = "Contesto dalla memoria:\n"
        for i, memory in enumerate(relevant_memories, 1):
            context += f"{i}. Utente: {memory.get('prompt', '')}\n"
            context += f"   Agente: {memory.get('response', '')}\n"
        
        return context if relevant_memories else "Nessun contesto rilevante trovato."
    
    def clear_short_term_memory(self) -> None:
        """Pulisce la memoria a breve termine"""
        self.short_term_memory = []
    
    def save_all_memory(self) -> bool:
        """Salva tutta la memoria a lungo termine"""
        return self._save_long_term_memory()
    
    def get_memory_stats(self) -> Dict:
        """Restituisce statistiche sulla memoria"""
        return {
            'short_term_count': len(self.short_term_memory),
            'long_term_count': len(self.long_term_memory),
            'short_term_limit': self.short_term_limit
        }