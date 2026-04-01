import json
from core.config import QUESTIONS_FILE


def load_questions() -> list:
    return (
        json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
        if QUESTIONS_FILE.exists()
        else []
    )


def save_questions(qs: list):
    QUESTIONS_FILE.write_text(
        json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8"
    )
