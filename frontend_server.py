#!/usr/bin/env python3
"""
Server frontend personalizzato per AgentiOLLAMAMatrix.
Serve i file statici e reindirizza automaticamente alla pagina principale.
"""

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os
import sys

class CustomHandler(SimpleHTTPRequestHandler):
    """Handler personalizzato per reindirizzamento automatico"""
    
    def do_GET(self):
        """Gestione delle richieste GET con reindirizzamento automatico"""
        
        # Reindirizza la root alla pagina principale
        if self.path == '/' or self.path == '/index.html':
            self.send_response(302)
            self.send_header('Location', '/static/index.html')
            self.end_headers()
            return
        
        # Reindirizza anche altre pagine comuni
        elif self.path in ['/home', '/main', '/app']:
            self.send_response(302)
            self.send_header('Location', '/static/index.html')
            self.end_headers()
            return
        
        # Serve normalmente gli altri file
        else:
            # Imposta la directory corretta per i file statici
            if not hasattr(self, 'static_dir'):
                self.static_dir = os.path.join(os.getcwd(), 'static')
            
            # Cambia temporaneamente la directory di lavoro
            original_cwd = os.getcwd()
            try:
                os.chdir(self.static_dir)
                super().do_GET()
            finally:
                os.chdir(original_cwd)
    
    def log_message(self, format, *args):
        """Sovrascrive il logging per renderlo più pulito"""
        sys.stderr.write("🌐 %s - [%s] %s\n" % (
            self.address_string(),
            self.log_date_time_string(),
            format % args
        ))

def run_server(port=8080):
    """Avvia il server frontend"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    
    print(f"🚀 Server frontend avviato su http://localhost:{port}")
    print(f"📋 Reindirizzamento automatico da / a /static/index.html")
    print(f"📁 Servendo file dalla directory: {os.path.join(os.getcwd(), 'static')}")
    print(f"🌐 Accesso diretto: http://localhost:{port}/static/index.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server frontend fermato")
    except Exception as e:
        print(f"❌ Errore nel server frontend: {e}")

if __name__ == '__main__':
    # Ottieni la porta dai parametri o usa 8080 come default
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Porta non valida. Utilizzo porta 8080")
    
    run_server(port)