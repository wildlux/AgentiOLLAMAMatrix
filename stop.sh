#!/bin/bash

# Stop script for merged system

echo "🛑 Fermando il sistema agenti..."

# Ferma backend
if [ -f backend.pid ]; then
    BACKEND_PID=$(cat backend.pid)
    kill $BACKEND_PID 2>/dev/null && echo "✅ Backend fermato" || echo "⚠️ Backend già fermato"
    rm -f backend.pid
fi

# Ferma frontend
if [ -f frontend.pid ]; then
    FRONTEND_PID=$(cat frontend.pid)
    kill $FRONTEND_PID 2>/dev/null && echo "✅ Frontend fermato" || echo "⚠️ Frontend già fermato"
    rm -f frontend.pid
fi

# Ferma processi Python
pkill -f "wsgi_main.py" 2>/dev/null && echo "✅ Processi backend fermati"
pkill -f "http.server" 2>/dev/null && echo "✅ Processi frontend fermati"

echo "✋ Sistema fermato"