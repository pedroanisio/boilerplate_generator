import logging
from pathlib import Path
from jinja2 import Template
from .base_handler import BaseHandler
from rich.panel import Panel


class ObservabilitySetupHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Add observability configurations for the project.
        """
        self.console.print(Panel("[bold cyan]Setting up observability tools...[/bold cyan]"))
        logging.info("Starting observability setup...")

        # Ensure required context values
        if "project_name" not in context:
            error_message = "Missing required context key: 'project_name'"
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
            logging.error(error_message)
            return error_message

        try:
            self.setup_observability(context)
            project_name = context["project_name"]
            self.console.print(f"[bold green]Observability setup completed for {project_name}![/bold green]")
            logging.info("Observability setup completed successfully.")
        except Exception as e:
            self.console.print(f"[bold red]Error during observability setup:[/bold red] {e}")
            logging.error(f"Error during observability setup: {e}", exc_info=True)
            raise

        # Pass to the next handler
        return None

    def setup_observability(self,context):
        """
        Core logic for setting up observability using Jinja2 templates.
        """
        project_dir = context["project_dir"]
        observability_path = Path(project_dir) / "infrastructure" / "observability"
        observability_path.mkdir(parents=True, exist_ok=True)

        # Render the Prometheus configuration template
        prometheus_config = self._render_template(
            "prometheus.yml.j2",
            {"backend_target": "backend:8000"}
        )

        # Write the rendered Prometheus configuration
        self._write_file(observability_path / "prometheus.yml", prometheus_config)

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
