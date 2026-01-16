# Dockerfile per l'agente AI e il sistema MCP

# Utilizza un'immagine Python ufficiale
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file necessari
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir flask

# Espone la porta del backend Flask
EXPOSE 5000

# Avvia il backend Flask
CMD ["python", "backend/app.py"]