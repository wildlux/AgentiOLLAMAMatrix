"""
Modulo per la gestione del blocco delle richieste per sezione
"""

import json
import os
from typing import Dict, List, Optional

class RequestBlocker:
    """Classe per gestire il blocco delle richieste per sezione"""
    
    def __init__(self, config_file: str = "request_blocks.json"):
        self.config_file = config_file
        self.blocked_sections = self._load_blocks()
    
    def _load_blocks(self) -> Dict:
        """Carica i blocchi dal file di configurazione"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_blocks(self) -> bool:
        """Salva i blocchi nel file di configurazione"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.blocked_sections, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def block_section(self, section: str) -> bool:
        """Blocca una sezione"""
        if section not in self.blocked_sections:
            self.blocked_sections[section] = True
            return self._save_blocks()
        return True
    
    def unblock_section(self, section: str) -> bool:
        """Sblocca una sezione"""
        if section in self.blocked_sections:
            del self.blocked_sections[section]
            return self._save_blocks()
        return True
    
    def is_blocked(self, section: str) -> bool:
        """Verifica se una sezione è bloccata"""
        return self.blocked_sections.get(section, False)
    
    def get_all_blocks(self) -> Dict:
        """Restituisce tutti i blocchi attivi"""
        return self.blocked_sections
    
    def reset_all_blocks(self) -> bool:
        """Resetta tutti i blocchi"""
        self.blocked_sections = {}
        return self._save_blocks()

class SectionManager:
    """Gestione avanzata delle sezioni con blocco richieste"""
    
    def __init__(self):
        self.blocker = RequestBlocker()
        self.available_sections = [
            'chat', 'code', 'creative', 'text', 'math', 'psychology'
        ]
    
    def block_section(self, section: str) -> Dict:
        """Blocca una sezione"""
        if section not in self.available_sections:
            return {"error": "Sezione non valida", "success": False}
        
        if self.blocker.block_section(section):
            return {"section": section, "blocked": True, "success": True}
        else:
            return {"error": "Impossibile salvare il blocco", "success": False}
    
    def unblock_section(self, section: str) -> Dict:
        """Sblocca una sezione"""
        if section not in self.available_sections:
            return {"error": "Sezione non valida", "success": False}
        
        if self.blocker.unblock_section(section):
            return {"section": section, "blocked": False, "success": True}
        else:
            return {"error": "Impossibile salvare lo sblocco", "success": False}
    
    def check_section(self, section: str) -> Dict:
        """Verifica lo stato di una sezione"""
        return {
            "section": section,
            "blocked": self.blocker.is_blocked(section),
            "success": True
        }
    
    def get_status(self) -> Dict:
        """Restituisce lo stato di tutte le sezioni"""
        return {
            "sections": {section: self.blocker.is_blocked(section) 
                        for section in self.available_sections},
            "success": True
        }

# Funzione per creare un gestore delle sezioni
def create_section_manager():
    """Crea un gestore delle sezioni"""
    return SectionManager()

# Esempio di utilizzo
if __name__ == "__main__":
    manager = create_section_manager()
    
    # Blocca la sezione matematica
    print(manager.block_section('math'))
    
    # Verifica lo stato
    print(manager.check_section('math'))
    
    # Sblocca la sezione
    print(manager.unblock_section('math'))
    
    # Ottieni lo stato di tutte le sezioni
    print(manager.get_status())