## path : project_setup/handlers/env_check.py
from .base_handler import BaseHandler
import subprocess
import sys
from rich.panel import Panel

class EnvCheckHandler(BaseHandler):
    def __init__(self, console):
        super().__init__()
        self.console = console

    def process(self, context, *args, **kwargs):
        required_tools = ["git", "pipenv", "yarn", "docker"]
        self.console.print(Panel("🔍 [bold cyan]Checking required tools...[/bold cyan]"))
        
        for tool in required_tools:
            if not self.check_tool(tool):
                self.console.print(f"[bold red]Error:[/bold red] {tool} is not installed. Please install it and try again.")
                sys.exit(1)
        
        self.console.print("[bold green]✅ All required tools are installed![/bold green]")
        return None  # Indicate successful processing

    def check_tool(self, tool):
        result = subprocess.run(f"which {tool}", shell=True, stdout=subprocess.PIPE, text=True)
        if result.returncode != 0:
            self.console.print(f"[bold red]❌ {tool} is not installed.[/bold red]")
            return False
        self.console.print(f"[bold green]✔ {tool} is installed.[/bold green]")
        return True
