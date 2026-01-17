#!/bin/bash

# 🚀 Lanciatore Universale per AgentiOLLAMAMatrix
# Versione: 2.0
# Data: 2024-01-17
# Autore: Mistral Vibe

echo "🤖 Avvio Sistema AgentiOLLAMAMatrix..."
echo "========================================"

# Funzione per controllare i prerequisiti
check_prerequisites() {
    echo "🔍 Controllo prerequisiti..."
    
    # Controlla Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 non trovato. Installalo con:"
        echo "   sudo apt install python3 python3-pip"
        exit 1
    fi
    
    # Controlla pip
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 non trovato. Installalo con:"
        echo "   sudo apt install python3-pip"
        exit 1
    fi
    
    # Controlla Ollama
    if ! command -v ollama &> /dev/null; then
        echo "❌ Ollama non trovato. Installalo da https://ollama.ai"
        exit 1
    fi
    
    echo "✅ Tutti i prerequisiti sono soddisfatti!"
}

# Funzione per avviare Ollama
start_ollama() {
    echo "🔧 Configurazione Ollama..."
    
    # Avvia Ollama se non è attivo
    if ! pgrep -f "ollama serve" > /dev/null; then
        echo "🚀 Avvio Ollama..."
        nohup ollama serve > /tmp/ollama.log 2>&1 &
        sleep 5
        
        # Verifica che Ollama sia avviato
        if ! pgrep -f "ollama serve" > /dev/null; then
            echo "❌ Impossibile avviare Ollama. Controlla i log in /tmp/ollama.log"
            exit 1
        fi
    else
        echo "✅ Ollama è già in esecuzione"
    fi
    
    # Verifica modelli
    echo "📋 Verifica modelli disponibili..."
    ollama list
}

# Funzione per installare dipendenze
install_dependencies() {
    echo "📦 Installazione dipendenze Python..."
    
    # Installa dipendenze di base
    pip3 install -q flask requests python-dotenv
    
    # Installa dipendenze specifiche
    if [ -f "requirements.txt" ]; then
        pip3 install -q -r requirements.txt
    fi
    
    if [ -f "requirements-dev.txt" ]; then
        pip3 install -q -r requirements-dev.txt
    fi
    
    echo "✅ Dipendenze installate"
}

# Funzione per avviare il backend
start_backend() {
    echo "🔧 Avvio backend Flask..."
    
    cd backend || { echo "❌ Cartella backend non trovata"; exit 1; }
    
    # Verifica se il backend è già in esecuzione
    if pgrep -f "python3.*wsgi_main.py" > /dev/null; then
        echo "⚠️  Backend già in esecuzione. Riavvio..."
        pkill -f "python3.*wsgi_main.py"
        sleep 2
    fi
    
    # Avvia il backend in background
    nohup python3 wsgi_main.py > /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    
    # Attendi che il backend sia pronto
    sleep 3
    
    # Verifica che il backend sia avviato
    if ! pgrep -f "python3.*wsgi_main.py" > /dev/null; then
        echo "❌ Impossibile avviare il backend. Controlla i log in /tmp/backend.log"
        exit 1
    fi
    
    echo "✅ Backend avviato (PID: $BACKEND_PID)"
    cd ..
}

# Funzione per avviare il frontend
start_frontend() {
    echo "🌐 Avvio frontend..."
    
    # Verifica se il frontend è già in esecuzione
    if pgrep -f "python3.*http.server.*8080" > /dev/null; then
        echo "⚠️  Frontend già in esecuzione. Riavvio..."
        pkill -f "python3.*http.server.*8080"
        sleep 2
    fi
    
    # Avvia il frontend personalizzato con reindirizzamento automatico
    echo "🌐 Avvio frontend personalizzato..."
    nohup python3 frontend_server.py > /tmp/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    
    # Attendi che il frontend sia pronto
    sleep 2
    
    # Verifica che il frontend sia avviato
    if ! pgrep -f "python3.*frontend_server.py" > /dev/null; then
        echo "❌ Impossibile avviare il frontend. Controlla i log in /tmp/frontend.log"
        exit 1
    fi
    
    echo "✅ Frontend avviato (PID: $FRONTEND_PID)"
    echo "📋 Reindirizzamento automatico da / a /static/index.html"
}

# Funzione per scaricare modelli
download_models() {
    echo "📥 Scaricamento modelli..."
    
    if [ -f "download_models.sh" ]; then
        chmod +x download_models.sh
        ./download_models.sh
    else
        echo "⚠️  File download_models.sh non trovato. Scarica manualmente i modelli."
    fi
}

# Funzione per mostrare lo stato del sistema
show_status() {
    echo ""
    echo "========================================"
    echo "📊 Stato del Sistema"
    echo "========================================"
    
    # Stato Ollama
    if pgrep -f "ollama serve" > /dev/null; then
        echo "✅ Ollama: Attivo"
    else
        echo "❌ Ollama: Non attivo"
    fi
    
    # Stato Backend
    if pgrep -f "python3.*wsgi_main.py" > /dev/null; then
        echo "✅ Backend: Attivo (http://localhost:54324)"
    else
        echo "❌ Backend: Non attivo"
    fi
    
    # Stato Frontend
    if pgrep -f "python3.*http.server.*8080" > /dev/null; then
        echo "✅ Frontend: Attivo (http://localhost:8080)"
    else
        echo "❌ Frontend: Non attivo"
    fi
    
    echo ""
    echo "📋 Modelli disponibili:"
    ollama list
    
    echo ""
    echo "========================================"
    echo "🎯 Accesso al Sistema"
    echo "========================================"
    echo "📱 Frontend: http://localhost:8080 (reindirizza automaticamente)"
    echo "🔗 Backend: http://localhost:54324"
    echo "📖 Documentazione: docs/README.md"
    echo ""
    echo "💡 Il frontend ora reindirizza automaticamente da / a /static/index.html"
    echo "🛑 Per fermare il sistema: ./stop.sh"
    echo "========================================"
}

# Funzione per gestire gli argomenti
handle_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --download-models|-d)
                DOWNLOAD_MODELS=true
                shift
                ;;
            --no-ollama|-n)
                SKIP_OLLAMA=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "❌ Argomento sconosciuto: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Funzione per mostrare l'aiuto
show_help() {
    echo "Utilizzo: $0 [OPZIONI]"
    echo ""
    echo "Opzioni:"
    echo "  -d, --download-models  Scarica i modelli prima di avviare"
    echo "  -n, --no-ollama        Salta l'avvio di Ollama"
    echo "  -h, --help             Mostra questo messaggio di aiuto"
    echo ""
    echo "Esempi:"
    echo "  $0                    Avvia normalmente"
    echo "  $0 -d                 Scarica modelli e avvia"
    echo "  $0 -n                 Avvia senza Ollama"
}

# Main
main() {
    # Gestione argomenti
    handle_arguments "$@"
    
    # Controllo prerequisiti
    check_prerequisites
    
    # Installazione dipendenze
    install_dependencies
    
    # Avvio Ollama (se non saltato)
    if [ "$SKIP_OLLAMA" != "true" ]; then
        start_ollama
    else
        echo "⚠️  Avvio senza Ollama (modalità offline)"
    fi
    
    # Scarica modelli (se richiesto)
    if [ "$DOWNLOAD_MODELS" = "true" ]; then
        download_models
    fi
    
    # Avvio backend
    start_backend
    
    # Avvio frontend
    start_frontend
    
    # Mostra stato
    show_status
    
    echo ""
    echo "🎉 Sistema AgentiOLLAMAMatrix avviato con successo!"
    echo ""
    
    # Mantieni attivo
    wait
}

# Esegui main con tutti gli argomenti
main "$@"