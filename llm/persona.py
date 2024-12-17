## path : persona/persona.py
from typing import List
from memory.short_term_memory import ShortTermMemory
from utils.prompt_builder import PromptBuilder
from llm.llm_provider import LLMProvider
from llm.llm_brain import LLMBrain
from llm.utils.message_loader import MessageLoader

class Persona:
    """
    Orchestrator AI assistant interactions.
    Manages system messages, traits, memory, and LLM responses.
    """

    def __init__(self, llm_brain: LLMBrain, config: dict):
        self.llm_brain = llm_brain
        self.message_loader = MessageLoader()
        self.prompt_builder = PromptBuilder()
        self.llm_provider = LLMProvider(model=llm_brain.model_type)

        # Load self-configuration
        self.system_message = self.message_loader.load_system_message(config["system_message_path"])
        self.n_shots = self.message_loader.load_n_shots(config["n_shots_path"])
        self.traits = config.get("traits", [])

        # Initialize memory with system_message and n_shots
        self.memory = ShortTermMemory(
            system_message=self.system_message,
            n_shots=self.n_shots,
            max_length=config.get("memory_max_length", 5)
        )

    def respond_to(self, user_input: str) -> str:
        """Generate a response to the user input."""
        messages = self.prompt_builder.build_messages(
            system_message=self.get_persona_message(),
            n_shots=self.n_shots,
            memory=self.memory.retrieve(),
            user_input=user_input
        )
        response = self.llm_provider.generate_response(messages)
        self.learn(user_input, response)
        return response

    def get_persona_message(self) -> str:
        """Construct the persona's current context message."""
        traits = " ".join(f"[Trait: {trait}]" for trait in self.traits)
        return f"{self.system_message}\n{traits}"

    def learn(self, user_message: str, assistant_response: str):
        """Store interaction in memory."""
        self.memory.add_interaction(user_message, assistant_response)

    def reflect(self):
        """Reflect on memory to refine traits or strategies."""
        # Placeholder for advanced logic
        pass

    def describe(self) -> str:
        """
        Describe the Persona, including its system message, traits, and example n-shots.

        :return: A string representation of the Persona's characteristics.
        """
        traits_description = ", ".join(self.traits) if self.traits else "None"
        n_shots_description = "\n".join(
            [f"Example {i + 1}:\n  User: {n['role']} - {n['content']}" for i, n in enumerate(self.n_shots)]
        ) if self.n_shots else "No examples provided."
        return (
            f"Persona Description:\n"
            f"- System Message: {self.system_message}\n"
            f"- Traits: {traits_description}\n"
            f"- Example Interactions (n-shots):\n{n_shots_description}"
        )
