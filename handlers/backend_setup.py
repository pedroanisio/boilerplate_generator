from .base_handler import BaseHandler
from jinja2 import Template
from pathlib import Path
from rich.panel import Panel
from utils.helpers import Project, run_command
import logging
import os


class BackendSetupHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Set up the Python backend with Django and PostgreSQL.
        """

        # Generate project-specific details
        prj = Project()
        context['db_name'] = prj.generate_random_project_name()
        context['db_user'] = prj.generate_db_username()
        context['db_password'] = prj.generate_random_password()
        context['secret_key'] = prj.generate_random_password(64)

        self.console.print(Panel("[bold cyan]Setting up Python backend...[/bold cyan]"))
        logging.info("Starting Python backend setup...")

        # Ensure required context values
        required_keys = ["project_name", "project_dir", "db_name", "db_user", 
                         "db_password", "secret_key", "allowed_hosts"]
        missing_keys = [key for key in required_keys if key not in context]
        if missing_keys:
            error_message = f"Missing required context keys: {', '.join(missing_keys)}"
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
            logging.error(error_message)
            return error_message

        project_name = context["project_name"]
        project_dir = context["project_dir"]

        try:
            # Execute backend setup logic
            self.setup_python_backend(project_name, project_dir, context)
            self.console.print(f"[bold green]Python backend setup completed for {project_name}![/bold green]")
            logging.info("Python backend setup completed successfully.")
        except Exception as e:
            self.console.print(f"[bold red]Error during Python backend setup:[/bold red] {e}")
            logging.error(f"Error during Python backend setup: {e}", exc_info=True)
            raise

        # Pass to the next handler
        return None

    def setup_python_backend(self, project_name, project_dir, context):
        """
        Core logic for setting up the Python backend with Django and PostgreSQL.
        """
        root_path = Path(project_dir)
        backend_path = root_path / "backend"
        backend_path.mkdir(parents=True, exist_ok=True)

        # Install Django and create the backend structure
        run_command("pipenv install django", "Install Django", cwd=backend_path)
        run_command("pipenv run django-admin startproject app .", "Create Django project named app", cwd=backend_path)
        run_command(
            "pipenv install pylint mypy pytest pytest-cov alembic",
            "Install dev tools and migration utility",
            cwd=backend_path,
        )
        run_command("pipenv install psycopg2-binary dj-database-url", "Install PostgreSQL adapter", cwd=backend_path)
        run_command("pipenv lock > Pipfile.lock && pipenv requirements > requirements.txt", "Generate requirements.txt", cwd=backend_path)
        run_command("pipenv lock > constraints.txt", "Generate constraints.txt", cwd=backend_path)
        run_command("echo '[tool.black]\nline-length = 79' > pyproject.toml", "Configure Black code formatter", cwd=backend_path)

        # Render templates for .env files and Django settings
        self._render_and_write_template("env.j2", backend_path / ".env", {
            "debug": True,
            "allowed_hosts": context["allowed_hosts"],
            "secret_key": context["secret_key"],
            "db_url": f"postgres://{context['db_user']}:{context['db_password']}@db:5432/{context['db_name']}",
        })
        self._render_and_write_template("env.j2", backend_path / ".env.staging", {
            "debug": False,
            "allowed_hosts": f"{context['db_name']}.stage.internal",
            "secret_key": context["secret_key"],
            "db_url": f"postgres://{context['db_user']}:{context['db_password']}@db:5432/{context['db_name']}",
        })
        self._render_and_write_template("env.j2", backend_path / ".env.production", {
            "debug": False,
            "allowed_hosts": "domain.com",
            "secret_key": context["secret_key"],
            "db_url": f"postgres://{context['db_user']}:{context['db_password']}@db:5432/{context['db_name']}",
        })
        self._render_and_write_template("settings.py.j2", backend_path / "app" / "settings.py", context, append=True)

        # Initialize Alembic for migrations
        run_command("alembic init migrations", "Initialize Alembic migrations", cwd=backend_path)

        # Output database credentials for reference
        self.console.print(f"[bold magenta]Database Credentials for {project_name}:[/bold magenta]")
        self.console.print(f"  Database Name: {context['db_name']}")
        self.console.print(f"  Username: {context['db_user']}")
        self.console.print(f"  Password: {context['db_password']}")
        self.console.print("\n[bold yellow]Add the following line to your /etc/hosts file for testing:[/bold yellow]")
        self.console.print(f"127.0.0.1    {context['project_name'].lower()}-{context['db_name']}.stage.internal")

    def _render_and_write_template(self, template_name, output_path, context, append=False):
        """
        Render a Jinja2 template and either append to or overwrite the target file.
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        # Render the template
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            rendered_content = template.render(context)

        # Append or overwrite based on the `append` flag
        if append:
            self._append_to_file(output_path, rendered_content)
        else:
            self._write_file(output_path, rendered_content)

    def _append_to_file(self, path, content):
        """
        Utility to append content to a file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        mode = "a" if path.exists() else "w"  # Append if file exists, otherwise write
        with open(path, mode) as f:
            f.write("\n" + content + "\n")  # Append with a newline for separation

    def _write_file(self, path, content):
        """
        Utility to overwrite content in a file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(path, "w") as f:
            f.write(content)


    @staticmethod
    def _write_file(path, content):
        """
        Utility to write content to a file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(path, "w") as f:
            f.write(content)
