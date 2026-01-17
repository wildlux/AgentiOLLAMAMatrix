# AgentiOLLAMAMatrix
Sistema Multi-Agente con Ollama - Assistente AI Italiano

## 🚀 Caratteristiche
- 🤖 Agenti specializzati per diverse categorie
- 💰 Assistente finanziario italiano
- 🧮 Risolvitore matematico avanzato
- 💻 Sviluppatore di codice esperto
- 📝 Scrittore e editor creativo
- 🎯 42 modelli Ollama ottimizzati
- 🔧 Context window adattiva
- 🌐 Interfaccia web moderna

## 📦 Installazione Rapida

```bash
git clone https://github.com/wildlux/AgentiOLLAMAMatrix.git
cd AgentiOLLAMAMatrix
pip install -r requirements.txt
./start.sh
```

Apri http://localhost:8080

## 🏗️ Architettura
- **Backend**: Python Flask + Ollama API
- **Frontend**: HTML/CSS/JS moderno
- **AI**: 42 modelli classificati per categoria
- **Ottimizzazioni**: Context window adattiva, caching intelligente

## 📋 Modelli Supportati
- **Finanza**: qwen2.5:14b-instruct-q4_K_M
- **Matematica**: qwen2-math:latest
- **Programmazione**: qwen2.5-coder:7b
- **Scrittura**: Llama 3.3:70b
- **Reasoning**: DeepSeek R1
- **Multi-agente**: Nous Hermes 2 Pro

## 🎯 Uso
1. **Avvia il sistema**: `./start.sh`
2. **Accedi al frontend**: http://localhost:8080 (reindirizzamento automatico)
3. **API Backend**: http://localhost:54324
4. **Autenticazione API**: Usa una delle chiavi demo:
   - `demo_key_123`
   - `admin_key_456`
   - `test_key_789`

## 🔐 Sicurezza
- **Autenticazione API**: Tutte le route `/api/*` richiedono una chiave API
- **HTTPS**: Forzato automaticamente con HSTS
- **Rate Limiting**: 200 richieste/giorno, 50/ora
- **CORS**: Restrizioni per origini non autorizzate
- **CSP**: Content Security Policy attiva
- **Logging**: Audit completo con IP e timestamp

**Esempio di richiesta API:**
```bash
curl -X GET http://localhost:54324/api/agenti \
     -H "X-API-KEY: demo_key_123"
```

## 📚 Documentazione
- [Guida Completa](docs/README.md)
- [Classificazione Modelli](progetto_analisi.txt)
- [Ottimizzazioni](GUIDA_MODELLI_PESANTI.md)

---
*Sistema sviluppato con ❤️ per assistenti AI locali*
