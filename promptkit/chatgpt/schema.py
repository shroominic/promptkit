from pydantic import BaseModel


class BaseMessage(BaseModel):
    """ Base message """
    role: str
    content: str
    
    def __str__(self):
        return self.content
    
    def __repr__(self):
        return f"{self.role}: {self.content}"


class UserMessage(BaseMessage):
    """ User message """
    role: str = "user"
    content: str
    

class SystemMessage(BaseMessage):
    """ System message """
    role: str = "system"
    content: str
    
    
class AssistantMessage(BaseMessage):
    """ Assistant message """
    role: str = "assistant"
    content: str
    

class FunctionMessage(BaseMessage):
    """ Function message """
    role: str = "function"
    content: str
    name: str
    function_call: dict
