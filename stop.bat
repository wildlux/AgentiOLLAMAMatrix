@echo off

:: 🛑 Script di arresto per AgentiOLLAMAMatrix
:: Versione: 1.0
:: Data: 2024-01-17
:: Autore: Mistral Vibe

echo 🛑 Arresto Sistema AgentiOLLAMAMatrix...
echo ========================================

:: Funzione per fermare un processo
:stop_process
setlocal
set name=%1
set pattern=%2

echo 🔍 Verifica %name%...

tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "%pattern%" >NUL
if "%ERRORLEVEL%"=="0" (
    echo ⚠️  %name% è in esecuzione. Arresto...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq %pattern%" >nul 2>&1
    timeout /t 2 /nobreak >nul
    
    tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "%pattern%" >NUL
    if "%ERRORLEVEL%"=="0" (
        echo ❌ Impossibile fermare %name%. Uccisione forzata...
        taskkill /F /IM python.exe /FI "WINDOWTITLE eq %pattern%" >nul 2>&1
    ) else (
        echo ✅ %name% fermato
    )
) else (
    echo ✅ %name% non è in esecuzione
)
endlocal
goto :eof

:: Ferma frontend
call :stop_process "Frontend" "frontend_server.py"

:: Ferma backend
call :stop_process "Backend" "wsgi_main.py"

:: Ferma Ollama (opzionale)
echo.
echo 🤖 Vuoi fermare anche Ollama? (s/n)
set /p response="Scelta: "
if /i "%response%" equ "s" (
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
    if "%ERRORLEVEL%"=="0" (
        echo ⚠️  Ollama è in esecuzione. Arresto...
        taskkill /F /IM ollama.exe >nul 2>&1
        timeout /t 2 /nobreak >nul
        
        tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
        if "%ERRORLEVEL%"=="0" (
            echo ❌ Impossibile fermare Ollama. Uccisione forzata...
            taskkill /F /IM ollama.exe >nul 2>&1
        ) else (
            echo ✅ Ollama fermato
        )
    ) else (
        echo ✅ Ollama non è in esecuzione
    )
) else (
    echo ✅ Ollama lasciato in esecuzione
)

:: Rimuovi file PID
if exist "backend.pid" (
    del backend.pid
    echo ✅ File backend.pid rimosso
)

if exist "frontend.pid" (
    del frontend.pid
    echo ✅ File frontend.pid rimosso
)

echo.
echo ========================================
echo 🎉 Sistema AgentiOLLAMAMatrix fermato!
echo ========================================
echo.
echo Premi un tasto per uscire...
pause