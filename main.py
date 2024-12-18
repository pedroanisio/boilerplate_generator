from handlers.env_check import EnvCheckHandler
from handlers.planning import PlanningHandler
from handlers.folder_setup import FolderSetupHandler
from handlers.git_init import GitInitializationHandler
from handlers.backend_setup import BackendSetupHandler
from handlers.frontend_setup import FrontendSetupHandler
from handlers.docker_setup import DockerConfigurationHandler
from handlers.observability import ObservabilitySetupHandler
from handlers.ci_cd import CiCdSetupHandler
from utils.helpers import chain_handlers
from rich.console import Console
from dotenv import load_dotenv
import logging
import os


def load_defaults_to_context(context):
    """
    Load defaults from .env file and set them in the context.
    """
    load_dotenv()  # Load .env file into environment variables

    # Extract relevant variables and set defaults if not provided
    context["allowed_hosts"] = os.getenv("ALLOWED_HOSTS", "localhost")    
    context["node_image"] = os.getenv("NODE_IMAGE", "22-slim")
    context["node_version"] = os.getenv("NODE_VERSION", "22.12")
    context["postgres_image"] = os.getenv("POSTGRES_IMAGE", "16")
    context["postgres_version"] = os.getenv("POSTGRES_VERSION", "16")
    context["python_image"] = os.getenv("PYTHON_IMAGE", "3.13-slim")
    context["python_version"] = os.getenv("PYTHON_VERSION", "3.13.1")

    logging.info("Defaults loaded from .env and set in context.")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console = Console()
    context = {}

    # Load defaults into context
    load_defaults_to_context(context)

    # Initialize handlers
    handlers = [
        EnvCheckHandler(console),
        PlanningHandler(console),
        FolderSetupHandler(console),
        GitInitializationHandler(console),
        BackendSetupHandler(console),
        FrontendSetupHandler(console),
        DockerConfigurationHandler(console),
        CiCdSetupHandler(console),
        ObservabilitySetupHandler(console),

    ]

    # Set up the chain
    head_handler = chain_handlers(handlers)

    # Start processing
    console.print("[bold cyan]Starting project setup...[/bold cyan]")
    logging.info("Starting project setup.")
    try:
        head_handler.handle(context)  # Start the chain
        console.print("[bold green]Project setup completed successfully![/bold green]")
        logging.info("Project setup completed successfully.")
    except Exception as e:
        console.print(f"[bold red]An error occurred during setup:[/bold red] {e}")
        logging.error(f"An error occurred during setup: {e}", exc_info=True)


if __name__ == "__main__":
    main()
