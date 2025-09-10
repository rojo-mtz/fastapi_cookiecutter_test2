# FastAPI Template Microservice

🚀 **Template microservice with FastAPI and Google Cloud integration**

A production-ready FastAPI template featuring authentication, Google Cloud services integration, containerization, and comprehensive development tooling.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Development Setup](#-development-setup)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Google Cloud Integration](#-google-cloud-integration)
- [Testing](#-testing)
- [Development Tools](#-development-tools)
- [Contributing](#-contributing)

## ✨ Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Google Cloud Integration**: BigQuery, Secret Manager, and App Engine support
- **Authentication**: API key-based authentication with exceptions for GCP services
- **Containerization**: Multi-stage Docker builds for development, testing, and production
- **Development Tools**: Pre-commit hooks, code formatting, linting, and type checking
- **Health Checks**: Built-in health check endpoints
- **Poetry**: Dependency management and packaging
- **Testing**: Comprehensive test suite with pytest and factory-boy

## 📋 Requirements

- **Python**: 3.11+ (recommended 3.12)
- **Poetry**: [Installation guide](https://python-poetry.org/docs/)
- **Docker**: For containerized deployment
- **Google Cloud Service Account**: With appropriate permissions
- **Pre-commit**: [Installation guide](https://pre-commit.com/#install)

## 🚀 Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd fastapi_cookiecutter

# Create virtual environment with pyenv (recommended)
pyenv install 3.12
pyenv virtualenv 3.12 template_microservice
pyenv shell template_microservice

# Install Poetry and dependencies
pip install poetry
poetry install
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
LOCAL_API_KEY=your_secure_api_key_here
GOOGLE_CLOUD_PROJECT=your-project-id
BIGQUERY_DATASET=your_dataset
BIGQUERY_LOCATION=US
```

### 3. Google Cloud Setup

Place your Google Cloud service account key as `key.json` in the project root:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

**Required permissions:**
- BigQuery Data Editor
- Secret Manager Admin
- Cloud Run Invoker (if using Cloud Run)

### 4. Run the Application

```bash
# Development server
poetry run uvicorn src.main:app --reload

# Or using Docker Compose
docker-compose up --build
```

## 📁 Project Structure

```
fastapi_cookiecutter/
├── src/                          # Application source code
│   ├── api/                      # API layer
│   │   ├── endpoints/            # API endpoints
│   │   │   ├── health.py         # Health check endpoints
│   │   │   └── providers.py      # Provider authentication endpoints
│   │   └── urls.py               # URL routing configuration
│   ├── core/                     # Core application logic
│   │   ├── db.py                 # Database configuration
│   │   ├── models.py             # Database models
│   │   └── utils.py              # Utility functions
│   ├── schemas/                  # Pydantic schemas
│   │   ├── health.py             # Health check schemas
│   │   └── providers.py          # Provider schemas
│   └── tests/                    # Test suite
├── deployment/                   # Deployment configurations
│   ├── development/              # Development Docker setup
│   ├── production/               # Production Docker setup
│   ├── testing/                  # Testing Docker setup
│   └── build.sh                  # Build scripts
├── docker-compose.yml            # Docker Compose configuration
├── pyproject.toml               # Poetry configuration
└── README.md                    # This file
```

## 🛠 Development Setup

### Install Development Dependencies

```bash
poetry install --with dev
```

### Setup Pre-commit Hooks

```bash
pre-commit install
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOCAL_API_KEY` | API key for authentication | Required |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | `celestial-gecko-449316-d2` |
| `BIGQUERY_DATASET` | BigQuery dataset name | `template_dataset` |
| `BIGQUERY_LOCATION` | BigQuery location | `US` |

## 🐳 Deployment

### Docker Compose (Recommended for Development)

```bash
# Start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f
```

### Production Deployment

```bash
# Build production image
docker build -f deployment/production/Dockerfile -t template-microservice:latest .

# Run production container
docker run -p 9000:9000 \
  -e LOCAL_API_KEY=your_api_key \
  -v $(pwd)/key.json:/src/key.json:ro \
  template-microservice:latest
```

### Testing Environment

```bash
# Run tests in Docker
cd deployment/testing
./test.sh
```

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Available Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/api/v1/health` | Health check | None |
| `POST` | `/api/v1/generate_url` | Generate authentication URL | API Key |

## 🔐 Authentication

### API Key Authentication

Include the API key in the request header:

```bash
curl -X POST "http://localhost:8000/api/v1/generate_url" \
  -H "X-API-KEY: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 123, "provider": "google"}'
```

### Authentication Exceptions

The following requests bypass API key authentication:
- **Google Cloud Cron jobs**: Header `X-Appengine-Cron: true`
- **Google Cloud Tasks**: User-Agent starts with `Google-Cloud-Tasks`

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click the **Authorize** button (🔒)
3. Enter your API key in the `X-API-KEY` field
4. Click **Authorize**
5. Test protected endpoints

## ☁️ Google Cloud Integration

### BigQuery Configuration

- **Project**: `celestial-gecko-449316-d2`
- **Dataset**: `template_dataset`
- **Location**: `US`

### Secret Manager

The application uses Google Cloud Secret Manager to store and retrieve authentication URLs with automatic TTL management (7 days).

**Features:**
- Automatic secret creation with TTL
- URL expiration tracking
- Secure credential management

### Service Account Permissions

Ensure your service account has the following roles:
- `roles/bigquery.dataEditor`
- `roles/secretmanager.admin`
- `roles/run.invoker` (for Cloud Run deployment)

## 🧪 Testing

### Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest src/tests/test_clabe_service.py

# Run tests in Docker
docker-compose -f docker-compose.test.yml up --build
```

### Test Structure

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Factory Classes**: Test data generation using factory-boy

## 🛠 Development Tools

### Code Formatting

```bash
# Format code with Black
poetry run black src/

# Sort imports
poetry run isort src/
```

### Linting

```bash
# Lint with flake8
poetry run flake8 src/

# Type checking with mypy
poetry run mypy src/
```

### Pre-commit Hooks

Automatically run on commit:
- Code formatting (Black)
- Import sorting (isort)
- Linting (flake8)
- Type checking (mypy)

### Make Commands

```bash
# View available commands
make help

# Run development server
make dev

# Run tests
make test

# Build Docker image
make build

# Deploy to production
make deploy
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install pre-commit hooks**: `pre-commit install`
4. **Make your changes** and ensure tests pass
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use type hints for all functions
- Keep commits atomic and well-described

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- **Email**: oliver@monthly.la
- **Issues**: Create an issue in this repository
- **Documentation**: Check the `/docs` endpoint when running the application

---

**Built with ❤️ using FastAPI and Google Cloud Platform**
