import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent


# Load .env file relative to the project root.
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)


# --------------------------------------------------
# APPLICATION SETTINGS
# --------------------------------------------------

APP_NAME = "EduGenie"


# --------------------------------------------------
# GEMINI SETTINGS
# --------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# --------------------------------------------------
# LOCAL EXPLANATION MODEL
# --------------------------------------------------

USE_LOCAL_EXPLAINER = (
    os.getenv(
        "USE_LOCAL_EXPLAINER",
        "false"
    ).lower()
    == "true"
)


ALLOW_OFFLINE_FALLBACK = (
    os.getenv(
        "ALLOW_OFFLINE_FALLBACK",
        "true"
    ).lower()
    == "true"
)


LOCAL_EXPLAINER_MODEL = os.getenv(
    "LOCAL_EXPLAINER_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)


# --------------------------------------------------
# SECURITY / INPUT LIMIT
# --------------------------------------------------

def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name, str(default))

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    return parsed if parsed > 0 else default


MAX_INPUT_CHARS = _get_int_env("MAX_INPUT_CHARS", 20000)