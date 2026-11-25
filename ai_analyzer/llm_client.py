from abc import ABC, abstractmethod
import json
from pathlib import Path

class Template_ai(ABC):  # The template every AI client must follow
    @abstractmethod # Compulsory
    def ask(self, prompt): # The rule is AI must have an ask that takes the prompt
        pass

class Mock(Template_ai):  # Mock AI used in D2
    def __init__(self, reply=None):  # a test can hand in its own reply
        self.reply = reply

    def ask(self, prompt): # The ask function from above that the template says must follow
        if self.reply is not None:  # if a test gave a reply use that reply
            return self.reply
        return json.dumps({  # Else use the normal reply
            "risk": "Medium",
            "reasons": ["For now this is a mock reply and the real AI is connected in Deliverable 3"]
        })
class Groq_client(Template_ai):  # The real AI that will be connected in D3 as Must Have feature
    def ask(self, prompt):
        raise NotImplementedError("The Groq client is connected in Deliverable 3.")

config_file = Path(__file__).parent / "config.json" # finds config.json file
def load_config(): # Reads the settings from the config.json file
    with open(config_file, encoding="utf-8") as f: #Opens the file
        return json.load(f) # Loads it into python data

def create_llm_client(config): # Decides which AI to use based on the provider in config.json file
    if config["provider"] == "mock":
        return Mock() # Ue the mock if the  config.json keys value is mock
    if config["provider"] == "groq":
        return Groq_client() # Use the real AI if it says groq, this is for D3
    raise ValueError(f"Unknown AI provider '{config['provider']}' in config.json.") # Anything else is an error