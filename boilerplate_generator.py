import os
import subprocess
from pathlib import Path
import sys
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
import os

# Initialize Rich console
console = Console()

def refine_input_with_openai(prompt_text, user_input):
    """Use OpenAI to refine the user's input."""
    # Simulate refinement with OpenAI (replace this with actual API call)
    refined_input = f"[Refined] {user_input.strip()}"
    return refined_input

def get_and_refine_input(prompt_text, default_value):
    """Prompt the user for input with a default value and refine it using OpenAI."""
    user_input = Prompt.ask(prompt_text, default=default_value)
    
    console.print("\n[bold yellow]Refining your input...[/bold yellow]")
    refined_input = refine_input_with_openai(prompt_text, user_input)
    console.print(f"\nSuggested refinement: [green]{refined_input}[/green]")
    
    confirmation = Prompt.ask("Do you want to use this refinement?", choices=["yes", "no"], default="yes")
    return refined_input if confirmation == "yes" else user_input


from utils.helper import Project

class FolderInfo:
    def __init__(self, name, parent=None):
        self.script_dir = Path(__file__).resolve().parent
        self.root_dir = self.script_dir.parent


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
        raise RuntimeError(f"Command failed: {description}")
    print(f"Success: {description} completed.\n")


def prompt_project_details():
    """Prompt the user for project planning details with default answers."""
    console.print(Panel("[bold cyan]Enter project details for planning[/bold cyan]\nPress Enter to accept default values."))

    # Default values
    default_root_path = Path(os.getcwd())  # Default to current working directory
    default_name = "My Project"
    default_goals = "Create a scalable and efficient project solution."
    default_architecture = "Microservices architecture with containerized deployments."
    default_nfr = "High scalability, performance, and security standards."

    # Collect inputs
    root_path = Prompt.ask("Project root path", default=str(default_root_path))
    root_path = Path(root_path).resolve()  # Ensure the path is absolute and normalized
    project_name = get_and_refine_input("Project name", default_name)
    project_goals = get_and_refine_input("Project goals", default_goals)
    architecture = get_and_refine_input("High-level architecture description", default_architecture)
    non_functional_requirements = get_and_refine_input(
        "Non-functional requirements (scalability, performance, etc.)", default_nfr
    )

    # Summary
    planning_content = f"""
# Project Planning

- **Root Path**: {root_path}
- **Name**: {project_name}
- **Goals**: {project_goals}
- **Architecture**: {architecture}
- **Non-functional Requirements**: {non_functional_requirements}
    """
    console.print("\n[bold magenta]Project Details Summary:[/bold magenta]")
    console.print(Panel(planning_content, title="Project Plan", subtitle="Review Details"))

    confirm = Prompt.ask("Do you want to proceed with this setup?", choices=["yes", "no"], default="yes")
    if confirm != "yes":
        console.print("[red]Setup aborted.[/red]")
        exit(0)

    console.print("[bold green]Setup confirmed. Proceeding...[/bold green]")
    return root_path, project_name, planning_content



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


def create_path(*args):
    path = Path()
    for arg in args:
        if isinstance(arg, str):
            path = path / arg
        elif isinstance(arg, Path):
            path = path / arg
        else:
            raise ValueError("Invalid argument type. Must be a string or Path object.")
    return path

def setup_python_backend(project_name):
    """Set up the Python backend with Django and PostgreSQL."""
    # Create a Path object for the root project directory
    root_path = create_path(project_name)
    root_path.mkdir(parents=True, exist_ok=True)  # Create if it doesn't exist

    # Create the backend directory
    backend_path = root_path / "backend"
    backend_path.mkdir(parents=True, exist_ok=True)

    # Now you can reliably use `root_path` and `backend_path` as Path objects
    # For example:
    # (backend_path / "some_file.txt").write_text("Hello, backend!")

    # Generate project-specific details
    db_name = Project.generate_random_project_name()
    db_user = Project.generate_db_username()
    db_password = Project.generate_random_password()

    staging_host = f"{project_name}-{db_name}.stage.internal" 

    # Change directory to backend_path to simplify commands
    os.makedirs(backend_path, exist_ok=True)
    os.chdir(backend_path)

    run_command("pipenv install django", "Install Django")
    run_command("pipenv run django-admin startproject app .", "Create Django project named app")
    run_command("pipenv install pylint mypy pytest pytest-cov alembic",
                "Install Django, dev tools, migration tool and database URL utility")
    run_command("pipenv install psycopg2-binary dj-database-url", "Install PostgreSQL adapter")
    run_command("pipenv lock > Pipfile.lock && pipenv requirements > requirements.txt",
                "Generate requirements.txt",
                )
    run_command("pipenv lock > constraints.txt", "Generate constraints.txt",)
    run_command("echo '[tool.black]\nline-length = 79' > pyproject.toml",
        "Configure Black code formatter",
    )

    # Define environment variables
    env_file_content = f"""DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY={Project.generate_random_password()}
DATABASE_URL=postgres://{db_user}:{db_password}@db:5432/{db_name}
"""
    with open(".env", "w") as f:
        f.write(env_file_content)

    with open(".env.staging", "w") as f:
        f.write(f"DEBUG=False\nALLOWED_HOSTS={staging_host}\nDATABASE_URL=postgres://{db_user}:{db_password}@db:5432/{db_name}")

    with open(".env.production", "w") as f:
        f.write(f"DEBUG=False\nALLOWED_HOSTS=domain.com\nDATABASE_URL=postgres://{db_user}:{db_password}@db:5432/{db_name}")

    # Update Django settings for PostgreSQL
    settings_path = create_path(backend_path, "app", "settings.py")
    with open(settings_path, "r") as f:
        settings = f.read()
    
    database_config = """
import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}
"""
    settings = settings.replace(
        "DATABASES = {",
        database_config
    )
    with open(settings_path, "w") as f:
        f.write(settings)

    # Initialize Alembic for migrations
    run_command(
        f"cd {backend_path} && alembic init migrations", "Initialize Alembic migrations"
    )

    # Output database credentials for reference
    print(f"Database Credentials for {project_name}:")
    print(f"  Database Name: {db_name}")
    print(f"  Username: {db_user}")
    print(f"  Password: {db_password}\n")
    print(f"  Staging Host: {staging_host}\n")

    # Suggest adding to /etc/hosts
    print("Add the following line to your /etc/hosts file for testing:")
    print(f"127.0.0.1    {staging_host}\n")


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
