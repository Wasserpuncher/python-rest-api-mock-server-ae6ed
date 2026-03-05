# Architecture of the Python REST API Mock Server

## 1. Overview

The Python REST API Mock Server is designed to be a lightweight, yet robust, tool for mocking RESTful APIs. It leverages Python's standard `http.server` module, specifically `http.server.BaseHTTPRequestHandler` and `socketserver.ThreadingHTTPServer`, to provide a multi-threaded HTTP server capable of handling concurrent requests. The core idea is to define mock responses (status codes, headers, bodies, and delays) for specific API paths and HTTP methods, which the server then dispatches upon receiving matching requests.

## 2. Core Components

The architecture is composed of two primary classes:

### 2.1. `MockAPIHandler`

*   **Type**: Inherits from `http.server.BaseHTTPRequestHandler`.
*   **Purpose**: This class is responsible for processing individual HTTP requests. For each incoming request, an instance of `MockAPIHandler` is created by the `HTTPServer`.
*   **Key Responsibilities**:
    *   **Request Parsing**: `BaseHTTPRequestHandler` handles the initial parsing of the request line (method, path, HTTP version) and headers.
    *   **Method Handling**: It implements `do_GET`, `do_POST`, `do_PUT`, `do_DELETE`, `do_HEAD`, and `do_OPTIONS` methods. Each `do_METHOD` method calls a central `_send_mock_response` utility.
    *   **Mock Dispatching**: The `_send_mock_response` method looks up the requested `path` and `method` in a shared `mock_definitions` dictionary (a static class variable).
    *   **Response Generation**: If a matching mock is found:
        *   It applies a configurable `delay` using `time.sleep()`.
        *   Sets the HTTP `status` code (e.g., 200, 201, 404).
        *   Sets custom HTTP `headers`.
        *   Writes the `body` content to the response stream (`self.wfile`).
    *   **Error Handling**: If no matching mock is found for a given path and method, it defaults to a `404 Not Found` response.
    *   **CORS Support**: The `do_OPTIONS` method includes basic CORS preflight headers to allow cross-origin requests from web applications.

### 2.2. `MockServer`

*   **Type**: A wrapper class encapsulating the `socketserver.ThreadingHTTPServer`.
*   **Purpose**: This class manages the lifecycle of the HTTP server (starting, stopping) and provides the interface for configuring mock definitions.
*   **Key Responsibilities**:
    *   **Initialization**: Takes `host`, `port`, and an optional `mocks` dictionary during instantiation. It sets the `MockAPIHandler.mock_definitions` static variable, ensuring all handler instances share the same mock data.
    *   **Server Creation**: Instantiates `socketserver.ThreadingHTTPServer`, which is a multi-threaded version of `http.server.HTTPServer`. This allows the server to handle multiple client connections concurrently, with each request processed in its own thread.
    *   **Server Control**: Provides `start()` and `stop()` methods:
        *   `start()`: Calls `self.server.serve_forever()` to keep the server running indefinitely, listening for requests. It includes `KeyboardInterrupt` handling for graceful shutdown.
        *   `stop()`: Calls `self.server.shutdown()` and `self.server.server_close()` for external control over the server's termination.

## 3. Data Flow and Interaction

1.  **Server Initialization**: A `MockServer` instance is created, passing a dictionary of `mock_definitions` (or using `DEFAULT_MOCKS`). This dictionary is then assigned to `MockAPIHandler.mock_definitions`.
2.  **Server Start**: `MockServer.start()` is called, which starts the `ThreadingHTTPServer` listening on the specified host and port.
3.  **Client Request**: A client sends an HTTP request (e.g., `GET /api/v1/users`) to the server.
4.  **Request Handling**: The `ThreadingHTTPServer` receives the request and spawns a new thread. In this thread, it creates an instance of `MockAPIHandler`.
5.  **Method Dispatch**: The `MockAPIHandler` instance's appropriate `do_METHOD` method (e.g., `do_GET`) is invoked.
6.  **Mock Lookup**: The `do_METHOD` calls `_send_mock_response`, which uses `self.path` and the request method to look up a corresponding response in `MockAPIHandler.mock_definitions`.
7.  **Response Generation**: If a match is found, the handler applies any specified `delay`, sets the `status` code and `headers`, and writes the `body` to the client.
8.  **No Match**: If no match, a `404 Not Found` response is sent.

```mermaid
graph TD
    A[Client] -->|HTTP Request| B(MockServer Instance)
    B --> C{socketserver.ThreadingHTTPServer}
    C -->|Spawns Thread for each Request| D(MockAPIHandler Instance)
    D -->|Calls do_GET/POST/...| E{_send_mock_response(path, method)}
    E --> F{Lookup in MockAPIHandler.mock_definitions}
    F --"Match Found (path, method)"--> G[Apply Delay]
    G --> H[Set Status, Headers, Body]
    H --> I[Send HTTP Response]
    F --"No Match"--> J[Send 404 Not Found]
    I --> A
    J --> A
```

## 4. Mock Definition Structure

The `mock_definitions` dictionary is central to the server's behavior. It's structured as follows:

```json
{
    "/api/v1/users": {                 // API Path (key)
        "GET": {                        // HTTP Method (key)
            "status": 200,              // HTTP Status Code
            "headers": {"Content-Type": "application/json"}, // Response Headers
            "body": "[...]",            // Response Body (string representation)
            "delay": 0.1                // Optional delay in seconds
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

## 5. Future Enhancements

*   **Configuration File Loading**: Implement loading mock definitions from external files (JSON, YAML) for easier management without code changes.
*   **Dynamic Path Matching**: Support for path parameters (e.g., `/api/v1/users/{id}`).
*   **Request Body Matching**: Allow defining mocks based on the content of the request body.
*   **Logging**: Enhanced logging capabilities for incoming requests and dispatched responses.
*   **Web UI**: A simple web interface for managing and viewing active mocks.
*   **Middleware/Plugins**: Support for custom middleware to modify requests/responses dynamically.