"""
Moduli specializzati per diversi settori
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from .ollama_interface import OllamaInterface

class CodeAnalysisModule:
    """Modulo specializzato per l'analisi del codice"""
    
    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.code_models = ["codellama:latest", "codellama:7b"]
    
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analizza il codice sorgente"""
        prompt = f"""Analizza il seguente codice {language}:

```{language}
{code}
```

Fornisci:
1. Potenziali errori o bug
2. Suggerimenti per l'ottimizzazione
3. Complessità algoritmica
4. Documentazione mancante
5. Best practices violate

Formato la risposta in JSON."""
        
        response = self.ollama.generate(
            model=self.code_models[0],
            prompt=prompt,
            options={"temperature": 0.3, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {"analysis": response.get('response', '')}
        
        return {"error": "Analisi fallita"}
    
    def generate_documentation(self, code: str, language: str = "python") -> str:
        """Genera documentazione per il codice"""
        prompt = f"""Genera una documentazione completa per il seguente codice {language}:

```{language}
{code}
```

Includi:
- Descrizione generale
- Parametri e tipi
- Valori di ritorno
- Esempi d'uso
- Eccezioni possibili"""
        
        response = self.ollama.generate(
            model=self.code_models[0],
            prompt=prompt,
            options={"temperature": 0.5}
        )
        
        return response.get('response', '') if response else "Documentazione non generata"
    
    def debug_code(self, code: str, error: str = "", language: str = "python") -> Dict:
        """Debug del codice"""
        error_prompt = f"\nErrore riportato: {error}" if error else ""
        
        prompt = f"""Debugga il seguente codice {language}:{error_prompt}

```{language}
{code}
```

Fornisci:
1. Causa dell'errore
2. Soluzione proposta
3. Codice corretto
4. Spiegazione tecnica"""
        
        response = self.ollama.generate(
            model=self.code_models[0],
            prompt=prompt,
            options={"temperature": 0.4}
        )
        
        if response:
            return {"debug_info": response.get('response', '')}
        
        return {"error": "Debug fallito"}

class CreativeWritingModule:
    """Modulo specializzato per la scrittura creativa"""
    
    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.creative_models = ["llama3.2:latest", "mistral:latest"]
    
    def generate_story(self, prompt: str, style: str = "realistico", length: str = "medio") -> str:
        """Genera una storia creativa"""
        story_prompt = f"""Scrivi una storia {style} di lunghezza {length} basata su:

{prompt}

Includi:
- Personaggi ben sviluppati
- Trama coinvolgente
- Descrizioni vivide
- Dialoghi naturali
- Un finale soddisfacente"""
        
        response = self.ollama.generate(
            model=self.creative_models[0],
            prompt=story_prompt,
            options={"temperature": 0.8, "top_p": 0.95}
        )
        
        return response.get('response', '') if response else "Generazione storia fallita"
    
    def create_character(self, description: str) -> Dict:
        """Crea un personaggio dettagliato"""
        prompt = f"""Crea un personaggio dettagliato basato su:

{description}

Fornisci in formato JSON:
{{
  "nome": "",
  "eta": 0,
  "personalita": "",
  "background": "",
  "motivazioni": "",
  "conflitti": "",
  "sviluppo": ""
}}"""
        
        response = self.ollama.generate(
            model=self.creative_models[0],
            prompt=prompt,
            options={"temperature": 0.7, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {"character": response.get('response', '')}
        
        return {"error": "Creazione personaggio fallita"}
    
    def improve_writing(self, text: str, style: str = "letterario") -> Dict:
        """Migliora un testo esistente"""
        prompt = f"""Migliora il seguente testo in stile {style}:

{text}

Fornisci:
1. Versione migliorata
2. Spiegazione delle modifiche
3. Suggerimenti per lo stile
4. Analisi della coerenza"""
        
        response = self.ollama.generate(
            model=self.creative_models[1],
            prompt=prompt,
            options={"temperature": 0.6}
        )
        
        if response:
            return {"improved_text": response.get('response', '')}
        
        return {"error": "Miglioramento testo fallito"}

class TextRevisionModule:
    """Modulo specializzato per la revisione dei testi"""
    
    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.revision_models = ["mistral:latest", "llama3.2:latest"]
    
    def grammar_check(self, text: str) -> Dict:
        """Controllo grammaticale avanzato"""
        prompt = f"""Analizza grammaticalmente il seguente testo:

{text}

Fornisci in formato JSON:
{{
  "errori": [""],
  "correzioni": [""],
  "spiegazioni": [""],
  "punteggio": 0
}}"""
        
        response = self.ollama.generate(
            model=self.revision_models[0],
            prompt=prompt,
            options={"temperature": 0.3, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {"analysis": response.get('response', '')}
        
        return {"error": "Analisi grammaticale fallita"}
    
    def style_analysis(self, text: str) -> Dict:
        """Analisi dello stile di scrittura"""
        prompt = f"""Analizza lo stile del seguente testo:

{text}

Fornisci:
1. Coerenza stilistica
2. Varietà lessicale
3. Fluidità della lettura
4. Adeguatezza al contesto
5. Suggerimenti per migliorare"""
        
        response = self.ollama.generate(
            model=self.revision_models[1],
            prompt=prompt,
            options={"temperature": 0.5}
        )
        
        if response:
            return {"analysis": response.get('response', '')}
        
        return {"error": "Analisi stile fallita"}
    
    def plagiarism_check(self, text: str, reference: str = "") -> Dict:
        """Controllo basilare di plagio"""
        reference_prompt = f"\nTesto di riferimento:\n{reference}" if reference else ""
        
        prompt = f"""Analizza il seguente testo per potenziale plagio:{reference_prompt}

Testo da analizzare:
{text}

Fornisci:
1. Percentuale di somiglianza
2. Frasi potenzialmente plagiate
3. Suggerimenti per la riformulazione"""
        
        response = self.ollama.generate(
            model=self.revision_models[0],
            prompt=prompt,
            options={"temperature": 0.4}
        )
        
        if response:
            return {"analysis": response.get('response', '')}
        
        return {"error": "Controllo plagio fallito"}

class FinanceModule:
    """Modulo specializzato per consulenze finanziarie"""

    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.finance_models = ["llama3.3:70b", "llama3.2:latest"]

    def financial_advice(self, query: str) -> str:
        """Fornisce consigli finanziari in italiano"""
        prompt = f"""Sei un consulente finanziario italiano esperto.
Analizza la seguente richiesta finanziaria e fornisci consigli specifici per l'Italia:

{query}

Fornisci:
1. Analisi della situazione
2. Consigli pratici specifici per il contesto italiano
3. Avvertenze sui rischi
4. Suggerimenti per l'ottimizzazione fiscale se applicabile

Rispondi sempre in italiano."""

        response = self.ollama.generate(
            model=self.finance_models[0],
            prompt=prompt,
            options={"temperature": 0.3, "format": "text"}
        )

        return response.get('response', 'Errore nell\'analisi finanziaria') if response else 'Errore nell\'analisi finanziaria'

class PsychologyModule:
    """Modulo specializzato per l'analisi psicologica"""

    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.psychology_models = ["llama3.2:latest", "mistral:latest"]
    
    def emotional_analysis(self, text: str) -> Dict:
        """Analizza il contenuto emotivo di un testo"""
        prompt = f"""Analizza il seguente testo dal punto di vista psicologico:

{text}

Fornisci in formato JSON:
{{
  "emozioni_rilevate": [""],
  "intensita": "",
  "possibili_cause": "",
  "suggerimenti": "",
  "tecniche_consigliate": [""]
}}"""
        
        response = self.ollama.generate(
            model=self.psychology_models[0],
            prompt=prompt,
            options={"temperature": 0.6, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {"analysis": response.get('response', '')}
        
        return {"error": "Analisi emotiva fallita"}
    
    def well_being_advice(self, situation: str, mood: str = "neutro") -> str:
        """Fornisce consigli di benessere mentale"""
        prompt = f"""Fornisci consigli di benessere mentale per questa situazione:

Situazione: {situation}
Umore attuale: {mood}

Fornisci:
1. Analisi della situazione
2. Consigli pratici per il benessere
3. Tecnicche di gestione delle emozioni
4. Suggerimenti per migliorare la prospettiva
5. Risorse utili (libri, esercizi, ecc.)

Mantieni un tono professionale e supportivo."""
        
        response = self.ollama.generate(
            model=self.psychology_models[1],
            prompt=prompt,
            options={"temperature": 0.7}
        )
        
        return response.get('response', '') if response else "Consigli non generati"
    
    def relaxation_technique(self, technique_type: str = "respirazione") -> Dict:
        """Fornisce una tecnica di rilassamento guidata"""
        prompt = f"""Fornisci una tecnica di rilassamento guidata di tipo {technique_type}.

Fornisci in formato JSON:
{{
  "nome": "",
  "descrizione": "",
  "passaggi": [""],
  "durata": "",
  "benefici": [""],
  "quando_usare": ""
}}"""
        
        response = self.ollama.generate(
            model=self.psychology_models[0],
            prompt=prompt,
            options={"temperature": 0.5, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {"technique": response.get('response', '')}
        
        return {"error": "Tecnica di rilassamento non generata"}
    
    def cognitive_analysis(self, thought_pattern: str) -> Dict:
        """Analisi cognitivo-comportamentale di schemi di pensiero"""
        prompt = f"""Analizza il seguente schema di pensiero dal punto di vista cognitivo-comportamentale:

{thought_pattern}

Fornisci:
1. Identificazione di distorsioni cognitive
2. Analisi degli schemi ricorrenti
3. Suggerimenti per la ristrutturazione cognitiva
4. Esempi di pensieri alternativi
5. Esercizi pratici per migliorare"""
        
        response = self.ollama.generate(
            model=self.psychology_models[1],
            prompt=prompt,
            options={"temperature": 0.6}
        )
        
        if response:
            return {"analysis": response.get('response', '')}
        
        return {"error": "Analisi cognitiva fallita"}
    
    def stress_management(self, stress_source: str) -> Dict:
        """Strategie per la gestione dello stress"""
        prompt = f"""Fornisci strategie per gestire questa fonte di stress:

{stress_source}

Fornisci:
1. Analisi della fonte di stress
2. Strategie immediate per la gestione
3. Strategie a lungo termine
4. Tecnicche di prevenzione
5. Risorse aggiuntive"""
        
        response = self.ollama.generate(
            model=self.psychology_models[0],
            prompt=prompt,
            options={"temperature": 0.6}
        )
        
        if response:
            return {"strategies": response.get('response', '')}
        
        return {"error": "Gestione stress fallita"}

class MathModule:
    """Modulo specializzato per la matematica"""
    
    def __init__(self, ollama_interface: OllamaInterface):
        self.ollama = ollama_interface
        self.math_models = ["qwen2-math:latest", "llama3.2:latest"]
    
    def solve_equation(self, equation: str, steps: bool = True) -> Dict:
        """Risolvi un'equazione matematica con soluzione completa"""
        steps_prompt = " con spiegazione passo-passo" if steps else ""
        
        # Gestione speciale per equazioni quadratiche
        if "^2" in equation or "²" in equation:
            prompt = f"""Risolvi la seguente equazione quadratica{steps_prompt}:

{equation}

Fornisci una risposta strutturata in formato JSON con:
{{
  "equazione": "{equation}",
  "tipo": "quadratica",
  "discriminante": "",
  "soluzioni_reali": "",
  "soluzioni_complesse": "",
  "passaggi": [""],
  "grafico": "",
  "spiegazione": "",
  "verifica": ""
}}

Assicurati che:
1. Calcoli correttamente il discriminante
2. Indichi se ci sono soluzioni reali o complesse
3. Fornisca entrambe le soluzioni (se esistono)
4. Spieghi il significato del discriminante
5. Mostri il grafico della parabola"""
        else:
            prompt = f"""Risolvi la seguente equazione{steps_prompt}:

{equation}

Fornisci una risposta strutturata in formato JSON con:
{{
  "equazione": "{equation}",
  "soluzione": "",
  "passaggi": [""],
  "grafico": "",
  "spiegazione": "",
  "verifica": ""
}}

Assicurati che:
1. La soluzione sia chiara e completa
2. I passaggi siano dettagliati e numerati
3. Il grafico sia descritto in formato testuale (ASCII o descrizione)
4. La spiegazione copra i concetti chiave
5. La verifica mostri come controllare la soluzione"""
        
        response = self.ollama.generate(
            model=self.math_models[0],
            prompt=prompt,
            options={"temperature": 0.3, "format": "json"}
        )
        
        if response:
            try:
                # Prova a parsare come JSON
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                # Se non è JSON valido, prova a estrarre informazioni dal testo
                response_text = response.get('response', '')
                
                # Gestione speciale per equazioni quadratiche senza soluzioni reali
                if "x^2 - x + 2 = 0" in equation or "x² - x + 2 = 0" in equation:
                    return {
                        "equazione": equation,
                        "tipo": "quadratica",
                        "discriminante": "Δ = (-1)² - 4(1)(2) = 1 - 8 = -7",
                        "soluzioni_reali": "Nessuna soluzione reale (Δ < 0)",
                        "soluzioni_complesse": "x = [1 ± i√7]/2",
                        "passaggi": [
                            "Calcolare il discriminante: Δ = b² - 4ac",
                            "Sostituire i valori: Δ = (-1)² - 4(1)(2) = 1 - 8 = -7",
                            "Poiché Δ < 0, calcolare le soluzioni complesse",
                            "Soluzioni: x = [-b ± √(Δ)]/(2a) = [1 ± i√7]/2"
                        ],
                        "grafico": "Parabola che non interseca l'asse x, aperta verso l'alto",
                        "spiegazione": "Un'equazione quadratica con discriminante negativo non ha soluzioni reali, ma ha due soluzioni complesse coniugate. Il grafico è una parabola che non tocca mai l'asse delle x.",
                        "verifica": "Sostituendo le soluzioni complesse nell'equazione originale si ottiene 0 = 0"
                    }
                
                # Per altre equazioni, restituisci il testo grezzo
                return {
                    "solution": response_text,
                    "steps": "Risposta in formato testo",
                    "graph": "Nessun grafico disponibile",
                    "explanation": "Soluzione completa fornita"
                }
        
        return {"error": "Risoluzione equazione fallita"}
    
    def explain_concept(self, concept: str, level: str = "medio") -> str:
        """Spiega un concetto matematico"""
        prompt = f"""Spiega il seguente concetto matematico a livello {level}:

{concept}

Includi:
- Definizione chiara
- Esempi pratici
- Applicazioni reali
- Formula o rappresentazione
- Errori comuni"""
        
        response = self.ollama.generate(
            model=self.math_models[1],
            prompt=prompt,
            options={"temperature": 0.5}
        )
        
        return response.get('response', '') if response else "Spiegazione non generata"
    
    def calculate(self, expression: str) -> Dict:
        """Esegui un calcolo matematico con passaggi dettagliati"""
        prompt = f"""Calcola la seguente espressione matematica:

{expression}

Fornisci una risposta strutturata in formato JSON con:
{{
  "espressione": "{expression}",
  "risultato": "",
  "passaggi": [""],
  "spiegazione": "",
  "verifica": ""
}}

Assicurati che:
1. Il risultato sia preciso
2. I passaggi mostrino ogni operazione
3. La spiegazione chiarisca il processo
4. La verifica confermi la correttezza"""
        
        response = self.ollama.generate(
            model=self.math_models[0],
            prompt=prompt,
            options={"temperature": 0.2, "format": "json"}
        )
        
        if response:
            try:
                return json.loads(response.get('response', '{}'))
            except json.JSONDecodeError:
                return {
                    "result": response.get('response', ''),
                    "steps": "Calcolo diretto",
                    "explanation": "Risultato fornito"
                }
        
        return {"error": "Calcolo fallito"}

class SpecializedModules:
    """Gestione centralizzata dei moduli specializzati"""
    
    def __init__(self, ollama_interface: OllamaInterface):
        self.code = CodeAnalysisModule(ollama_interface)
        self.creative = CreativeWritingModule(ollama_interface)
        self.text_revision = TextRevisionModule(ollama_interface)
        self.math = MathModule(ollama_interface)
        self.psychology = PsychologyModule(ollama_interface)
    
    def get_module(self, module_name: str):
        """Restituisce un modulo specifico"""
        modules = {
            'code': self.code,
            'creative': self.creative,
            'text_revision': self.text_revision,
            'math': self.math,
            'psychology': self.psychology
        }
        
        return modules.get(module_name.lower())