import json
import re
from typing import List, Optional
from openai import OpenAI

from utils.config import SYSTEM_PROMPT, USER_TASK_TMPL


def _try_responses_api(client: OpenAI, model: str, system: str, user: str) -> Optional[dict]:
    """
    Try to use the new Responses API. Return dict or None if not supported.
    """
    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        txt = resp.output_text
        return json.loads(txt)
    except (TypeError, AttributeError):
        return None
    except Exception as e:
        raise e


def _use_chat_completions(client: OpenAI, model: str, system: str, user: str) -> dict:
    """
    Fallback using Chat Completions with new API format.
    """
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        m = re.search(r"\{.*\}", content, flags=re.S)
        return json.loads(m.group(0)) if m else {"raw": content}


def analyze_chunk(client: OpenAI, chunk_text: str, target_role: Optional[str], model: str) -> dict:
    """Analyze a single chunk of resume text."""
    role_line = f"Target Role: {target_role}\n" if target_role else ""
    user = USER_TASK_TMPL.format(role_line=role_line, body=chunk_text)

    data = _try_responses_api(client, model, SYSTEM_PROMPT, user)
    if data is not None:
        return data

    return _use_chat_completions(client, model, SYSTEM_PROMPT, user)


def fuse_partials(client: OpenAI, partials: List[dict], target_role: Optional[str], model: str) -> dict:
    """Merge multiple partial analyses into one coherent result."""
    fuse_prompt = f"""
You are merging multiple partial analyses (JSON objects) from different chunks
of the same resume. Combine them into one **deduped, coherent** final JSON with
the same keys and requirements as before.

Target Role: {target_role or "General Software Engineer"}

Here are the partial JSON analyses:
{json.dumps(partials, ensure_ascii=False, indent=2)}
"""
    data = _try_responses_api(client, model, SYSTEM_PROMPT, fuse_prompt)
    if data is not None:
        return data
    return _use_chat_completions(client, model, SYSTEM_PROMPT, fuse_prompt)
