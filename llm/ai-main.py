import json
from llm.llm_brain import LLMBrain
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from memory.composite_memory import CompositeMemory
from persona.persona import Persona

# Load configuration
with open("config/config.json") as f:
    config = json.load(f)

# Initialize core components
llm_brain = LLMBrain(model_type=config["model_name"], max_tokens=config["max_tokens"])
short_term_memory = ShortTermMemory(max_length=5)
long_term_memory = LongTermMemory()
memory = CompositeMemory(short_term_memory, long_term_memory)

# Initialize Persona
persona = Persona(llm_brain=llm_brain, memory=memory, config=config)

# Example user interaction
user_input = "What are the best practices for microservices?"
response = persona.respond_to(user_input)
print("Assistant:", response)

# Persona reflects on the conversation
persona.reflect()
