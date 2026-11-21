import os
import sys
from pathlib import Path

import requests


def get_anthropic_api_key() -> str | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        return api_key.strip()

    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return None

    for line in env_path.read_text(encoding="utf-8").splitlines():
        name, separator, value = line.partition("=")
        if separator and name.strip() == "ANTHROPIC_API_KEY":
            return value.strip().strip("\"'")

    return None


def anthropic_status_message(status_code: int) -> str:
    if status_code == 200:
        return "VALID - Anthropic API accepted the key"
    if status_code == 401:
        return "REJECTED - Anthropic did not accept the supplied API key"
    if status_code == 403:
        return "FORBIDDEN - the key is valid but lacks permission for this operation"
    if status_code == 429:
        return "LIMITED - rate limit or usage quota has been reached"
    if status_code == 400:
        return "BAD REQUEST - Anthropic rejected the test request"
    if 500 <= status_code < 600:
        return "ANTHROPIC ISSUE - Anthropic returned a server error"
    return f"UNKNOWN - Anthropic returned HTTP {status_code}"


def test_anthropic_api_key():
    api_key = get_anthropic_api_key()
    if not api_key:
        message = "ANTHROPIC STATUS: MISSING - ANTHROPIC_API_KEY is not configured"
        print(message, flush=True)
        assert False, message
    if api_key == "<ANTHROPIC_API_KEY>":
        message = "ANTHROPIC STATUS: PLACEHOLDER - replace ANTHROPIC_API_KEY with a real API key"
        print(message, flush=True)
        assert False, message

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Reply with OK"}],
            },
            timeout=30,
        )
    except requests.RequestException as exc:
        message = f"ANTHROPIC STATUS: CONNECTION ERROR - {exc}"
        print(message, flush=True)
        raise AssertionError(message) from exc

    status = anthropic_status_message(response.status_code)
    status_message = f"ANTHROPIC STATUS: {status} (HTTP {response.status_code})"
    print(status_message, flush=True)

    if not response.ok:
        try:
            error = response.json().get("error", {})
            detail = error.get("message") if isinstance(error, dict) else str(error)
        except requests.JSONDecodeError:
            detail = response.text[:300]
        if detail:
            print(f"DETAIL: {detail}", flush=True)
            status_message = f"{status_message}; DETAIL: {detail}"
        assert False, status_message

    try:
        data = response.json()
    except requests.JSONDecodeError as exc:
        message = "ANTHROPIC STATUS: INVALID RESPONSE - Anthropic returned non-JSON data"
        print(message, flush=True)
        raise AssertionError(message) from exc

    assert data.get("content"), "Anthropic returned no message content"


if __name__ == "__main__":
    try:
        test_anthropic_api_key()
    except AssertionError:
        sys.exit(1)