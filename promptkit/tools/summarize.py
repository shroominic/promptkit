import re
from ..chatgpt import ChatGPTSession
from ..utils import retry_if_false


@retry_if_false(retries=3, except_text="Failed to summarize text")
def summarize(text: str) -> str:
    """ 
    Summarize text using the openai api 
    """
    response = ChatGPTSession(model="gpt-4").direct_response(
        f"""
        Summarize the following text: 
        {text}
        
        Reply with a codeblock and format it like this:
        ```
        SUMMARY_START
        ...
        SUMMARY_END
        ```
        """)
    summary = re.search(
        r"SUMMARY_START(.*?)SUMMARY_END", 
        response.content, 
        re.DOTALL
    ) 
    return summary.group(1).strip() if summary else ""
