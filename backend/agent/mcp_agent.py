import yaml
import os
import logging
from typing import Dict, List, Optional, Union, Callable, Generator, Any
from .ollama_interface import OllamaInterface
from .memory_manager import MemoryManager
from .task_manager import TaskManager
from .specialized_modules import SpecializedModules
from .model_mapping import ModelMapper
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class MCPAgent:
    """Agente Multi-Component Processing per l'interfaccia con Ollama.

    Questa classe gestisce l'interazione con modelli Ollama, fornendo funzionalità
    di chat, analisi codice, generazione creativa, correzione testi, risoluzione
    matematica e supporto psicologico.
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        """Inizializza l'agente MCP.

        Args:
            config_path: Percorso al file di configurazione YAML
        """
        # Configura il logging
        self.logger = logging.getLogger(__name__)

        # Carica la configurazione
        self.config = self._load_config(config_path)

        # Inizializza i componenti
        self.ollama = OllamaInterface(
            base_url=self.config['ollama']['base_url'],
            timeout=self.config['ollama']['timeout']
        )

        self.memory = MemoryManager(self.config)
        self.task_manager = TaskManager(self.config)
        self.specialized = SpecializedModules(self.ollama)
        self.model_mapper = ModelMapper()  # Aggiungi il mapper dei modelli

        # Aggiungi modulo finanziario
        from .specialized_modules import FinanceModule
        self.finance = FinanceModule(self.ollama)

        # Imposta il modello corrente basato sulla sezione
        self.current_section = 'chat'
        self._set_model_for_section(self.current_section)

        # Stato dell'agente
        self.current_model = self.config['models']['primary']
        self.available_models = self._get_available_models()

        # Carica prompt finanziari dal config esistente
        self.financial_prompts = {
            'italian_tax': "Sei un esperto fiscale italiano. Fornisci informazioni accurate sui regimi fiscali italiani...",
            'investment': "Sei un consulente finanziario. Analizza investimenti considerando il mercato italiano...",
        }

        # Avvia il task manager
        self.task_manager.start()

        self.logger.info("Agente MCP inizializzato con successo")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carica la configurazione YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except (yaml.YAMLError, IOError) as e:
            print(f"Errore nel caricamento della configurazione: {e}")
            raise
    
    def _get_available_models(self) -> List[str]:
        """Recupera i modelli disponibili"""
        models = self.ollama.list_models()
        return [model['name'] for model in models]
    
    def set_model(self, model_name: str) -> bool:
        """Imposta il modello corrente"""
        if model_name in self.available_models:
            self.current_model = model_name
            return True
        print(f"Modello {model_name} non disponibile.")
        return False
    
    def think(
        self,
        prompt: str,
        mode: str = 'general',
        use_memory: bool = True,
        model: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[str, Generator[Any, None, None], None]:
        """
        Elabora un prompt e restituisce la risposta del modello
        
        Args:
            prompt: Testo di input
            use_memory: Se True, include il contesto dalla memoria
            model: Modello specifico da utilizzare (opzionale)
            stream: Se True, restituisce un generatore per lo streaming
            
        Returns:
            Risposta del modello o None in caso di errore
        """
        # Seleziona il modello (priorità: modello specifico > modello corrente > predefinito)
        target_model = model or self.current_model or self.config['models']['primary']
        
        # Aggiungi contesto dalla memoria se richiesto
        if use_memory:
            memory_context = self.memory.get_memory_context(prompt)
            full_prompt = f"{memory_context}\n\nUtente: {prompt}"
        else:
            full_prompt = prompt
        
        # Recupera i parametri di generazione
        gen_params = self.config['generation']
        
        # Genera la risposta
        response = self.ollama.generate(
            model=target_model,
            prompt=full_prompt,
            options=gen_params,
            stream=stream
        )
        
        if response:
            if stream:
                # Per lo streaming, restituisci il generatore
                return response
            else:
                # Per risposta normale, salva in memoria e restituisci
                result = response.get('response', '')
                
                # Salva l'interazione in memoria
                interaction = {
                    'prompt': prompt,
                    'response': result,
                    'model': target_model
                }
                self.memory.add_to_memory(interaction)
                
                return result
        
        return None
    
    def think_async(self, prompt: str, callback: Callable = None) -> str:
        """
        Esegue il pensiero in modo asincrono
        
        Args:
            prompt: Testo di input
            callback: Funzione da chiamare al completamento
            
        Returns:
            ID del task
        """
        def think_task():
            result = self.think(prompt)
            if callback:
                callback(result)
            return result
        
        return self.task_manager.add_task(think_task)
    
    def get_memory_stats(self) -> Dict:
        """Restituisce statistiche sulla memoria"""
        return self.memory.get_memory_stats()
    
    def get_task_stats(self) -> Dict:
        """Restituisce statistiche sui task"""
        return self.task_manager.get_stats()
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """Cerca nella memoria"""
        return self.memory.search_memory(query, limit)
    
    def clear_memory(self) -> None:
        """Pulisce la memoria a breve termine"""
        self.memory.clear_short_term_memory()
    
    def save_memory(self) -> bool:
        """Salva la memoria a lungo termine"""
        return self.memory.save_all_memory()
    
    def get_available_models(self) -> List[str]:
        """Restituisce i modelli disponibili"""
        return self.available_models
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Restituisce informazioni su un modello"""
        return self.ollama.get_model_info(model_name)
    
    def create_embedding(self, text: str, model: str = "embeddinggemma:latest") -> Optional[Dict]:
        """Crea un embedding dal testo"""
        return self.ollama.create_embedding(model, text)
    
    # Metodi per i moduli specializzati
    
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analizza il codice sorgente con colorazione sintattica"""
        result = self.specialized.code.analyze_code(code, language)
        
        # Aggiungi la versione con colorazione sintattica
        if 'analysis' in result or 'error' not in result:
            result['formatted_code'] = self.format_code(code, language)
        
        return result
    
    def generate_documentation(self, code: str, language: str = "python") -> Dict:
        """Genera documentazione per il codice con colorazione sintattica"""
        documentation = self.specialized.code.generate_documentation(code, language)
        
        return {
            "documentation": documentation,
            "formatted_code": self.format_code(code, language)
        }
    
    def debug_code(self, code: str, error: str = "", language: str = "python") -> Dict:
        """Debug del codice"""
        return self.specialized.code.debug_code(code, error, language)
    
    def generate_story(self, prompt: str, style: str = "realistico", length: str = "medio") -> str:
        """Genera una storia creativa"""
        return self.specialized.creative.generate_story(prompt, style, length)
    
    def create_character(self, description: str) -> Dict:
        """Crea un personaggio dettagliato"""
        return self.specialized.creative.create_character(description)
    
    def improve_writing(self, text: str, style: str = "letterario") -> Dict:
        """Migliora un testo esistente"""
        return self.specialized.creative.improve_writing(text, style)
    
    def grammar_check(self, text: str) -> Dict:
        """Controllo grammaticale avanzato"""
        return self.specialized.text_revision.grammar_check(text)
    
    def style_analysis(self, text: str) -> Dict:
        """Analisi dello stile di scrittura"""
        return self.specialized.text_revision.style_analysis(text)
    
    def plagiarism_check(self, text: str, reference: str = "") -> Dict:
        """Controllo basilare di plagio"""
        return self.specialized.text_revision.plagiarism_check(text, reference)
    
    def solve_equation(self, equation: str, steps: bool = True) -> Dict:
        """Risolvi un'equazione matematica"""
        return self.specialized.math.solve_equation(equation, steps)
    
    def explain_concept(self, concept: str, level: str = "medio") -> str:
        """Spiega un concetto matematico"""
        return self.specialized.math.explain_concept(concept, level)
    
    def calculate(self, expression: str) -> Dict:
        """Esegui un calcolo matematico"""
        return self.specialized.math.calculate(expression)
    
    # Metodi per il modulo psicologico
    
    def emotional_analysis(self, text: str) -> Dict:
        """Analizza il contenuto emotivo di un testo"""
        return self.specialized.psychology.emotional_analysis(text)
    
    def well_being_advice(self, situation: str, mood: str = "neutro") -> str:
        """Fornisce consigli di benessere mentale"""
        return self.specialized.psychology.well_being_advice(situation, mood)
    
    def relaxation_technique(self, technique_type: str = "respirazione") -> Dict:
        """Fornisce una tecnica di rilassamento guidata"""
        return self.specialized.psychology.relaxation_technique(technique_type)
    
    def cognitive_analysis(self, thought_pattern: str) -> Dict:
        """Analisi cognitivo-comportamentale di schemi di pensiero"""
        return self.specialized.psychology.cognitive_analysis(thought_pattern)
    
    def stress_management(self, stress_source: str) -> Dict:
        """Strategie per la gestione dello stress"""
        return self.specialized.psychology.stress_management(stress_source)
    
    def shutdown(self) -> None:
        """Arresta l'agente in modo pulito"""
        self.task_manager.stop()
        self.save_memory()
        self.logger.info("Agente MCP arrestato correttamente.")
    
    def format_code(self, code: str, language: str = "python") -> str:
        """Applica la colorazione sintattica al codice"""
        try:
            if language.lower() == "python":
                lexer = PythonLexer()
            else:
                # Per altri linguaggi, usa un lexer generico
                from pygments.lexers import get_lexer_by_name
                lexer = get_lexer_by_name(language, stripall=True)
            
            formatter = HtmlFormatter(noclasses=True, style="colorful")
            return highlight(code, lexer, formatter)
        except:
            # Se la colorazione fallisce, restituisci il codice originale
            return f"<pre>{code}</pre>"
    
    def _set_model_for_section(self, section: str) -> None:
        """Imposta il modello ottimale per la sezione corrente"""
        model_info = self.model_mapper.get_model_for_section(section)
        self.current_model = model_info['primary']
        self.logger.info(f"Modello impostato su {self.current_model} per la sezione {section}")
    
    def set_section(self, section: str) -> Dict:
        """Cambia la sezione corrente e imposta il modello ottimale"""
        if section not in self.model_mapper.get_all_mappings():
            return {"error": "Sezione non valida", "success": False}
        
        self.current_section = section
        self._set_model_for_section(section)
        
        return {
            "section": section,
            "model": self.current_model,
            "success": True
        }
    
    def get_status(self) -> Dict:
        """Restituisce lo stato corrente dell'agente"""
        return {
            'current_model': self.current_model,
            'current_section': self.current_section,
            'available_models': len(self.available_models),
            'memory_stats': self.get_memory_stats(),
            'task_stats': self.get_task_stats(),
            'status': 'running'
        }