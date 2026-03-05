# Architektur des Python REST API Mock Servers

## 1. Überblick

Der Python REST API Mock Server ist als leichtgewichtiges, aber robustes Werkzeug zum Mocken von RESTful APIs konzipiert. Er nutzt das Standard-Modul `http.server` von Python, insbesondere `http.server.BaseHTTPRequestHandler` und `socketserver.ThreadingHTTPServer`, um einen Multi-Thread-HTTP-Server bereitzustellen, der gleichzeitige Anfragen verarbeiten kann. Die Kernidee besteht darin, Mock-Antworten (Statuscodes, Header, Bodies und Verzögerungen) für bestimmte API-Pfade und HTTP-Methoden zu definieren, die der Server dann bei Empfang passender Anfragen ausliefert.

## 2. Kernkomponenten

Die Architektur besteht aus zwei primären Klassen:

### 2.1. `MockAPIHandler`

*   **Typ**: Erbt von `http.server.BaseHTTPRequestHandler`.
*   **Zweck**: Diese Klasse ist für die Verarbeitung einzelner HTTP-Anfragen zuständig. Für jede eingehende Anfrage wird vom `HTTPServer` eine Instanz von `MockAPIHandler` erstellt.
*   **Hauptaufgaben**:
    *   **Anfrage-Parsing**: `BaseHTTPRequestHandler` übernimmt das anfängliche Parsen der Anfragezeile (Methode, Pfad, HTTP-Version) und der Header.
    *   **Methodenbehandlung**: Es implementiert die Methoden `do_GET`, `do_POST`, `do_PUT`, `do_DELETE`, `do_HEAD` und `do_OPTIONS`. Jede `do_METHOD`-Methode ruft eine zentrale `_send_mock_response`-Dienstfunktion auf.
    *   **Mock-Dispatching**: Die Methode `_send_mock_response` sucht den angefragten `path` und die `method` in einem gemeinsamen `mock_definitions`-Dictionary (einer statischen Klassenvariable).
    *   **Antwortgenerierung**: Wenn ein passender Mock gefunden wird:
        *   Wird eine konfigurierbare `delay` mittels `time.sleep()` angewendet.
        *   Wird der HTTP-`status`-Code gesetzt (z.B. 200, 201, 404).
        *   Werden benutzerdefinierte HTTP-`headers` gesetzt.
        *   Wird der `body`-Inhalt in den Antwortstrom (`self.wfile`) geschrieben.
    *   **Fehlerbehandlung**: Wenn für einen bestimmten Pfad und eine Methode kein passender Mock gefunden wird, wird standardmäßig eine `404 Not Found`-Antwort gesendet.
    *   **CORS-Unterstützung**: Die `do_OPTIONS`-Methode enthält grundlegende CORS-Preflight-Header, um Cross-Origin-Anfragen von Webanwendungen zu ermöglichen.

### 2.2. `MockServer`

*   **Typ**: Eine Wrapper-Klasse, die den `socketserver.ThreadingHTTPServer` kapselt.
*   **Zweck**: Diese Klasse verwaltet den Lebenszyklus des HTTP-Servers (Starten, Stoppen) und bietet die Schnittstelle zur Konfiguration von Mock-Definitionen.
*   **Hauptaufgaben**:
    *   **Initialisierung**: Nimmt `host`, `port` und ein optionales `mocks`-Dictionary während der Instanziierung entgegen. Es setzt die statische Variable `MockAPIHandler.mock_definitions`, um sicherzustellen, dass alle Handler-Instanzen dieselben Mock-Daten teilen.
    *   **Servererstellung**: Instanziiert `socketserver.ThreadingHTTPServer`, eine Multi-Thread-Version von `http.server.HTTPServer`. Dies ermöglicht dem Server, mehrere Client-Verbindungen gleichzeitig zu verarbeiten, wobei jede Anfrage in einem eigenen Thread bearbeitet wird.
    *   **Serversteuerung**: Bietet die Methoden `start()` und `stop()`:
        *   `start()`: Ruft `self.server.serve_forever()` auf, um den Server unbegrenzt laufen zu lassen und auf Anfragen zu warten. Enthält eine `KeyboardInterrupt`-Behandlung für das saubere Herunterfahren.
        *   `stop()`: Ruft `self.server.shutdown()` und `self.server.server_close()` zur externen Steuerung der Serverbeendigung auf.

## 3. Datenfluss und Interaktion

1.  **Serverinitialisierung**: Eine `MockServer`-Instanz wird erstellt, wobei ein Dictionary von `mock_definitions` übergeben wird (oder `DEFAULT_MOCKS` verwendet wird). Dieses Dictionary wird dann `MockAPIHandler.mock_definitions` zugewiesen.
2.  **Serverstart**: `MockServer.start()` wird aufgerufen, wodurch der `ThreadingHTTPServer` auf dem angegebenen Host und Port zu lauschen beginnt.
3.  **Client-Anfrage**: Ein Client sendet eine HTTP-Anfrage (z.B. `GET /api/v1/users`) an den Server.
4.  **Anfragebearbeitung**: Der `ThreadingHTTPServer` empfängt die Anfrage und startet einen neuen Thread. In diesem Thread wird eine Instanz von `MockAPIHandler` erstellt.
5.  **Methoden-Dispatching**: Die entsprechende `do_METHOD`-Methode (z.B. `do_GET`) der `MockAPIHandler`-Instanz wird aufgerufen.
6.  **Mock-Suche**: Die `do_METHOD` ruft `_send_mock_response` auf, die `self.path` und die Anfragemethode verwendet, um eine entsprechende Antwort in `MockAPIHandler.mock_definitions` nachzuschlagen.
7.  **Antwortgenerierung**: Wenn eine Übereinstimmung gefunden wird, wendet der Handler eine angegebene `delay` an, setzt den `status`-Code und die `headers` und schreibt den `body` an den Client.
8.  **Keine Übereinstimmung**: Wenn keine Übereinstimmung gefunden wird, wird eine `404 Not Found`-Antwort gesendet.

```mermaid
graph TD
    A[Client] -->|HTTP-Anfrage| B(MockServer-Instanz)
    B --> C{socketserver.ThreadingHTTPServer}
    C -->|Startet Thread für jede Anfrage| D(MockAPIHandler-Instanz)
    D -->|Ruft do_GET/POST/... auf| E{_send_mock_response(path, method)}
    E --> F{Suche in MockAPIHandler.mock_definitions}
    F --"Übereinstimmung gefunden (path, method)"--> G[Verzögerung anwenden]
    G --> H[Status, Header, Body setzen]
    H --> I[HTTP-Antwort senden]
    F --"Keine Übereinstimmung"--> J[404 Not Found senden]
    I --> A
    J --> A
```

## 4. Struktur der Mock-Definition

Das `mock_definitions`-Dictionary ist zentral für das Verhalten des Servers. Es ist wie folgt strukturiert:

```json
{
    "/api/v1/users": {                 // API-Pfad (Schlüssel)
        "GET": {                        // HTTP-Methode (Schlüssel)
            "status": 200,              // HTTP-Statuscode
            "headers": {"Content-Type": "application/json"}, // Antwort-Header
            "body": "[...]",            // Antwort-Body (String-Darstellung)
            "delay": 0.1                // Optionale Verzögerung in Sekunden
        },
        "POST": {
            "status": 201,
            "headers": {"Content-Type": "application/json"},
            "body": "{"id": 3, "name": "Charlie", "message": "User created"}",
            "delay": 0.2
        }
    },
    "/health": {
        "GET": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "{"status": "UP"}",
            "delay": 0
        }
    }
}
```

## 5. Zukünftige Erweiterungen

*   **Konfigurationsdateiladen**: Implementierung des Ladens von Mock-Definitionen aus externen Dateien (JSON, YAML) zur einfacheren Verwaltung ohne Codeänderungen.
*   **Dynamisches Pfad-Matching**: Unterstützung für Pfadparameter (z.B. `/api/v1/users/{id}`).
*   **Anfragekörper-Matching**: Ermöglicht die Definition von Mocks basierend auf dem Inhalt des Anfragekörpers.
*   **Protokollierung**: Verbesserte Protokollierungsfunktionen für eingehende Anfragen und gesendete Antworten.
*   **Web-UI**: Eine einfache Weboberfläche zur Verwaltung und Anzeige aktiver Mocks.
*   **Middleware/Plugins**: Unterstützung für benutzerdefinierte Middleware zur dynamischen Änderung von Anfragen/Antworten.