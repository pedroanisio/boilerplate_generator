import os
import subprocess
from pathlib import Path
import sys

def check_dependency(tool):
    """Check if a required tool is installed."""
    result = subprocess.run(f"which {tool}", shell=True, stdout=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {tool} is not installed or not in PATH. Please install it and try again.")
        sys.exit(1)
    else:
        print(f"Success: {tool} is installed and executable.")


def check_environment():
    """Ensure all required tools are installed."""
    print("Checking required tools...")
    required_tools = ["git", "pipenv", "yarn", "docker"]
    for tool in required_tools:
        check_dependency(tool)
    print("All required tools are installed.\n")

def run_command(command, description):
    """Run a shell command and print status."""
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error: {description} failed.")
        exit(result.returncode)
    print(f"Success: {description} completed.\n")


def prompt_project_details():
    """Prompt the user for project planning details."""
    print("Enter project details for planning:")
    project_name = input("Project name: ").strip()
    project_goals = input("Project goals: ").strip()
    architecture = input("High-level architecture description: ").strip()
    non_functional_requirements = input(
        "Non-functional requirements (scalability, performance, etc.): "
    ).strip()

    planning_content = f"""
# Project Planning

- **Name**: {project_name}
- **Goals**: {project_goals}
- **Architecture**: {architecture}
- **Non-functional Requirements**: {non_functional_requirements}
    """
    print("\nProject Details Summary:")
    print(planning_content)

    confirm = input("Do you want to proceed with this setup? (yes/no): ").lower()
    if confirm != "yes":
        print("Setup aborted.")
        exit(0)

    return project_name, planning_content


def create_project_structure(project_name, planning_content):
    """Create the basic project directory structure."""
    print(f"Creating project structure for {project_name}...")
    directories = [
        f"{project_name}/backend",
        f"{project_name}/frontend",
        f"{project_name}/infrastructure",
        f"{project_name}/tests",
        f"{project_name}/docs",
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    with open(f"{project_name}/docs/planning.md", "w") as f:
        f.write(planning_content)

    print(f"Project structure created.\n")


def initialize_git(project_name):
    """Initialize a Git repository."""
    run_command(f"cd {project_name} && git init", "Initialize Git repository")
    run_command(
        f"cd {project_name} && echo '# {project_name}' > README.md",
        "Create README.md",
    )
    run_command(
        f"cd {project_name} && echo '__pycache__/\n.env\n*.log\n' > .gitignore",
        "Create .gitignore",
    )
    run_command(
        f"cd {project_name} && git add . && git commit -m 'Initial commit'",
        "Perform initial Git commit",
    )
    run_command(f"cd {project_name} && git checkout -b develop", "Create 'develop' branch")
    run_command(f"cd {project_name} && git tag v0.1.0", "Create initial version tag")


def setup_python_backend(project_name):
    """Set up the Python backend with Django."""
    backend_path = f"{project_name}/backend"
    run_command(f"cd {backend_path} && pipenv install django", "Install Django")
    run_command(
        f"cd {backend_path} && django-admin startproject app .", "Create Django project"
    )
    run_command(
        f"cd {backend_path} && pipenv install pylint mypy pytest pytest-cov alembic",
        "Install dev tools and migration tool",
    )
    run_command(
        f"cd {backend_path} && pipenv lock > Pipfile.lock && pipenv requirements > requirements.txt",
        "Generate requirements.txt",
    )
    run_command(
        f"cd {backend_path} && pipenv lock > constraints.txt",
        "Generate constraints.txt",
    )
    run_command(
        f"cd {backend_path} && echo '[tool.black]\nline-length = 79' > pyproject.toml",
        "Configure Black code formatter",
    )
    env_file_content = """DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=your-secret-key
"""
    with open(f"{backend_path}/.env", "w") as f:
        f.write(env_file_content)
    with open(f"{backend_path}/.env.staging", "w") as f:
        f.write("DEBUG=False\nALLOWED_HOSTS=staging.domain.com")
    with open(f"{backend_path}/.env.production", "w") as f:
        f.write("DEBUG=False\nALLOWED_HOSTS=domain.com")
    run_command(
        f"cd {backend_path} && alembic init migrations", "Initialize Alembic migrations"
    )


def setup_node_frontend(project_name):
    """Set up the Node.js frontend with Create React App, ESLint, and Prettier."""
    frontend_path = f"{project_name}/frontend"
    
    # Create React App with TypeScript template
    run_command(
        f"npx create-react-app {frontend_path} --template typescript",
        "Initialize React app with TypeScript",
    )
    
    # Navigate to the frontend directory
    run_command(
        f"cd {frontend_path}",
        "Navigate to frontend directory",
    )
    
    # Install ESLint, Prettier, and related plugins with --legacy-peer-deps
    run_command(
        f"cd {frontend_path} && npm install eslint prettier eslint-config-prettier eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y --save-dev --legacy-peer-deps",
        "Install ESLint, Prettier, and plugins",
    )
    
    # Set up ESLint configuration
    eslint_config = '''{
  "extends": [
    "react-app",
    "plugin:react/recommended",
    "plugin:jsx-a11y/recommended",
    "prettier"
  ],
  "plugins": ["react", "jsx-a11y"],
  "rules": {
    // Add custom rules here
  }
}'''
    with open(f"{frontend_path}/.eslintrc.json", "w") as f:
        f.write(eslint_config)
    
    # Set up Prettier configuration
    prettier_config = '''{
  "semi": true,
  "singleQuote": true,
  "printWidth": 80,
  "trailingComma": "es5"
}'''
    with open(f"{frontend_path}/.prettierrc", "w") as f:
        f.write(prettier_config)


def configure_docker(project_name):
    """Create Dockerfiles and Docker Compose."""
    backend_dockerfile = f"""FROM python:3.13.1-slim
WORKDIR /app
COPY backend /app
RUN pip install pipenv && pipenv install --system --deploy
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
"""
    frontend_dockerfile = """FROM node:22.12.0-slim
WORKDIR /app
COPY frontend /app
RUN yarn install
CMD ["yarn", "start"]
"""
    docker_compose = f"""
version: "3.8"
services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
      - ALLOWED_HOSTS=localhost
      - SECRET_KEY=your-secret-key
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
"""

    with open(f"{project_name}/backend/Dockerfile", "w") as f:
        f.write(backend_dockerfile)

    with open(f"{project_name}/frontend/Dockerfile", "w") as f:
        f.write(frontend_dockerfile)

    with open(f"{project_name}/docker-compose.yml", "w") as f:
        f.write(docker_compose)

    print("Dockerfiles and Docker Compose configuration created.\n")


def setup_ci_cd(project_name):
    """Set up GitHub Actions for CI/CD."""
    github_actions_path = f"{project_name}/.github/workflows"
    Path(github_actions_path).mkdir(parents=True, exist_ok=True)
    ci_cd_yaml = f"""
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          cd backend
          pip install pipenv
          pipenv install --system --deploy

      - name: Run tests
        run: |
          cd backend
          pytest --cov=.

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "22"

      - name: Install frontend dependencies
        run: |
          cd frontend
          yarn install

      - name: Lint frontend code
        run: |
          cd frontend
          yarn lint

      - name: Build Docker images
        run: |
          docker build -t backend:latest backend
          docker build -t frontend:latest frontend
"""
    with open(f"{github_actions_path}/ci_cd_pipeline.yml", "w") as f:
        f.write(ci_cd_yaml)
    print("GitHub Actions CI/CD pipeline configured.\n")


def setup_observability(project_name):
    """Add observability configurations."""
    observability_path = f"{project_name}/infrastructure/observability"
    Path(observability_path).mkdir(parents=True, exist_ok=True)
    with open(f"{observability_path}/prometheus.yml", "w") as f:
        f.write(
            """
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['backend:8000']
"""
        )
    print("Observability tools placeholders added.\n")


def setup_documentation(project_name):
    """Add documentation templates."""
    docs_path = f"{project_name}/docs"
    with open(f"{docs_path}/CONTRIBUTING.md", "w") as f:
        f.write("# Contributing Guidelines\n")
    with open(f"{docs_path}/API_DOCS.md", "w") as f:
        f.write("# API Documentation\n")
    with open(f"{docs_path}/architecture.md", "w") as f:
        f.write("# Architecture Overview\n")
    print("Documentation templates added.\n")


def main():
    check_environment()
    project_name, planning_content = prompt_project_details()
    create_project_structure(project_name, planning_content)
    initialize_git(project_name)
    setup_python_backend(project_name)
    setup_node_frontend(project_name)
    configure_docker(project_name)
    setup_ci_cd(project_name)
    setup_observability(project_name)
    setup_documentation(project_name)
    print(f"\nBoilerplate project {project_name} initialized successfully!")


if __name__ == "__main__":
    main()
