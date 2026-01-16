#!/bin/bash

# Status check for merged system

echo "📊 Stato del Sistema Agenti Unificato"
echo "===================================="

# Controlla backend
if [ -f backend.pid ] && kill -0 $(cat backend.pid) 2>/dev/null; then
    echo "✅ Backend: ATTIVO (PID: $(cat backend.pid))"
else
    echo "❌ Backend: NON ATTIVO"
fi

# Controlla frontend
if [ -f frontend.pid ] && kill -0 $(cat frontend.pid) 2>/dev/null; then
    echo "✅ Frontend: ATTIVO (PID: $(cat frontend.pid))"
else
    echo "❌ Frontend: NON ATTIVO"
fi

# Controlla Ollama
if pgrep -f "ollama serve" > /dev/null; then
    echo "✅ Ollama: ATTIVO"
    echo "📚 Modelli disponibili:"
    ollama list 2>/dev/null | head -10
else
    echo "❌ Ollama: NON ATTIVO"
fi

# Controlla porte
echo ""
echo "🔍 Controllo porte:"
netstat -tln 2>/dev/null | grep -E ":54324|:8080" || echo "⚠️ Porte non in ascolto"

echo ""
echo "💡 Comandi:"
echo "  ./launcher.sh          - Avvia sistema"
echo "  ./launcher.sh download-models - Avvia e scarica modelli"
echo "  ./stop.sh              - Ferma sistema"