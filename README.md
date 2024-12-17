# Project Boilerplate Generator

This script automates the creation of a boilerplate project with backend and frontend components, including Git initialization, dependency setup, Docker configurations, CI/CD pipelines, and observability configurations.

## Features

- **Backend**: Python with Django, preconfigured with development tools like `pytest`, `mypy`, and `alembic`.
- **Frontend**: React app with TypeScript, ESLint, and Prettier.
- **Version Control**: Git initialization with `.gitignore`, branches, and initial tags.
- **Docker**: Prebuilt `Dockerfile` for backend and frontend, with a `docker-compose.yml` configuration.
- **CI/CD**: GitHub Actions pipeline for automated testing, linting, and Docker builds.
- **Observability**: Prometheus configuration for monitoring.
- **Documentation**: Templates for contributing, API documentation, and architecture overview.

## Requirements

Ensure the following tools are installed and accessible from your PATH:

- `git`
- `pipenv`
- `yarn`
- `docker`

Run the script in a Unix-like environment for compatibility.

## Installation and Usage

1. Clone the repository containing this script or save the file locally.
2. Ensure all dependencies are installed (see [Requirements](#requirements)).
3. Run the script:

    ```bash
    python boilerplate_generator.py
    ```

4. Follow the prompts to provide project details like name, goals, architecture, and non-functional requirements.
5. The script will generate a project directory with the following structure:

    ```
    <project_name>/
    ├── backend/
    │   ├── app/
    │   ├── migrations/
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── requirements.txt
    │   ├── .env
    │   └── constraints.txt
    ├── frontend/
    │   ├── src/
    │   ├── Dockerfile
    │   ├── .eslintrc.json
    │   └── .prettierrc
    ├── infrastructure/
    │   ├── observability/
    │   │   └── prometheus.yml
    ├── docs/
    │   ├── planning.md
    │   ├── CONTRIBUTING.md
    │   ├── API_DOCS.md
    │   └── architecture.md
    ├── .github/
    │   └── workflows/
    │       └── ci_cd_pipeline.yml
    └── docker-compose.yml
    ```

## Generated Configurations

### Backend

- Preconfigured with Django and essential development tools.
- Environment variable files for different stages (`.env`, `.env.staging`, `.env.production`).

### Frontend

- React app initialized with TypeScript template.
- Linting and formatting with ESLint and Prettier.

### Docker

- Backend and frontend `Dockerfile`s.
- `docker-compose.yml` for combined service orchestration.

### CI/CD

- GitHub Actions pipeline for code quality checks and Docker builds.

### Observability

- Prometheus configuration to monitor the Django backend.

### Documentation

- Templates for contributing, API documentation, and architecture details.

## Known Limitations

- Assumes a Unix-like environment for shell commands.
- Requires pre-installed dependencies (`git`, `pipenv`, `yarn`, and `docker`).

## License

This project is licensed under the MIT License. Feel free to use and modify as needed.
