# Python REST API Mock Server

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/your-username/python-rest-api-mock-server/Python%20application)

## 📝 Project Description

A lightweight, enterprise-ready REST API mock server built with Python's `http.server` module. This project allows developers to quickly set up mock APIs for testing and development purposes, reducing dependencies on backend services during frontend or integration testing phases. It supports various HTTP methods, custom status codes, headers, and response bodies, along with configurable response delays.

## ✨ Features

*   **Simple & Lightweight**: Built purely on Python's standard library, no external dependencies (except for testing).
*   **Customizable Mocks**: Define your API endpoints, HTTP methods, status codes, headers, and response bodies.
*   **Response Delays**: Simulate network latency with configurable delays for each mock response.
*   **Multi-threading**: Handles multiple concurrent requests efficiently using `socketserver.ThreadingHTTPServer`.
*   **Bilingual Documentation**: Comprehensive documentation available in both English and German.
*   **Enterprise-Ready**: Includes CI/CD pipeline, unit tests, and contribution guidelines for collaborative development.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/python-rest-api-mock-server.git
    cd python-rest-api-mock-server
    ```

2.  **(Optional) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies (for testing and development):**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To start the mock server with the default mock definitions:

```bash
python main.py
```

The server will start on `http://127.0.0.1:8000/` by default. You can then make requests to the defined mock endpoints:

*   `GET http://127.0.0.1:8000/api/v1/users`
*   `POST http://127.0.0.1:8000/api/v1/users`
*   `GET http://127.0.0.1:8000/api/v1/products/1`
*   `GET http://127.0.0.1:8000/health`

To stop the server, press `Ctrl+C`.

#### Customizing Mocks

You can modify the `DEFAULT_MOCKS` dictionary in `main.py` or pass a custom dictionary to the `MockServer` constructor:

```python
# main.py (example modification)

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

## 🧪 Running Tests

To run the unit tests:

```bash
python -m unittest test_main.py
```

## 🤝 Contributing

We welcome contributions to the Python REST API Mock Server! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

If you have any questions or suggestions, please open an issue in the GitHub repository.