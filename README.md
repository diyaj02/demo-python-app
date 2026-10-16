# DevOps Capstone Project — Python Flask Application

## Project Overview

This project demonstrates an end-to-end DevOps workflow using a Python Flask web application. It covers source code management, containerization, continuous integration, Docker image publishing, Kubernetes deployments, and application testing.

The application provides a container information dashboard, a persistent visit counter, and a Notes REST API supporting CRUD operations.

**GitHub Repository:** https://github.com/diyaj02/demo-python-app

**Docker Hub Repository:** https://hub.docker.com/r/diyaa02/demo-python-app

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Application programming language |
| Flask | REST API and web application |
| PostgreSQL 16 | Persistent database |
| Redis 7 | Caching |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Git and GitHub | Version control and pull requests |
| CircleCI | Continuous integration and image publishing |
| Docker Hub | Container image registry |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| pytest | Unit and integration testing |
| Ruff | Python linting |
| Gitleaks | Secret scanning |

## Project Architecture

```text
GitHub Repository
       |
       v
CircleCI Pipeline
       |
       +-- Secret Scanning
       +-- Ruff Linting
       +-- Unit Tests
       +-- Integration Tests
       |
       v
Docker Build and Push
       |
       v
Docker Hub
       |
       v
Kubernetes (Minikube)
       |
       +-- QA Namespace
       +-- Staging Namespace
       +-- Production Namespace
              |
              +-- Flask Application
              +-- PostgreSQL
              +-- Redis
```

## 1. Git Branching Strategy

Three protected branches are used:

- `main` — Quality Assurance (QA)
- `staging` — Pre-production environment
- `prod` — Production environment

Changes are developed in feature branches and promoted using GitHub pull requests.

**Promotion workflow:**

```text
feature/* → main → staging → prod
```

Branch protection prevents direct pushes to protected branches and requires changes to go through pull requests.

Promotion pull requests use merge commits to preserve Git history.

## 2. Application Features

### Container Information Dashboard

The homepage displays:

- Container hostname or ID
- Python version
- Application startup time
- Persistent visit counter

### Notes REST API

The Notes API supports Create, Read, Update, and Delete operations.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application dashboard |
| GET | `/health` | Application health and visit information |
| GET | `/api/info` | Application information |
| POST | `/api/notes` | Create a note |
| GET | `/api/notes` | List all notes |
| PUT | `/api/notes/{id}` | Update a note |
| DELETE | `/api/notes/{id}` | Delete a note |

Notes are stored in PostgreSQL. Redis caches visit-count data temporarily.

## 3. Docker Containerization

The application uses a Dockerfile based on `python:3.12-slim`.

The image:

- Installs Python dependencies
- Copies application source code
- Uses a non-root application user
- Exposes port 8080
- Starts the Flask application

A `.dockerignore` file excludes unnecessary files from the Docker build context.

### Build the Image

```bash
docker build -t demo-python-app:local .
```

### Run the Container

```bash
docker run --rm -p 8081:8080 demo-python-app:local
```

Note: The standalone container requires a reachable PostgreSQL database for the database-backed endpoints. For a complete working environment, use Docker Compose.

## 4. Docker Compose

Docker Compose manages three services:

1. **Flask** — Web application and REST API
2. **PostgreSQL** — Persistent application data
3. **Redis** — Temporary cache

PostgreSQL uses a named volume to preserve database records across container restarts.

Health checks verify database and cache readiness before the application starts.

Database initialization is performed automatically using `init_db.py`.

### Local Setup

Create a `.env` file:

```dotenv
POSTGRES_PASSWORD=your_local_database_password
```

Keep this file private and do not commit it.

Start the application:

```bash
docker compose up -d --build
```

Visit:

http://localhost:8081

Stop the containers:

```bash
docker compose down
```

Do not add `-v` when you want to preserve PostgreSQL data.

## 5. Unit Testing

Unit tests use pytest to verify API behavior and input validation.

Tests include:

- Application information endpoint
- Missing note title
- Empty note title
- Invalid note content
- Invalid note update request

Run the unit tests:

```bash
python -m pytest tests/test_main.py -v
```

## 6. Integration Testing

Integration tests verify the application against real PostgreSQL and Redis services.

They include:

- PostgreSQL connection verification
- Note creation
- Note retrieval
- Note updates
- Note deletion
- Redis connectivity and key storage

Run integration tests using Docker Compose:

```bash
docker compose run --rm tests
```

The test runner installs development dependencies and runs pytest inside the Compose network.

## 7. CircleCI Pipeline

CircleCI automates code quality checks, testing, Docker image builds, and image publishing.

The configuration is stored in:

```text
.circleci/config.yml
```

### QA Pipeline — `main`

Runs the following jobs:

1. Secret scanning using Gitleaks
2. Ruff linting
3. pytest unit tests
4. PostgreSQL and Redis integration tests
5. Docker image build and push

### Staging Pipeline — `staging`

Builds and publishes the staging Docker image.

### Production Pipeline — `prod`

Builds and publishes the production Docker image.

Docker Hub credentials are configured securely using CircleCI environment variables:

```text
DOCKERHUB_USER
DOCKERHUB_TOKEN
```

## 8. Docker Hub Image Tags

The pipeline publishes moving and commit-specific tags.

| Environment | Moving tag | Example commit-specific tag |
|---|---|---|
| QA | `qa` | `qa-1ca47c8` |
| Staging | `stage` | `stage-be05fbb` |
| Production | `prod` | `prod-5562032` |

Example image:

```text
diyaa02/demo-python-app:qa
```

Commit-specific tags provide traceability from published images to source code commits.

## 9. Kubernetes Deployment

The application is deployed to a local Minikube Kubernetes cluster.

Three namespaces separate environments:

```text
qa
stage
prod
```

Each namespace contains:

- Flask application Deployment and Service
- PostgreSQL Deployment and Service
- Redis Deployment and Service
- PostgreSQL persistent volume claim
- Kubernetes Secrets

### Kubernetes Manifest Files

```text
k8s/deployment.yaml
k8s/stage.yaml
k8s/prod.yaml
```

### Check Namespaces

```bash
kubectl get namespaces
```

### Check Running Pods

```bash
kubectl get pods -A
```

### Check Deployments

```bash
kubectl get deployments -n qa
kubectl get deployments -n stage
kubectl get deployments -n prod
```

### Access the QA Application

```bash
kubectl port-forward -n qa service/demo-app 8082:8080
```

Open:

http://localhost:8082

### Kubernetes Rollout

Restart the QA application:

```bash
kubectl rollout restart deployment/demo-app -n qa
```

Verify rollout completion:

```bash
kubectl rollout status deployment/demo-app -n qa --timeout=180s
```

A successful rollout confirms that Kubernetes recreated the application Pods and restored the desired healthy state.

## 10. Security Practices

The project incorporates several security controls:

- Protected GitHub branches
- Pull-request-based change promotion
- Automated secret scanning
- Non-root Docker container execution
- Docker Hub access tokens
- CircleCI environment variables
- Kubernetes Secrets
- Docker image pull credentials
- `.gitignore` and `.dockerignore` exclusions

Database passwords and registry tokens must never be committed to GitHub.

## 11. Project Verification

The following functionality was tested during development:

- GitHub branch protection rejected direct pushes
- Feature changes were promoted through pull requests
- Docker image built and ran successfully
- PostgreSQL stored persistent visit records
- Redis stored cached visit counts
- Notes CRUD operations worked
- Five API validation unit tests passed
- Two integration tests passed
- CircleCI QA, staging, and production pipelines succeeded
- Docker Hub images were published with environment-specific tags
- Kubernetes successfully deployed nine application Pods across three namespaces
- QA Kubernetes rollout completed successfully
- Git branch file consistency was verified

## 12. Project Outcome

The DevOps Capstone project demonstrates a complete application delivery workflow from source code to containerized deployment.

It integrates automated testing, secure credential management, database persistence, caching, Docker image publication, and Kubernetes orchestration.

The project demonstrates how a single Python application can be developed, tested, promoted, and deployed consistently across QA, staging, and production environments.

---

**Project:** DevOps Capstone — Python Flask Application

**GitHub:** https://github.com/diyaj02/demo-python-app

**Docker Hub:** https://hub.docker.com/r/diyaa02/demo-python-app
