import re
import pydantic

from promptkit.chatgpt.schema import AssistantMessage
from promptkit.chatgpt.session import ChatSession


class AssistantResponse(AssistantMessage):
    """ 
    Represents a response or message from the chatgpt api 
    """
    session: ChatSession
    response: dict
    
    def __init__(self, session: ChatSession, response: dict) -> None:
        super().__init__(role="assistant", 
                         content=response["choices"][0]["message"]["content"].strip(),
                         session=session,  # type: ignore
                         response=response)  # type: ignore

    @property
    def model(self) -> str:
        return str(self.response["model"])

    @property
    def usage(self) -> int:
        return int(self.response["usage"]["total_tokens"])

    @property
    def finish_reason(self) -> str:
        return str(self.response["choices"][0]["finish_reason"])

    def get_codeblock(self) -> str | None:
        return code.group(2) if (
            code := re.search(
            r"```(\w+)(.*?)```",
            self.content, re.DOTALL)
        ) else None

    def get_bool(self) -> bool:
        """ Yes/No response to boolean """
        return self.content.lower().startswith("y")

    async def regenerate(self):
        """ Regenerate the response based on the session history """
        if not self.session.history:
            raise ValueError("Cannot regenerate first response")
        self = await self.session.generate(history=self.session.history[:-1])
        self.session.history.pop()
        self.session.history.append(self)
        return self

    def __repr__(self) -> str:
        return f"GPTResponse({self.content})"

    def __str__(self) -> str:
        return self.content
