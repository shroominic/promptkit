import re
from pydantic import BaseModel
from typing import Dict
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from promptkit.chatgpt import ChatGPTSession as Session


class GPTResponse(BaseModel):
    """ Represents a response from the chatgpt api """
    session: Session
    response: Dict

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
        if not self.session.history:
            raise ValueError("Cannot regenerate first response")
        self.response = self.session.generate(history=self.session.history[:-1])
        self.session.history[-1] = self.response.message
        return self

    def __repr__(self) -> str:
        return f"GPTResponse({self.content})"

    def __str__(self) -> str:
        return self.content
