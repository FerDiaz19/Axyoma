#!/usr/bin/env python
"""
Servidor de prueba simple para debug
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/superadmin/listar_empresas'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Datos de prueba
            response = {
                "empresas": [
                    {
                        "empresa_id": 1,
                        "nombre": "TechCorp Solutions",
                        "rfc": "TCS950815MX3",
                        "direccion": "Av. Tecnológico 1500",
                        "correo": "contacto@techcorp.mx",
                        "telefono": "4421234567",
                        "status": True,
                        "administrador": "OK",
                        "plantas_count": 2,
                        "empleados_count": 0,
                        "fecha_registro": None
                    },
                    {
                        "empresa_id": 2,
                        "nombre": "InnovaSoft Industries",
                        "rfc": "ISI980320QR1",
                        "direccion": "Blvd. Bernardo Quintana 2000",
                        "correo": "info@innovasoft.mx",
                        "telefono": "4427654321",
                        "status": True,
                        "administrador": "OK",
                        "plantas_count": 2,
                        "empleados_count": 0,
                        "fecha_registro": None
                    }
                ],
                "total": 2,
                "mensaje": "Datos de prueba"
            }
            
            self.wfile.write(json.dumps(response).encode())
            print(f"📤 Datos enviados: {response}")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), Handler)
    print("🚀 Servidor de prueba ejecutándose en http://localhost:8000")
    server.serve_forever()
