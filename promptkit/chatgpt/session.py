from typing import List
from dotenv import load_dotenv
from os import getenv
from .response import GPTResponse
import openai

load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")


class ChatGPTSession:
    """ Session with the chatgpt api """

    def __init__(self, model: str = "gpt-3.5-turbo", history: List[GPTResponse] = []):
        self.history = history
        self.model = model
        self.usage = 0
    
    def add_user(self, message: str):
        """ Add a user message to the session history """
        msg = {"role": "user", "content": f"{message}"}
        self.history.append(msg)
    
    def add_system(self, message: str):
        """ Add a system message to the session history """
        msg = {"role": "system", "content": message}
        self.history.append(msg)
    
    def direct_response(self, instruction: str) -> GPTResponse:
        """ Add a system message as instruction and generate a response """
        self.add_system(instruction)
        return self.get_response()
    
    def get_response(self) -> GPTResponse:
        """ Get response and add it to the session history """
        if self.history[-1]["role"] == "assistant":
            self.add_system_message("Continue your response...")
        gptresponse = self.generate()
        self.history.append(gptresponse.message)
        print("\n".join([msg["content"].strip() for msg in self.history]))
        return gptresponse
    
    def generate(self, history=None, **kwargs) -> GPTResponse:
        """ Generate a response using the chatgpt api """
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=history or self.history,
            **kwargs
        )
        self.usage += completion.usage["total_tokens"]

        return GPTResponse(self, completion)
    
    def __repr__(self) -> str:
        return f"ChatGPTSession(model={self.model}, cost={self.usage * 0.00003})"
