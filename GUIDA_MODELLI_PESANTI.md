# Guida all'Uso dei Modelli Pesanti

## 📋 Panoramica
Questa guida spiega come utilizzare i modelli LLM più pesanti (come qwen2.5:14b) con il sistema Assistente AI.

## 💻 Requisiti di Sistema

### RAM Minima Raccomandata:
- **qwen2.5:14b**: 16GB RAM
- **llama3.3:70b**: 32GB RAM
- **qwen2.5:72b**: 32GB+ RAM

### Spazio Disco:
- **qwen2.5:14b**: ~9GB
- **llama3.3:70b**: ~40GB
- **qwen2.5:72b**: ~40GB

## 🚀 Come Utilizzare i Modelli Pesanti

### 1. Scaricare il Modello
```bash
# Scarica qwen2.5:14b (il modello richiesto)
ollama pull qwen2.5:14b-instruct-q4_K_M

# Oppure usa lo script automatico
./download_models.sh
```

### 2. Verifica Download
```bash
ollama list | grep qwen2.5
```

### 3. Avvia il Sistema
```bash
./start.sh
```

### 4. Seleziona il Modello Pesante
- Apri http://localhost:8080
- Nel menu laterale, seleziona "Modello AI"
- Scegli "qwen2.5:14b-instruct-q4_K_M" dall'elenco
- Oppure usa il pulsante "🔥 Modelli Pesanti" nella chat

## ⚙️ Ottimizzazioni per Modelli Pesanti

### Context Window Automatica
Il sistema adatta automaticamente la context window basata sulla RAM:
- 7.6GB RAM → 4096 tokens (aumentato per modelli pesanti)
- 16GB+ RAM → 8192 tokens
- 32GB+ RAM → 16384 tokens

### Suggerimenti per Performance
1. **Chiudi altre applicazioni** durante l'uso
2. **Usa SSD** per velocità di caricamento
3. **Aumenta swap** se RAM insufficiente:
   ```bash
   sudo fallocate -l 16G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

## 🎯 Quando Usare Modelli Pesanti

### qwen2.5:14b-instruct-q4_K_M
**Ideale per:**
- Analisi complesse e ragionamento avanzato
- Scrittura creativa e letteratura
- Traduzioni accurate
- Analisi tecnica dettagliata
- Risposta a domande profonde

### Confronto con Modelli Leggeri

| Aspetto | mistral:7b | qwen2.5:14b |
|---------|------------|-------------|
| Velocità | ⚡ Molto Veloce | 🐌 Lento |
| Qualità | ⭐ Buona | ⭐⭐⭐⭐ Eccellente |
| RAM | 4GB | 16GB+ |
| Context | 4096 tokens | 8192+ tokens |
| Uso | Chat veloce | Analisi profonda |

## 🔧 Troubleshooting

### Errore "out of memory"
```
Soluzioni:
1. Chiudi altre applicazioni
2. Aumenta swap space
3. Usa modello più leggero temporaneamente
4. Riavvia il sistema
```

### Modello non risponde
```
Verifica:
1. ollama serve è attivo
2. Modello scaricato completamente
3. RAM sufficiente
4. Context window non troppo alta
```

### Performance lenta
```
Ottimizzazioni:
1. Usa SSD invece di HDD
2. Chiudi browser tabs non necessari
3. Aumenta RAM se possibile
4. Usa modelli più piccoli per task semplici
```

## 📊 Monitoraggio Risorse

Durante l'uso di modelli pesanti, monitora:
```bash
# RAM usage
free -h

# CPU usage
top -p $(pgrep ollama)

# Disco I/O
iotop
```

## 🎉 Conclusioni

I modelli pesanti offrono qualità superiore ma richiedono più risorse.
Usali per task che richiedono ragionamento profondo e analisi complessa.

Per uso quotidiano, mantieni mistral:7b come default e passa ai modelli pesanti solo quando necessario.