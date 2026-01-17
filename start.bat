@echo off

:: 🚀 Lanciatore Universale per AgentiOLLAMAMatrix
:: Versione: 2.0
:: Data: 2024-01-17
:: Autore: Mistral Vibe

echo 🤖 Avvio Sistema AgentiOLLAMAMatrix...
echo ========================================

:: Imposta variabili globali
set DOWNLOAD_MODELS=false
set SKIP_OLLAMA=false

:: Funzione per mostrare l'aiuto
:show_help
echo Utilizzo: %~nx0 [OPZIONI]
echo 🎯 Accesso al Sistema
echo ========================================
echo 📱 Frontend: http://localhost:8080
echo 🔗 Backend: http://localhost:54324
echo 📖 Documentazione: docs/README.md
echo.
echo 🛑 Per fermare il sistema: stop.bat
echo ========================================
=======
echo.
echo ========================================
echo 🎯 Accesso al Sistema
echo ========================================
echo 📱 Frontend: http://localhost:8080 (reindirizza automaticamente)
echo 🔗 Backend: http://localhost:54324
echo 📖 Documentazione: docs/README.md
echo.
echo 💡 Il frontend ora reindirizza automaticamente da / a /static/index.html
echo 🛑 Per fermare il sistema: stop.bat
echo ========================================Opzioni:
echo   -d, --download-models  Scarica i modelli prima di avviare
echo   -n, --no-ollama        Salta l'avvio di Ollama
echo   -h, --help             Mostra questo messaggio di aiuto
echo.
echo Esempi:
echo   %~nx0                    Avvia normalmente
echo   %~nx0 -d                 Scarica modelli e avvia
echo   %~nx0 -n                 Avvia senza Ollama
goto :eof

:: Funzione per gestire gli argomenti
:handle_arguments
if "%1"=="" goto :eof

if "%1"=="-d" (
    set DOWNLOAD_MODELS=true
    shift
    goto handle_arguments
)

if "%1"=="--download-models" (
    set DOWNLOAD_MODELS=true
    shift
    goto handle_arguments
)

if "%1"=="-n" (
    set SKIP_OLLAMA=true
    shift
    goto handle_arguments
)

if "%1"=="--no-ollama" (
    set SKIP_OLLAMA=true
    shift
    goto handle_arguments
)

if "%1"=="-h" (
    call :show_help
    exit /b 0
)

if "%1"=="--help" (
    call :show_help
    exit /b 0
)

echo ❌ Argomento sconosciuto: %1
call :show_help
exit /b 1

:: Funzione per controllare i prerequisiti
:check_prerequisites
echo 🔍 Controllo prerequisiti...

:: Controlla Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato. Installalo da https://www.python.org
    pause
    exit /b 1
)

:: Controlla pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip non trovato. Installalo con: python -m ensurepip --upgrade
    pause
    exit /b 1
)

:: Controlla Ollama (solo se non saltato)
if "%SKIP_OLLAMA%"=="false" (
    ollama --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Ollama non trovato. Installalo da https://ollama.ai
        pause
        exit /b 1
    )
)

echo ✅ Tutti i prerequisiti sono soddisfatti!
goto :eof

:: Funzione per avviare Ollama
:start_ollama
echo 🔧 Configurazione Ollama...

:: Verifica se Ollama è già in esecuzione
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Ollama è già in esecuzione
) else (
    echo 🚀 Avvio Ollama...
    start "" "%~dp0ollama.exe" serve
    timeout /t 5 /nobreak >nul
    
    :: Verifica che Ollama sia avviato
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        echo ✅ Ollama avviato con successo
    ) else (
        echo ❌ Impossibile avviare Ollama
        pause
        exit /b 1
    )
)

echo 📋 Verifica modelli disponibili...
ollama list

goto :eof

:: Funzione per installare dipendenze
:install_dependencies
echo 📦 Installazione dipendenze Python...

:: Installa dipendenze di base
python -m pip install -q flask requests python-dotenv

:: Installa dipendenze specifiche
if exist "requirements.txt" (
    python -m pip install -q -r requirements.txt
)

if exist "requirements-dev.txt" (
    python -m pip install -q -r requirements-dev.txt
)

echo ✅ Dipendenze installate
goto :eof

:: Funzione per avviare il backend
:start_backend
echo 🔧 Avvio backend Flask...

cd "%~dp0backend" || (
    echo ❌ Cartella backend non trovata
    pause
    exit /b 1
)

:: Verifica se il backend è già in esecuzione
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "wsgi_main.py" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  Backend già in esecuzione. Riavvio...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq wsgi_main.py" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

:: Avvia il backend in background
start "Backend Flask" /MIN python wsgi_main.py

timeout /t 3 /nobreak >nul

:: Verifica che il backend sia avviato
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "wsgi_main.py" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Backend avviato
) else (
    echo ❌ Impossibile avviare il backend
    pause
    exit /b 1
)

cd ..
goto :eof

:: Funzione per avviare il frontend
:start_frontend
echo 🌐 Avvio frontend...

:: Verifica se il frontend è già in esecuzione
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "http.server" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  Frontend già in esecuzione. Riavvio...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq http.server" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

:: Avvia il frontend personalizzato
start "Frontend" /MIN python frontend_server.py

:: Verifica che il frontend sia avviato
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "frontend_server.py" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Frontend avviato
) else (
    echo ❌ Impossibile avviare il frontend
    pause
    exit /b 1
)

goto :eof

:: Funzione per scaricare modelli
:download_models
echo 📥 Scaricamento modelli...

if exist "download_models.bat" (
    call download_models.bat
) else (
    echo ⚠️  File download_models.bat non trovato. Scarica manualmente i modelli.
)

goto :eof

:: Funzione per mostrare lo stato del sistema
:show_status
echo.
echo ========================================
echo 📊 Stato del Sistema
echo ========================================

:: Stato Ollama
if "%SKIP_OLLAMA%"=="false" (
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        echo ✅ Ollama: Attivo
    ) else (
        echo ❌ Ollama: Non attivo
    )
) else (
    echo ⚠️  Ollama: Modalità offline
)

:: Stato Backend
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "wsgi_main.py" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Backend: Attivo (http://localhost:54324)
) else (
    echo ❌ Backend: Non attivo
)

:: Stato Frontend
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "http.server" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Frontend: Attivo (http://localhost:8080)
) else (
    echo ❌ Frontend: Non attivo
)

echo.
echo 📋 Modelli disponibili:
ollama list

echo.
echo ========================================
echo 🎯 Accesso al Sistema
echo ========================================
echo 📱 Frontend: http://localhost:8080
echo 🔗 Backend: http://localhost:54324
echo 📖 Documentazione: docs/README.md
echo.
echo 🛑 Per fermare il sistema: stop.bat
echo ========================================

goto :eof

:: Main
:main
:: Gestione argomenti
call :handle_arguments %*

:: Controllo prerequisiti
call :check_prerequisites

:: Installazione dipendenze
call :install_dependencies

:: Avvio Ollama (se non saltato)
if "%SKIP_OLLAMA%"=="false" (
    call :start_ollama
) else (
    echo ⚠️  Avvio senza Ollama (modalità offline)
)

:: Scarica modelli (se richiesto)
if "%DOWNLOAD_MODELS%"=="true" (
    call :download_models
)

:: Avvio backend
call :start_backend

:: Avvio frontend
call :start_frontend

:: Mostra stato
call :show_status

echo.
echo 🎉 Sistema AgentiOLLAMAMatrix avviato con successo!
echo.
echo Premi un tasto per uscire...
pause

exit /b 0

:: Esegui main con tutti gli argomenti
call :main %*