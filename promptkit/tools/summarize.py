import re
from promptkit.chatgpt import ChatSession
from promptkit.utils import retry_if_false, from_template


# @retry_if_false(retries=3, except_text="Failed to summarize text")
async def summarize(text: str) -> str | None:
    """ 
    Summarize text using the openai api 
    """
    response = await ChatSession(model="gpt-4").direct_response(
        from_template("summarize", text=text),
    )
    summary = re.search(
        r"SUMMARY_START(.*?)SUMMARY_END", 
        response.content, 
        re.DOTALL
    ) 
    return summary.group(1).strip() if summary else None
