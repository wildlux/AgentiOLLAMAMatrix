#!/bin/bash

# 🛑 Script di arresto per AgentiOLLAMAMatrix
# Versione: 1.0
# Data: 2024-01-17
# Autore: Mistral Vibe

echo "🛑 Arresto Sistema AgentiOLLAMAMatrix..."
echo "========================================"

# Funzione per fermare un processo
stop_process() {
    local name=$1
    local pattern=$2
    
    echo "🔍 Verifica $name..."
    
    if pgrep -f "$pattern" > /dev/null; then
        echo "⚠️  $name è in esecuzione. Arresto..."
        pkill -f "$pattern"
        sleep 2
        
        if pgrep -f "$pattern" > /dev/null; then
            echo "❌ Impossibile fermare $name. Uccisione forzata..."
            pkill -9 -f "$pattern"
        else
            echo "✅ $name fermato"
        fi
    else
        echo "✅ $name non è in esecuzione"
    fi
}

# Ferma frontend
stop_process "Frontend" "python3.*frontend_server.py"

# Ferma backend
stop_process "Backend" "python3.*wsgi_main.py"

# Ferma Ollama (opzionale)
echo ""
echo "🤖 Vuoi fermare anche Ollama? (s/n)"
read -r response
if [[ "$response" =~ ^([sS]|[yY])$ ]]; then
    stop_process "Ollama" "ollama serve"
else
    echo "✅ Ollama lasciato in esecuzione"
fi

# Rimuovi file PID
if [ -f "backend.pid" ]; then
    rm backend.pid
    echo "✅ File backend.pid rimosso"
fi

if [ -f "frontend.pid" ]; then
    rm frontend.pid
    echo "✅ File frontend.pid rimosso"
fi

echo ""
echo "========================================"
echo "🎉 Sistema AgentiOLLAMAMatrix fermato!"
echo "========================================"