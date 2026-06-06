import os
from openai import OpenAI
from openai._exceptions import AuthenticationError, RateLimitError, OpenAIError
from dotenv import load_dotenv
load_dotenv()

def check_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {"status": "error", "message": "API key not found"}

    client = OpenAI(api_key=api_key)

    try:
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1
        )

        return {
            "status": "success",
            "message": "API key valid and has usable quota"
        }

    except AuthenticationError:
        return {"status": "invalid_key", "message": "Invalid API key"}

    except RateLimitError as e:
        msg = str(e).lower()

        if "quota" in msg or "exceeded your current quota" in msg:
            return {
                "status": "quota_exceeded",
                "message": "API key valid but quota exhausted"
            }

        return {
            "status": "rate_limited",
            "message": "Too many requests"
        }

    except OpenAIError as e:
        return {"status": "openai_error", "message": str(e)}

    except Exception as e:
        return {"status": "unknown_error", "message": str(e)}


if __name__ == "__main__":
    print(check_openai_key())
