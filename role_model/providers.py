from typing import List, Dict
try:
    import os
    from openai import OpenAI
    _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception:
    _client = None

def openai_provider(messages: List[Dict[str, str]]) -> str:
    if _client is None:
        raise RuntimeError("OpenAI not available. Install 'openai' and set OPENAI_API_KEY.")
    result = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        temperature=0.3,
    )
    return result.choices[0].message.content or ""
