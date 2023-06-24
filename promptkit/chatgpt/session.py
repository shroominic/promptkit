from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv
import openai
from .response import GPTResponse
from .schema import BaseMessage


load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")


class ChatGPTSession(BaseModel):
    """ Session with the chatgpt api """
    model: str = "gpt-3.5-turbo"
    history: List[GPTResponse] = []
    api_key: str | None = None
    cost: float = 0
    
    def __init__(self, model: str = "gpt-3.5-turbo", history: List[GPTResponse] = []):
        self.history = history
        self.model = model
        self.api_key 
        self.cost = 0
    
    def add_user(self, message: BaseMessage):
        """ Add a user message to the session history """
        msg = BaseMessage(**{"role": "user", "content": f"{message}"})
        self.history.append(msg)
    
    def add_system(self, message: str):
        """ Add a system message to the session history """
        msg = {"role": "system", "content": message}
        self.history.append(msg)
    
    def direct_response(self, instruction: str) -> GPTResponse:
        """ Add a system message as instruction and generate a response """
        self.add_system(instruction)
        return self.get_response()
    
    async def get_response(self) -> GPTResponse:
        """ Get response and add it to the session history """
        if self.history[-1]["role"] == "assistant":
            self.add_system_message("Continue your response...")
        gptresponse = await self.generate()
        self.history.append(gptresponse.message)
        print("\n".join([msg["content"].strip() for msg in self.history]))
        return gptresponse
    
    async def generate(self, history=None, **kwargs) -> GPTResponse:
        """ Generate a response using the chatgpt api """
        completion = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=history or self.history,
            **kwargs
        )
        
        # self.cost += completion.usage["total_tokens"] *  model_cost

        return GPTResponse(session=self, response=completion)
    
    def __repr__(self) -> str:
        return f"ChatGPTSession(model={self.model}, cost={})"
