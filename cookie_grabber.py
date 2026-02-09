import json
import os
import random
import time
from pathlib import Path

from seleniumbase import SB

OUTPUT_FILE = Path("session_pool.json")
KEYWORD = ["car", "cars", "auto", "vehicle", "bus"]
TARGET_URL = "https://www.google.com/search?q={}"
POOL_SIZE = 4
SLEEP = 3


def grab_session(session_id: str, keyword: str):
    try:
        with SB(
            headless=True,
            uc=True,
            chromium_arg="--no-sandbox",
        ) as sb:
            sb.open(TARGET_URL.format(keyword))
            sb.sleep(SLEEP)
            sb.driver.refresh()
            sb.sleep(SLEEP)

            cookies = sb.get_cookies()
            ua = sb.get_user_agent()

    except Exception as e:
        raise RuntimeError(
            f"Failed to create session {session_id} with keyword {keyword}"
        ) from e

    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)

    return {
        "id": session_id,
        "headers": {
            "User-Agent": ua,
            "Cookie": cookie_str,
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    }


def main():
    sessions = []

    for i in range(POOL_SIZE):
        keyword = random.choice(KEYWORD)
        session_id = f"s{i+1}"

        print(f"[INFO] Generating session {session_id} using keyword {keyword}")
        session = grab_session(session_id, keyword)
        sessions.append(session)

    payload = {
        "updated_at": int(time.time()),
        "sessions": sessions,
    }

    OUTPUT_FILE.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
