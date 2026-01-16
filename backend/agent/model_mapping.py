"""
Mapping tra sezioni e modelli LLM ottimali
"""

from typing import Dict, List

class ModelMapper:
    """Classe per gestire il mapping tra sezioni e modelli LLM"""
    
    def __init__(self):
        # Mapping ottimale sezione -> modello
        self.section_models = {
            'chat': {
                'primary': 'llama3.2:latest',
                'secondary': 'mistral:latest',
                'description': 'Modelli generici per conversazioni'
            },
            'code': {
                'primary': 'codellama:latest',
                'secondary': 'qwen2.5-coder:latest',
                'description': 'Modelli specializzati per il codice'
            },
            'creative': {
                'primary': 'llama3.2:latest',
                'secondary': 'mistral:latest',
                'description': 'Modelli creativi per la scrittura'
            },
            'text': {
                'primary': 'mistral:latest',
                'secondary': 'llama3.2:latest',
                'description': 'Modelli per revisione testi'
            },
            'math': {
                'primary': 'qwen2-math:latest',
                'secondary': 'llama3.2:latest',
                'description': 'Modelli matematici specializzati'
            },
            'psychology': {
                'primary': 'llama3.2:latest',
                'secondary': 'mistral:latest',
                'description': 'Modelli per analisi psicologica'
            }
        }
    
    def get_model_for_section(self, section: str) -> Dict:
        """Restituisce il modello ottimale per una sezione"""
        return self.section_models.get(section, {
            'primary': 'llama3.2:latest',
            'secondary': 'mistral:latest',
            'description': 'Modello predefinito'
        })
    
    def get_all_mappings(self) -> Dict:
        """Restituisce tutti i mapping"""
        return self.section_models
    
    def add_custom_mapping(self, section: str, primary: str, secondary: str, description: str) -> bool:
        """Aggiunge un mapping custom"""
        self.section_models[section] = {
            'primary': primary,
            'secondary': secondary,
            'description': description
        }
        return True

# Funzione per creare un mapper
def create_model_mapper():
    """Crea un mapper di modelli"""
    return ModelMapper()

# Esempio di utilizzo
if __name__ == "__main__":
    mapper = create_model_mapper()
    
    # Ottieni il modello per la sezione matematica
    print("Modello per matematica:", mapper.get_model_for_section('math'))
    
    # Ottieni tutti i mapping
    print("Tutti i mapping:", mapper.get_all_mappings())