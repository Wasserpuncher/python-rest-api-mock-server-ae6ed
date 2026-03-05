# Contributing to Python REST API Mock Server

We welcome contributions to the Python REST API Mock Server project! By participating in this project, you agree to abide by our code of conduct. Please read this document carefully to understand how you can contribute.

## Table of Contents

1.  [Code of Conduct](#1-code-of-conduct)
2.  [How to Contribute](#2-how-to-contribute)
    *   [Reporting Bugs](#reporting-bugs)
    *   [Suggesting Enhancements](#suggesting-enhancements)
    *   [Submitting Pull Requests](#submitting-pull-requests)
3.  [Development Setup](#3-development-setup)
4.  [Coding Guidelines](#4-coding-guidelines)
5.  [License](#5-license)

## 1. Code of Conduct

We are committed to providing a welcoming and inclusive environment for everyone. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) (if applicable, otherwise state: "We don't have a separate Code of Conduct file yet, but we expect all contributors to be respectful and professional.") before contributing.

## 2. How to Contribute

### Reporting Bugs

If you find a bug, please help us by submitting an issue to our [GitHub Issues](https://github.com/your-username/python-rest-api-mock-server/issues).

When reporting a bug, please include:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Actual behavior.
*   Screenshots or error messages if applicable.
*   Your operating system and Python version.

### Suggesting Enhancements

We love to hear your ideas for improving the project! You can suggest enhancements by opening an issue on our [GitHub Issues](https://github.com/your-username/python-rest-api-mock-server/issues).

When suggesting an enhancement, please include:

*   A clear and concise description of the proposed feature.
*   Why this feature would be useful.
*   Any potential alternatives or considerations.

### Submitting Pull Requests

1.  **Fork the repository**: Click the "Fork" button at the top right of the repository page.
2.  **Clone your fork**: `git clone https://github.com/YOUR_USERNAME/python-rest-api-mock-server.git`
3.  **Create a new branch**: `git checkout -b feature/your-feature-name` or `bugfix/your-bugfix-name`
4.  **Make your changes**: Implement your feature or fix the bug.
    *   Ensure your code adheres to the [Coding Guidelines](#4-coding-guidelines).
    *   Write or update unit tests for your changes.
    *   Update documentation if necessary (both English and German `README` and `docs/architecture` files).
5.  **Run tests**: Make sure all existing tests pass and your new tests also pass.
    `python -m unittest test_main.py`
6.  **Commit your changes**: `git commit -m "feat: Add a new feature"` (use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) if possible).
7.  **Push to your fork**: `git push origin feature/your-feature-name`
8.  **Open a Pull Request**: Go to the original repository on GitHub and click the "New pull request" button. Provide a clear title and description for your changes.

## 3. Development Setup

After cloning the repository, you can set up your development environment:

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate # macOS/Linux
    .\venv\Scripts\activate   # Windows
    ```
2.  **Install development dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Coding Guidelines

*   **Python Version**: Code should be compatible with Python 3.8+.
*   **Style Guide**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style. We use `flake8` for linting.
*   **Type Hinting**: Use [type hints](https://docs.python.org/3/library/typing.html) for all function arguments and return values.
*   **Docstrings**: All public classes, methods, and functions should have [PEP 257](https://www.python.org/dev/peps/pep-0257/) compliant docstrings (in English).
*   **Inline Comments**: Use inline comments sparingly to explain complex logic, and ensure they are in **German** to aid beginners (as per project requirements).
*   **Variable Names**: Use clear, descriptive English variable and function names.
*   **Testing**: All new features and bug fixes should be accompanied by appropriate unit tests.

## 5. License

By contributing to this project, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.