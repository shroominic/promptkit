import re    
    

class GPTResponse:
    """ Represents a response from the chatgpt api """
    
    def __init__(self, session, response: dict):
        self.response = response
        self.session = session
    
    def get_codeblock(self) -> str:
        return re.search(
            r"```(\w+)(.*?)```", 
            self.content, re.DOTALL
        ).group(2)

    def get_bool(self) -> bool:
        """ Extract boolean from response """
        return self.content.lower().startswith("y")
    
    def regenerate(self):
        """ Regenerate the response """
        self.response = self.session.generate(history=self.session.history[:-1])
        self.session.history[-1] = self.response.message
        return self
    
    @property
    def message(self) -> str:
        return self.response["choices"][0]["message"]
    
    @property
    def content(self) -> str:
        return self.message["content"].strip()
    
    @property
    def model(self) -> str:
        return str(self.response["model"])
    
    @property
    def usage(self) -> int:
        return int(self.response["usage"]["total_tokens"])
    
    @property
    def finish_reason(self) -> str:
        return str(self.response["choices"][0]["finish_reason"])
    
    def __repr__(self) -> str:
        return f"GPTResponse({self.content})"
    
    def __str__(self) -> str:
        return self.content