# 🛠️ Guida per Sviluppatori - AgentiOLLAMAMatrix

Questa guida è rivolta agli sviluppatori che desiderano contribuire o estendere il sistema AgentiOLLAMAMatrix.

## 📦 Struttura del Progetto

```
agente_ai/
├── backend/                  # Backend Flask
│   ├── app.py                # Applicazione principale
│   ├── routes/               # Route API
│   ├── agent/                # Moduli agenti AI
│   └── config/               # Configurazioni
├── src/                     # Codice sorgente principale
│   ├── models/               # Modelli dati
│   │   └── agente_ai.py      # Classe AgenteAI
│   └── mcp/                 # Multi-Model Communication Protocol
│       └── mcp.py            # Classe MCP
├── tests/                   # Test unitari
├── docs/                    # Documentazione
└── static/                  # Frontend statico
```

## 🏗️ Architettura Tecnica

### 1. Backend Flask

Il backend è implementato con Flask e fornisce le seguenti API:

- **GET /api/agenti**: Elenca tutti gli agenti
- **POST /api/agenti**: Aggiunge un nuovo agente
- **DELETE /api/agenti/<nome>**: Rimuove un agente
- **POST /api/messaggi**: Invia messaggi tra agenti
- **GET /api/stanza**: Ottiene la cronologia della stanza

### 2. Sistema MCP (Multi-Model Communication Protocol)

Il cuore del sistema è la classe `MCP` che gestisce:
- Comunicazione tra agenti AI
- Cronologia della stanza
- Gestione degli stati degli agenti

### 3. Classe AgenteAI

La classe base `AgenteAI` implementa:
- Identità dell'agente (nome, ruolo, stato)
- Metodi di risposta ai messaggi
- Gestione dello stato

## 🔧 Configurazione

### Variabili d'Ambiente

Crea un file `.env` nella root del progetto:

```env
# Configurazione Flask
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your_secret_key_here

# Configurazione Ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=qwen2.5:14b-instruct-q4_K_M

# Configurazione API
API_KEY=demo_key_123
```

### Dipendenze

Installa le dipendenze con:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Per sviluppo
```

## 🚀 Sviluppo

### Avvio in Modalità Sviluppo

```bash
# Avvia il backend Flask
cd backend
python app.py

# Avvia il frontend (se applicabile)
cd static
python -m http.server 8080
```

### Esecuzione Test

```bash
# Esegui tutti i test
pytest

# Esegui test specifici
pytest tests/test_agente_ai.py
pytest tests/test_mcp.py
```

## 📝 Best Practice

### 1. Codice Python

- Segui PEP 8 per lo stile del codice
- Usa type hints per tutte le funzioni
- Aggiungi docstring complete
- Mantieni le funzioni brevi e focalizzate

### 2. Sicurezza

- Non esporre chiavi API nel codice
- Usa sempre HTTPS in produzione
- Valida tutti gli input utente
- Implementa rate limiting per le API

### 3. Testing

- Scrivi test unitari per ogni nuova funzione
- Mantieni una copertura dei test > 80%
- Usa test di integrazione per i flussi principali
- Esegui i test prima di ogni commit

## 🔄 Estensione del Sistema

### Aggiungere un Nuovo Tipo di Agente

1. Crea una nuova classe che estende `AgenteAI`:

```python
from models.agente_ai import AgenteAI

class AgenteFinanziario(AgenteAI):
    def __init__(self, nome: str):
        super().__init__(nome, ruolo="Esperto Finanziario")
        self.specializzazione = "analisi di mercato"
    
    def rispondi(self, messaggio: str) -> str:
        # Logica specifica per risposte finanziarie
        return f"{self.nome}: Analisi finanziaria di '{messaggio}'"
```

2. Registra il nuovo agente nel sistema MCP:

```python
agente_finanziario = AgenteFinanziario(nome="Mario")
mcp.aggiungi_agente(agente_finanziario)
```

### Aggiungere una Nuova API

1. Crea una nuova route in `backend/app.py`:

```python
@app.route('/api/analisi', methods=['POST'])
def esegui_analisi():
    """Esegue un'analisi finanziaria."""
    data = request.get_json()
    # Logica di analisi
    return jsonify({'risultato': 'analisi completata'}), 200
```

2. Aggiungi la documentazione dell'API in Swagger/OpenAPI

## 🐛 Debugging

### Log

I log sono salvati in:
- `logs/backend.log` - Log del backend
- `logs/agenti.log` - Log degli agenti

### Strumenti di Debug

- **Flask Debug Toolbar**: Per debug delle richieste HTTP
- **PyCharm Debugger**: Per debug interattivo
- **Postman**: Per testare le API

## 📦 Deployment

### Requisiti di Produzione

- Python 3.8+
- Flask 2.0+
- Ollama 0.1.0+
- Nginx (per reverse proxy)
- Gunicorn (per WSGI)

### Configurazione Nginx

```nginx
server {
    listen 80;
    server_name tuo-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /percorsoprogetto/static/;
    }
}
```

### Avvio con Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## 🤝 Contributi

### Workflow Git

1. Fork il repository
2. Crea un branch per la feature: `git checkout -b feature/nome-feature`
3. Commit le modifiche: `git commit -m "Aggiunta nuova feature"`
4. Push: `git push origin feature/nome-feature`
5. Apri una Pull Request

### Linee Guida per i Commit

- Usa messaggi di commit chiari e descrittivi
- Mantieni i commit piccoli e focalizzati
- Aggiungi riferimenti a issue se applicabile
- Usa il formato: `tipo: descrizione` (es. `feat: aggiunta nuovo agente`)

## 📚 Risorse

- [Documentazione Flask](https://flask.palletsprojects.com/)
- [Documentazione Ollama](https://ollama.ai/docs)
- [PEP 8 - Style Guide Python](https://peps.python.org/pep-0008/)
- [Testing in Python](https://docs.pytest.org/)

---

*Questa guida è in continua evoluzione. Contributi e suggerimenti sono benvenuti!*