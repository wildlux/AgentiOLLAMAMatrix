#!/bin/bash

# Merged Agent Management System Launcher

echo "🤖 Avvio Sistema Agenti Unificato..."

# Controlla se Ollama è installato
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama non trovato. Installalo da https://ollama.ai"
    exit 1
fi

# Avvia Ollama se non è attivo
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "🚀 Avvio Ollama..."
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
fi

# Scarica modelli se richiesti
if [ "$1" = "download-models" ]; then
    echo "📥 Scaricamento modelli top..."
    ./download_models.sh
fi

# Avvia backend
echo "🔧 Avvio backend..."
cd backend
python3 wsgi_main.py &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid

# Avvia frontend
echo "🌐 Avvio frontend..."
cd ../static
python3 -m http.server 8080 --bind 0.0.0.0 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid

echo "✅ Sistema avviato!"
echo "📱 Frontend: http://localhost:8080"
echo "🔗 Backend: http://localhost:54324"
echo "🛑 Per fermare: ./stop.sh"

# Mantieni attivo
wait