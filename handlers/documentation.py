from .base_handler import BaseHandler
from jinja2 import Template
from pathlib import Path
from rich.panel import Panel
import logging


class DocumentationSetupHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Add documentation templates for the project.
        """

        self.console.print(Panel("[bold cyan]Setting up documentation templates...[/bold cyan]"))
        logging.info("Starting documentation setup...")

        # Ensure required context values
        if "project_name" not in context:
            error_message = "Missing required context key: 'project_name'"
            self.console.print(f"[bold red]Error:[/bold red] {error_message}")
            logging.error(error_message)
            return error_message

        try:
            self.setup_documentation(context)
            project_name = context["project_name"]
            self.console.print(f"[bold green]Documentation templates added for {project_name}![/bold green]")
            logging.info("Documentation setup completed successfully.")
        except Exception as e:
            self.console.print(f"[bold red]Error during documentation setup:[/bold red] {e}")
            logging.error(f"Error during documentation setup: {e}", exc_info=True)
            raise

        # Pass to the next handler
        return None

    def setup_documentation(self, context):        
        """
        Core logic for setting up documentation using Jinja2 templates.
        """
        project_name = context["project_name"]
        project_dir = context["project_dir"]

        docs_path = Path(project_dir) / "docs"
        docs_path.mkdir(parents=True, exist_ok=True)

        # Render and write templates for documentation
        self._render_and_write_template("CONTRIBUTING.md.j2", docs_path / "CONTRIBUTING.md", {})
        self._render_and_write_template("API_DOCS.md.j2", docs_path / "API_DOCS.md", {})
        self._render_and_write_template("architecture.md.j2", docs_path / "architecture.md", {})

    def _render_and_write_template(self, template_name, output_path, context):
        """
        Render a Jinja2 template and write it to a file.
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            content = template.render(context)

        self._write_file(output_path, content)

    @staticmethod
    def _write_file(path, content):
        """
        Utility to write content to a file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(path, "w") as f:
            f.write(content)
