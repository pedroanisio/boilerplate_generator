from .base_handler import BaseHandler
from jinja2 import Template
from pathlib import Path
from rich.panel import Panel
import logging


class CiCdSetupHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Set up GitHub Actions for CI/CD.
        """
        self.console.print(Panel("[bold cyan]Setting up CI/CD pipeline with GitHub Actions...[/bold cyan]"))
        logging.info("Starting CI/CD setup...")

        # Ensure required context values
        required_keys = ["project_name", "python_version", "node_version"]
        missing_keys = [key for key in required_keys if key not in context]
        if missing_keys:
            error_message = f"Missing required context keys: {', '.join(missing_keys)}"
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
            logging.error(error_message)
            return error_message

        project_name = context["project_name"]

        try:
            self.setup_ci_cd(project_name, context)
            self.console.print(f"[bold green]CI/CD pipeline configured for {project_name}![/bold green]")
            logging.info("CI/CD setup completed successfully.")
        except Exception as e:
            self.console.print(f"[bold red]Error during CI/CD setup:[/bold red] {e}")
            logging.error(f"Error during CI/CD setup: {e}", exc_info=True)
            raise

        # Pass to the next handler
        return None

    def setup_ci_cd(self, project_name, context):
        """
        Core logic for setting up GitHub Actions CI/CD using Jinja2 templates.
        """
        project_dir = context["project_dir"]
        github_actions_path = Path(project_dir) / ".github" / "workflows"
        github_actions_path.mkdir(parents=True, exist_ok=True)

        # Render the CI/CD pipeline template
        ci_cd_yaml = self._render_template("ci_cd_pipeline.yml.j2", context)

        # Write the rendered template to the GitHub Actions workflows directory
        self._write_file(github_actions_path / "ci_cd_pipeline.yml", ci_cd_yaml)

    def _render_template(self, template_name, context):
        """
        Render a Jinja2 template with the provided context.
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            return template.render(context)

    @staticmethod
    def _write_file(path, content):
        """
        Utility to write content to a file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(path, "w") as f:
            f.write(content)
