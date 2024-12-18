from pathlib import Path
from rich.panel import Panel
from jinja2 import Template
from .base_handler import BaseHandler
from utils.commands import run_command


class GitInitializationHandler(BaseHandler):
    def __init__(self, console, template_dir="handlers/templates"):
        super().__init__()
        self.console = console
        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory '{self.template_dir}' does not exist.")

    def process(self, context, *args, **kwargs):
        """
        Initialize a Git repository for the project.
        """
        self.console.print(Panel("[bold cyan]Initializing Git repository...[/bold cyan]"))

        # Ensure the project name is in the context
        if "project_name" not in context or "project_dir" not in context:
            self.console.print("[bold red]Error:[/bold red] Missing 'project_name' or 'project_dir' in context.")
            return "Error: Missing 'project_name' or 'project_dir' in context."

        project_dir = context["project_dir"]
        project_name = context["project_name"]

        # Initialize Git
        try:
            self.initialize_git(project_name, project_dir)
            self.console.print(f"[bold green]Git repository initialized successfully for {project_name}![/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]Error initializing Git repository:[/bold red] {e}")
            raise

        # Pass to the next handler
        return None

    def initialize_git(self, project_name, project_dir):
        """
        Initialize a Git repository with a README, .gitignore (from template), and initial commit.
        """
        project_path = Path(project_dir)

        # Run commands using the `utils.run_command` function
        run_command("git init", "Initialize Git repository", cwd=project_path)
        run_command(
            f"echo '# {project_name}' > README.md", 
            "Create README.md", 
            cwd=project_path
        )
        
        # Render and write the .gitignore template
        gitignore_content = self._render_template("gitignore.j2", {"project_name": project_name})
        self._write_file(project_path / ".gitignore", gitignore_content)

        run_command(
            "git add . && git commit -m 'Initial commit'", 
            "Perform initial Git commit", 
            cwd=project_path
        )
        run_command("git checkout -b develop", "Create 'develop' branch", cwd=project_path)
        run_command("git tag v0.1.0", "Create initial version tag", cwd=project_path)

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
