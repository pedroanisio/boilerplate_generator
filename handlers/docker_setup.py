from .base_handler import BaseHandler
from jinja2 import Template
from pathlib import Path
from rich.panel import Panel
from rich.prompt import Prompt
import logging


class DockerConfigurationHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Configure Docker for the project by creating Dockerfiles and a Docker Compose file.
        """
        self.console.print(Panel("[bold cyan]Configuring Docker...[/bold cyan]"))
        logging.info("Starting Docker configuration...")

        # Ensure required context values and gather missing data
        required_keys = ["project_name", "project_dir", "python_image", "node_image"]
        optional_keys = ["secret_key", "allowed_hosts", "db_user", "db_password"]
        missing_keys = [key for key in required_keys if key not in context]

        if missing_keys:
            error_message = f"Missing required context keys: {', '.join(missing_keys)}"
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
            logging.error(error_message)
            return error_message

        # Prompt for missing optional values
        self._ensure_optional_context_values(context, optional_keys)

        try:
            self.configure_docker(context)
            self.console.print(f"[bold green]Docker configuration completed for {context['project_name']}![/bold green]")
            logging.info("Docker configuration completed successfully.")
        except Exception as e:
            self.console.print(f"[bold red]Error during Docker configuration:[/bold red] {e}")
            logging.error(f"Error during Docker configuration: {e}", exc_info=True)
            raise

        # Pass to the next handler
        return None

    def configure_docker(self, context):
        """
        Core logic to create Dockerfiles and a Docker Compose file using Jinja2 templates.
        """
        project_path = Path(context["project_dir"])

        # Load templates
        backend_template = self._load_template("backend.Dockerfile.j2")
        frontend_template = self._load_template("frontend.Dockerfile.j2")
        compose_template = self._load_template("docker-compose.yml.j2")

        # Render templates
        backend_dockerfile = backend_template.render(python_version=context["python_image"])
        frontend_dockerfile = frontend_template.render(node_version=context["node_image"])
        docker_compose = compose_template.render(
            project_name=context["project_name"],
            secret_key=context["secret_key"],
            allowed_hosts=context["allowed_hosts"],
            db_user=context["db_user"],
            db_password=context["db_password"],
        )

        # Write rendered files
        self._write_file(project_path / "backend" / "Dockerfile", backend_dockerfile)
        self._write_file(project_path / "frontend" / "Dockerfile", frontend_dockerfile)
        self._write_file(project_path / "docker-compose.yml", docker_compose)

    def _ensure_optional_context_values(self, context, optional_keys):
        """
        Prompt for missing optional context values and update the context.
        """
        prompts = {
            "secret_key": "Enter the secret key for the backend",
            "allowed_hosts": "Enter the allowed hosts (comma-separated)",
            "db_user": "Enter the PostgreSQL username",
            "db_password": "Enter the PostgreSQL password",
        }

        defaults = {
            "secret_key": "your-secret-key",
            "allowed_hosts": "localhost",
            "db_user": "postgres",
            "db_password": "postgres",
        }

        for key in optional_keys:
            if key not in context:
                context[key] = self._prompt_for_missing_value(prompts[key], defaults[key])

    def _load_template(self, template_name):
        """
        Load a Jinja2 template from the templates directory.
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        with open(template_path, "r") as f:
            return Template(f.read())

    @staticmethod
    def _write_file(file_path, content):
        """
        Utility to write content to a file.
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(file_path, "w") as f:
            f.write(content)

    def _prompt_for_missing_value(self, prompt_message, default=None):
        """
        Prompt the user to enter a missing value with an optional default.
        """
        return Prompt.ask(prompt_message, default=default)
