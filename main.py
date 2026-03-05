import http.server
import socketserver
import json
import time
from typing import Dict, Any, Optional

# Standard-Antworten für den Mock-Server
DEFAULT_MOCKS: Dict[str, Any] = {
    "/api/v1/users": {
        "GET": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]),
            "delay": 0.1
        },
        "POST": {
            "status": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"id": 3, "name": "Charlie", "message": "User created"}),
            "delay": 0.2
        }
    },
    "/api/v1/products/1": {
        "GET": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"id": 1, "name": "Laptop", "price": 1200.00}),
            "delay": 0.05
        }
    },
    "/health": {
        "GET": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "UP", "service": "MockServer"}),
            "delay": 0
        }
    }
}

class MockAPIHandler(http.server.BaseHTTPRequestHandler):
    """
    Ein benutzerdefinierter HTTP-Anfrage-Handler für den Mock-Server.
    Dieser Handler verarbeitet eingehende HTTP-Anfragen und liefert vordefinierte Mock-Antworten.
    """
    # Statische Variable, die die Mock-Definitionen für alle Handler-Instanzen speichert.
    mock_definitions: Dict[str, Any] = {}

    def _set_headers(self, status_code: int, headers: Dict[str, str]) -> None:
        """
        Setzt die HTTP-Antwort-Header und den Statuscode.
        :param status_code: Der HTTP-Statuscode, z.B. 200, 404.
        :param headers: Ein Dictionary von Headern, die gesendet werden sollen.
        """
        self.send_response(status_code) # Sendet den HTTP-Statuscode.
        for key, value in headers.items():
            self.send_header(key, value) # Sendet jeden Header einzeln.
        self.end_headers() # Beendet den Header-Block.

    def _send_mock_response(self, path: str, method: str) -> None:
        """
        Sucht nach einer passenden Mock-Antwort und sendet diese.
        Verzögert die Antwort, falls eine `delay`-Angabe vorhanden ist.
        :param path: Der angefragte URL-Pfad.
        :param method: Die HTTP-Methode (GET, POST, etc.).
        """
        # Überprüft, ob der Pfad in den Mock-Definitionen vorhanden ist.
        if path in self.mock_definitions:
            path_mocks = self.mock_definitions[path]
            # Überprüft, ob die HTTP-Methode für diesen Pfad definiert ist.
            if method in path_mocks:
                mock_response = path_mocks[method]
                delay = mock_response.get("delay", 0) # Holt die Verzögerung oder verwendet 0 als Standard.
                if delay > 0:
                    time.sleep(delay) # Führt eine Verzögerung aus.

                status = mock_response.get("status", 200) # Holt den Status oder verwendet 200 als Standard.
                headers = mock_response.get("headers", {"Content-Type": "text/plain"}) # Holt Header oder Standard.
                body = mock_response.get("body", "") # Holt den Body oder einen leeren String.

                self._set_headers(status, headers) # Setzt die Header und den Status.
                self.wfile.write(body.encode('utf-8')) # Schreibt den Body in die Antwort.
                return

        # Wenn kein passender Mock gefunden wurde, sende 404 Not Found.
        self._set_headers(404, {"Content-Type": "text/plain"})
        self.wfile.write(f"No mock response found for {method} {path}\n".encode('utf-8'))

    def do_GET(self) -> None:
        """
        Behandelt HTTP GET-Anfragen.
        """
        self._send_mock_response(self.path, "GET")

    def do_POST(self) -> None:
        """
        Behandelt HTTP POST-Anfragen.
        """
        self._send_mock_response(self.path, "POST")

    def do_PUT(self) -> None:
        """
        Behandelt HTTP PUT-Anfragen.
        """
        self._send_mock_response(self.path, "PUT")

    def do_DELETE(self) -> None:
        """
        Behandelt HTTP DELETE-Anfragen.
        """
        self._send_mock_response(self.path, "DELETE")

    def do_HEAD(self) -> None:
        """
        Behandelt HTTP HEAD-Anfragen.
        (Kann optional implementiert werden, um nur Header zu senden).
        """
        self._send_mock_response(self.path, "HEAD") # Nutzt die gleiche Logik, sendet aber keinen Body.

    def do_OPTIONS(self) -> None:
        """
        Behandelt HTTP OPTIONS-Anfragen.
        Nützlich für CORS-Preflight-Anfragen.
        """
        self._set_headers(200, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "86400"
        })
        self.wfile.write(b"")


class MockServer:
    """
    Ein einfacher HTTP Mock-Server, der vordefinierte Antworten auf Anfragen liefert.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 8000, mocks: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialisiert den MockServer.
        :param host: Der Host, an den der Server gebunden werden soll (Standard: 127.0.0.1).
        :param port: Der Port, auf dem der Server lauschen soll (Standard: 8000).
        :param mocks: Ein Dictionary von Mock-Definitionen. Wenn None, werden DEFAULT_MOCKS verwendet.
        """
        self.host = host # Speichert den Hostnamen.
        self.port = port # Speichert den Port.
        MockAPIHandler.mock_definitions = mocks if mocks is not None else DEFAULT_MOCKS # Setzt die globalen Mocks.
        # Erstellt einen Threading-HTTP-Server, der Anfragen in separaten Threads verarbeitet.
        self.server = socketserver.ThreadingHTTPServer((self.host, self.port), MockAPIHandler)
        print(f"[MockServer] Server wird gestartet auf http://{self.host}:{self.port}/") # Info-Ausgabe.

    def start(self) -> None:
        """
        Startet den Mock-Server und lässt ihn auf eingehende Anfragen warten.
        """
        try:
            self.server.serve_forever() # Der Server läuft unendlich, bis er unterbrochen wird.
        except KeyboardInterrupt:
            print("\n[MockServer] Server wird heruntergefahren...") # Meldung bei Unterbrechung.
            self.server.shutdown() # Fährt den Server sauber herunter.
            self.server.server_close() # Schließt die Server-Sockets.
            print("[MockServer] Server wurde erfolgreich heruntergefahren.") # Bestätigung.

    def stop(self) -> None:
        """
        Stoppt den Mock-Server.
        """
        print("[MockServer] Server wird extern gestoppt...") # Info-Ausgabe.
        self.server.shutdown() # Fährt den Server sauber herunter.
        self.server.server_close() # Schließt die Server-Sockets.

if __name__ == "__main__":
    # Beispiel für die Verwendung des Mock-Servers.
    # Hier können benutzerdefinierte Mocks übergeben werden, falls gewünscht.
    # mock_definitions = {
    #     "/custom/hello": {
    #         "GET": {
    #             "status": 200,
    #             "headers": {"Content-Type": "text/plain"},
    #             "body": "Hello from custom mock!",
    #             "delay": 0.5
    #         }
    #     }
    # }
    # server = MockServer(port=8080, mocks=mock_definitions)

    server = MockServer(port=8000) # Erstellt eine Instanz des Mock-Servers auf Port 8000.
    server.start() # Startet den Server.