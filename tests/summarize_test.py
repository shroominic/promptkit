import asyncio
from promptkit.tools import summarize


def test_summarize():
    example = "SendGrid has a number of APIs that can easily integrate with your system and help you do amazingly simple things with your email streams. The Parse API is one of the most flexible tools you can use to simplify processes and create great email experiences for your customers."
    summary = asyncio.run(summarize(example))

    assert summary
    assert len(summary) > 10
    assert summary != example
    
    print(summary)
