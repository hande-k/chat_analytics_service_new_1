# Chat Analytics Service

This is the backend service for the Chat Analytics system, responsible for processing and serving chat data via an API.

## Getting Started

### Prerequisites
- Ensure you have [Poetry](https://python-poetry.org/) installed for dependency management.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/chat_analytics_service_public_1.git
    cd chat_analytics_service_public_1
    ```

2. Install dependencies:
    ```bash
    poetry install
    ```

3. Start the service:
    ```bash
    poetry run uvicorn src.app.main:app --port 5001
    ```

4. Access the service:
    ```
    http://127.0.0.1:5001/
    ```
