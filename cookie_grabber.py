import json
import random
import time
from pathlib import Path

from seleniumbase import SB

OUTPUT_FILE = Path("session_pool.json")
KEYWORD = ["car", "cars", "auto", "vehicle", "bus"]
TARGET_URL = "https://www.google.com/search?q={}"
POOL_SIZE = 5
SLEEP = 3
MAX_SESSIONS = 500


def grab_session(session_id: str, keyword: str):
    try:
        sb_kwargs = {
            "headless": True,
            "uc": True,
        }

        with SB(**sb_kwargs) as sb:
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
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Cookie": cookie_str,
            "X-Browser-Year": "2026"    
        }
    }


def main():
    if OUTPUT_FILE.exists():
        try:
            existing_data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
            sessions = existing_data.get("sessions", [])
        except Exception:
            sessions = []
    else:
        sessions = []

    for _ in range(POOL_SIZE):
        keyword = random.choice(KEYWORD)
        session_id = f"s{len(sessions) + 1}"
        print(f"[INFO] Generating session {session_id} using keyword {keyword}")
        session = grab_session(session_id, keyword)
        sessions.append(session)

    if len(sessions) > MAX_SESSIONS:
        sessions = sessions[-MAX_SESSIONS:]

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
