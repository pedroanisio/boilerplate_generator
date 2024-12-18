import logging
from typing import List
from llm.abstract.abstract_memory import AbstractMemory
from llm.utils.message_loader import MessageLoader
from llm.prompt.builder import PromptBuilder
from llm.provider.llm_provider import LLMProvider
from llm.llm_brain import LLMBrain

class Persona:
    def __init__(self, llm_brain: LLMBrain, memory: AbstractMemory, config: dict):
        self.llm_brain = llm_brain
        self.memory = memory
        self.message_loader = MessageLoader()
        self.prompt_builder = PromptBuilder(model=llm_brain.model_type, max_tokens=llm_brain.max_tokens)
        self.llm_provider = LLMProvider(model=llm_brain.model_type, temperature=llm_brain.temperature, client=llm_brain.client)

        self.system_message = self.message_loader.load_system_message(config["system_message_path"])
        self.n_shots = self.message_loader.load_n_shots(config["n_shots_path"])
        self.traits = config.get("traits", [])

    def respond_to(self, user_input: str) -> str:
        messages = self.prompt_builder.build_messages(
            system_message=self.get_persona_message(),
            n_shots=self.n_shots,
            memory=self.memory.retrieve(),
            user_input=user_input
        )
        response = self.llm_provider.generate(messages)
        self.learn(user_input, response)
        return response

    def get_persona_message(self) -> str:
        traits_desc = " ".join(f"[Trait: {t}]" for t in self.traits)
        return f"{self.system_message}\n{traits_desc}".strip()

    def learn(self, user_message: str, assistant_response: str):
        self.memory.add_interaction(user_message, assistant_response)

    def reflect(self):
        messages = self.prompt_builder.reflect(memory=self.memory.retrieve())
        response = self.llm_provider.generate(messages)
        return response

    def describe(self) -> str:
        traits_description = ", ".join(self.traits) if self.traits else "None"
        return (
            f"Persona Description:\n"
            f"- System Message: {self.system_message}\n"
            f"- Traits: {traits_description}\n"
            f"- N-Shots: {len(self.n_shots)} examples"
        )
