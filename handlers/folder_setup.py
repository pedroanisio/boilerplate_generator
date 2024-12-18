from .base_handler import BaseHandler
from pathlib import Path
from rich.panel import Panel
import re

class FolderSetupHandler(BaseHandler):
    def __init__(self, console):
        super().__init__()
        self.console = console

    def process(self, context, *args, **kwargs):
        """
        Process the creation of the project structure.
        """
        self.console.print(Panel("[bold cyan]Setting up the project structure...[/bold cyan]"))

        # Ensure required context values are present
        required_keys = ["project_name", "planning_content", "project_root"]
        missing_keys = [key for key in required_keys if key not in context]
        if missing_keys:
            raise ValueError(f"Missing required context keys: {', '.join(missing_keys)}")

        # Convert project_name to snake_case
        project_name = re.sub(r'(?<!^)(?=[A-Z])', '_', context["project_name"]).lower()

        # Convert project_root to a Path object
        project_root = Path(context["project_root"])

        # Use planning_content
        planning_content = context["planning_content"]

        # Create the project root directory
        project_dir = project_root / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Add project_dir to context
        context["project_dir"] = project_dir

        # Create the project structure
        try:
            self.create_project_structure(project_dir, planning_content)
            self.console.print("[bold green]Project structure created successfully![/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]Error creating project structure:[/bold red] {e}")
            raise

        # Pass to the next handler
        return None

    def create_project_structure(self, project_dir, planning_content):
        """
        Create the basic project directory structure.
        """
        self.console.print(f"Creating project structure at: [bold magenta]{project_dir}[/bold magenta]...")

        # Define subdirectories
        subdirectories = [
            "backend",
            "frontend",
            "infrastructure",
            "tests",
            "docs",
        ]
        
        # Create directories
        for subdirectory in subdirectories:
            dir_path = project_dir / subdirectory
            dir_path.mkdir(parents=True, exist_ok=True)

        # Create a planning document in the docs directory
        docs_path = project_dir / "docs" / "planning.md"
        with open(docs_path, "w") as f:
            f.write(planning_content)

        self.console.print(f"Project structure created. Documentation saved at [bold green]{docs_path}[/bold green].")
