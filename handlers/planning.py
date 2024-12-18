## path : ./handlers/planning.py
from .base_handler import BaseHandler
from dotenv import load_dotenv
from llm.ai_manager import AIManager
from openai import OpenAI
from pathlib import Path
from rich.panel import Panel
from rich.prompt import Prompt
from utils.openai import OpenAIEngine
from utils.prompt_utils import PromptUtils
import logging
import os

# Load environment variables
load_dotenv()

# Define a simple Flavor class for demonstration
class Flavor:
    def __init__(self, model: str, system_message: str, user_message: str):
        self.model = model
        self.system_message = system_message
        self.user_message = user_message

class PlanningHandler(BaseHandler):
    def __init__(self, console):
        super().__init__()
        self.console = console
        self.project_root = self.get_project_root()

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Initialize the AI Manager
        self.ai_manager = AIManager(config_path="llm/config/config.json")


    def get_project_root(self):
        """Determine the project root dynamically."""
        # Locate the directory containing the current file and navigate to the root
        return Path(__file__).resolve().parent.parent

    def process(self, context, *args, **kwargs):
        """Execute the project planning process."""
        self.console.print(Panel("[bold cyan]Enter project details for planning[/bold cyan]\nPress Enter to accept default values."))

        # Prompt project details
        root_path, project_name, planning_content = self.prompt_project_details()

        # Display summary
        self.console.print("\n[bold magenta]Project Details Summary:[/bold magenta]")
        self.console.print(Panel(planning_content, title="Project Plan", subtitle="Review Details"))

        confirm = Prompt.ask("Do you want to proceed with this setup?", choices=["yes", "no"], default="yes")
        if confirm != "yes":
            self.console.print("[red]Setup aborted.[/red]")
            exit(0)

        self.console.print("[bold green]Setup confirmed. Proceeding...[/bold green]")

        context["project_root"] = root_path
        context["project_name"] = project_name
        context["planning_content"] = planning_content
        # Pass to the next handler
        return None  # Indicate successful processing        

    def prompt_project_details(self):
        """Prompt the user for project details."""
        default_root_path = Path().resolve()  # Default to current working directory
        default_name = "My Project"
        default_goals = "Create a scalable and efficient project solution."
        default_architecture = "Microservices architecture with containerized deployments."
        default_nfr = "High scalability, performance, and security standards."

        # Collect inputs
        root_path = Prompt.ask("Project root path", default=str(default_root_path))
        root_path = Path(root_path).resolve()
        project_name = self.get_and_refine_input("Project name", default_name)
        project_goals = self.get_and_refine_input("Project goals", default_goals)
        architecture = self.get_and_refine_input("High-level architecture description", default_architecture)
        non_functional_requirements = self.get_and_refine_input(
            "Non-functional requirements (scalability, performance, etc.)", default_nfr
        )

        planning_content = f"""
# Project Planning

- **Root Path**: {root_path}
- **Name**: {project_name}
- **Goals**: {project_goals}
- **Architecture**: {architecture}
- **Non-functional Requirements**: {non_functional_requirements}
        """
        return root_path, project_name, planning_content

    def get_and_refine_input(self, prompt_text, default_value, max_tokens=100):
        """Prompt the user for input with refinement."""

        user_input = Prompt.ask(prompt_text, default=default_value)

        message = f"{prompt_text}: {user_input}"
        
        self.console.print("\n[bold yellow]Refining your input...[/bold yellow]")
        # Use the engine
        refined_input = self.ai_manager.interact(message)

        self.console.print(f"\nSuggested refinement: [green]{refined_input}[/green]")
        confirmation = Prompt.ask("Do you want to use this refinement?", choices=["yes", "no"], default="yes")
        return refined_input if confirmation == "yes" else user_input

