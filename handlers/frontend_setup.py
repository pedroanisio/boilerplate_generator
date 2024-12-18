from .base_handler import BaseHandler
from jinja2 import Template
from pathlib import Path
from rich.panel import Panel
from utils.helpers import run_command


class FrontendSetupHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Set up the Node.js frontend with Create React App, ESLint, and Prettier.
        """
        self.console.print(Panel("[bold cyan]Setting up Node.js frontend...[/bold cyan]"))

        # Ensure project name and directory are in the context
        if "project_name" not in context or "project_dir" not in context:
            self.console.print("[bold red]Error:[/bold red] Missing 'project_name' or 'project_dir' in context.")
            return "Error: Missing 'project_name' or 'project_dir' in context."

        project_name = context["project_name"]
        project_dir = context["project_dir"]

        try:
            self.setup_node_frontend(project_name, project_dir, context)
            self.console.print(f"[bold green]Node.js frontend setup completed for {project_name}![/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]Error during Node.js frontend setup:[/bold red] {e}")
            raise

        # Pass to the next handler
        return None

    def setup_node_frontend(self, project_name, project_dir, context):
        """
        Core logic for setting up the Node.js frontend.
        """
        frontend_path = Path(project_dir) / "frontend"

        # Create React App with TypeScript template
        run_command(
            f"npx create-react-app {frontend_path} --template typescript",
            "Initialize React app with TypeScript",
            cwd=frontend_path.parent,
        )

        # Install ESLint, Prettier, and related plugins
        run_command(
            "npm install eslint prettier eslint-config-prettier eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y --save-dev --legacy-peer-deps",
            "Install ESLint, Prettier, and plugins",
            cwd=frontend_path,
        )

        # Render and write ESLint configuration
        eslint_config = self._render_template("eslint_config.j2", context)
        self._write_file(frontend_path / ".eslintrc.json", eslint_config)

        # Render and write Prettier configuration
        prettier_config = self._render_template("prettier_config.j2", context)
        self._write_file(frontend_path / ".prettierrc", prettier_config)

    def _render_template(self, template_name, context):
        """
        Render a Jinja2 template with the given context.
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            return template.render(context)

    @staticmethod
    def _write_file(file_path, content):
        """
        Utility to write content to a file.
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(file_path, "w") as f:
            f.write(content)
