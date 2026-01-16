#!/bin/bash

# Script per scaricare i modelli Ollama migliori

echo "🤖 Scaricamento modelli Ollama top..."

# Modelli raccomandati
MODELS=(
    "llama3.3:70b"      # Migliore generale
    "qwen2.5:72b"       # Avanzato
    "deepseek-coder:33b" # Codice
    "qwen2.5-math:72b"  # Matematica
    "mistral:7b"        # Veloce
)

for model in "${MODELS[@]}"; do
    echo "📥 Scaricando $model..."
    ollama pull "$model"
    if [ $? -eq 0 ]; then
        echo "✅ $model scaricato con successo"
    else
        echo "❌ Errore scaricando $model"
    fi
done

echo "🎉 Tutti i modelli scaricati!"
echo "💡 Puoi ora avviare il server con ./launcher.sh"