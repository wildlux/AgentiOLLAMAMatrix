@echo off

:: Script di avvio per Windows

echo Avvio dell'agente AI e del sistema MCP...

:: Verifica se Docker è installato
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Docker è installato. Vuoi avviare l'applicazione con Docker? (s/n)
    set /p response="Scelta: "
    if /i "%response%" equ "s" (
        echo Avvio con Docker...
        echo L'applicazione sarà disponibile all'indirizzo: http://localhost:5001
        :: Verifica se docker-compose è disponibile come plugin
        docker compose version >nul 2>&1
        if %errorlevel% equ 0 (
            docker compose up --build
        ) else (
            echo docker-compose non è disponibile. Assicurati di avere Docker Compose installato.
            pause
            exit /b 1
        )
        exit /b 0
    )
)

:: Verifica se Python è installato
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non è installato. Installalo prima di procedere.
    pause
    exit /b 1
)

:: Verifica se Flask è installato
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Flask non è installato. Installazione in corso...
    pip install flask
)

:: Avvia il backend Flask
cd "%~dp0backend"
python app.py

echo Backend Flask avviato con successo!
echo L'applicazione è disponibile all'indirizzo: http://localhost:5000
pause