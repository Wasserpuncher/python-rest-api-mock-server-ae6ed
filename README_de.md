# Python REST API Mock Server

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/your-username/python-rest-api-mock-server/Python%20application)

## 📝 Projektbeschreibung

Ein leichter, unternehmensfähiger REST API Mock-Server, der mit dem Python-Modul `http.server` erstellt wurde. Dieses Projekt ermöglicht es Entwicklern, schnell Mock-APIs für Test- und Entwicklungszwecke einzurichten, wodurch Abhängigkeiten von Backend-Diensten während Frontend- oder Integrationstestphasen reduziert werden. Es unterstützt verschiedene HTTP-Methoden, benutzerdefinierte Statuscodes, Header und Antwortkörper sowie konfigurierbare Antwortverzögerungen.

## ✨ Funktionen

*   **Einfach & Leichtgewichtig**: Rein mit der Python-Standardbibliothek erstellt, keine externen Abhängigkeiten (außer für Tests).
*   **Anpassbare Mocks**: Definieren Sie Ihre API-Endpunkte, HTTP-Methoden, Statuscodes, Header und Antwortkörper.
*   **Antwortverzögerungen**: Simulieren Sie Netzwerklatenz mit konfigurierbaren Verzögerungen für jede Mock-Antwort.
*   **Multi-threading**: Verarbeitet mehrere gleichzeitige Anfragen effizient mit `socketserver.ThreadingHTTPServer`.
*   **Zweisprachige Dokumentation**: Umfassende Dokumentation in Englisch und Deutsch verfügbar.
*   **Unternehmensfähig**: Enthält CI/CD-Pipeline, Unit-Tests und Richtlinien für die Zusammenarbeit.

## 🚀 Erste Schritte

### Voraussetzungen

*   Python 3.8+

### Installation

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/your-username/python-rest-api-mock-server.git
    cd python-rest-api-mock-server
    ```

2.  **(Optional) Virtuelle Umgebung erstellen und aktivieren:**
    ```bash
    python -m venv venv
    # Unter Windows
    .\venv\Scripts\activate
    # Unter macOS/Linux
    source venv/bin/activate
    ```

3.  **Abhängigkeiten installieren (für Tests und Entwicklung):**
    ```bash
    pip install -r requirements.txt
    ```

### Verwendung

Um den Mock-Server mit den Standard-Mock-Definitionen zu starten:

```bash
python main.py
```

Der Server startet standardmäßig auf `http://127.0.0.1:8000/`. Sie können dann Anfragen an die definierten Mock-Endpunkte stellen:

*   `GET http://127.0.0.1:8000/api/v1/users`
*   `POST http://127.0.0.1:8000/api/v1/users`
*   `GET http://127.0.0.1:8000/api/v1/products/1`
*   `GET http://127.0.0.1:8000/health`

Um den Server zu stoppen, drücken Sie `Strg+C`.

#### Mocks anpassen

Sie können das `DEFAULT_MOCKS`-Dictionary in `main.py` ändern oder ein benutzerdefiniertes Dictionary an den `MockServer`-Konstruktor übergeben:

```python
# main.py (Beispieländerung)

my_custom_mocks = {
    "/my-service/data": {
        "GET": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"id": 123, "value": "Custom Data"}',
            "delay": 0.3
        },
        "POST": {
            "status": 201,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": "Data created"}',
            "delay": 0.1
        }
    }
}

if __name__ == "__main__":
    server = MockServer(port=8080, mocks=my_custom_mocks)
    server.start()
```

## 🧪 Tests ausführen

Um die Unit-Tests auszuführen:

```bash
python -m unittest test_main.py
```

## 🤝 Mitwirken

Wir freuen uns über Beiträge zum Python REST API Mock Server! Bitte beachten Sie die Datei [CONTRIBUTING.md](CONTRIBUTING.md) für Richtlinien zur Mitwirkung.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – weitere Details finden Sie in der Datei [LICENSE](LICENSE).

## 📞 Kontakt

Bei Fragen oder Vorschlägen öffnen Sie bitte ein Issue im GitHub-Repository.