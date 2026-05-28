import json
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "json/config.json"
QUESTIONS_FILE = BASE_DIR / "json/perguntas.json"
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

ASSETS_DIR = BASE_DIR / "assets"
ICON_PATH = ASSETS_DIR / "car-icon.svg"

THEMES = {
    "dark": {
        "bg": "#1e1e20",
        "surface": "#2a2a2c",
        "surface_hover": "#323235",
        "border": "#363638",
        "line": "#303032",
        "text_pri": "#efefef",
        "text_mut": "#8a8a8c",
        "text_dim": "#5a5a5c",
        "accent": "#808080",
        "accent_bg": "#212121",
        "green": "#34d399",
        "red": "#fb7185",
        "orange": "#8A6D53",
    },
    "light": {
        "bg": "#f5f5f7",
        "surface": "#ffffff",
        "surface_hover": "#ebebec",
        "border": "#d1d1d6",
        "line": "#e5e5ea",
        "text_pri": "#1c1c1e",
        "text_mut": "#8e8e93",
        "text_dim": "#aeaeb2",
        "accent": "#0066ff",
        "accent_bg": "#ffefff",
        "green": "#10b981",
        "red": "#ef4444",
        "orange": "#b07a50",
    },
}

DEFAULT_CONFIG = {
    "theme": "dark",
    "font_family": "Inter",
    "font_size": 13,
    "questions_per_round": 5,
    "gemini_api_key": "",
    "gemini_model": "gemini-flash-lite-latest",
}

GEMINI_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3-flash-preview",
    "gemini-3.1-pro-preview",
    "gemini-pro-latest",
]

_CFG: dict = {}


def load_config() -> dict:
    global _CFG
    conf = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            json_data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            conf.update(json_data)
        except Exception:
            pass
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        conf["gemini_api_key"] = env_key
    _CFG.clear()
    _CFG.update(conf)
    return _CFG


def save_config():
    api_key = _CFG.get("gemini_api_key", "")
    if not ENV_FILE.exists():
        ENV_FILE.touch()
    set_key(str(ENV_FILE), "GEMINI_API_KEY", api_key)
    conf_to_save = _CFG.copy()
    if "gemini_api_key" in conf_to_save:
        del conf_to_save["gemini_api_key"]
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(conf_to_save, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _c(key: str) -> str:
    theme = _CFG.get("theme", "dark")
    if theme not in THEMES:
        theme = "dark"
    return THEMES[theme].get(key, "#ff00ff")


def build_stylesheet() -> str:
    fam = _CFG.get("font_family", "Inter")
    size = _CFG.get("font_size", 13)
    return f"""
* {{ font-family: '{fam}', 'SF Pro Text', 'Segoe UI', sans-serif; font-size: {size}px; }}
QMainWindow, QWidget {{ background: {_c('bg')}; color: {_c('text_pri')}; border: none; }}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 6px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {_c('border')}; border-radius: 3px; min-height: 20px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QLabel {{ background: transparent; border: none; }}
QFrame {{ border: none; }}
QLineEdit {{
    background: {_c('bg')}; color: {_c('text_pri')};
    border: 1px solid {_c('border')}; border-radius: 8px; padding: 7px 11px;
}}
QLineEdit:focus {{ border: 1px solid {_c('accent')}; }}
QComboBox {{
    background: {_c('bg')}; color: {_c('text_pri')};
    border: 1px solid {_c('border')}; border-radius: 8px;
    padding: 5px 11px; min-height: 32px;
}}
QComboBox:focus {{ border: 1px solid {_c('accent')}; }}
QComboBox::drop-down {{ border: none; width: 22px; }}
QComboBox QAbstractItemView {{
    background: {_c('surface')}; color: {_c('text_pri')};
    border: 1px solid {_c('border')}; border-radius: 8px;
    selection-background-color: {_c('surface_hover')}; outline: none;
}}
QSpinBox {{
    background: {_c('bg')}; color: {_c('text_pri')};
    border: 1px solid {_c('border')}; border-radius: 8px;
    padding: 5px 10px; min-height: 32px;
}}
QSpinBox:focus {{ border: 1px solid {_c('accent')}; }}
QSpinBox::up-button, QSpinBox::down-button {{ border: none; background: transparent; width: 16px; }}
"""
