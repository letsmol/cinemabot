import os
from pathlib import Path


TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY", "")


BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "base.db"
TEMPLATES_DIR = BASE_DIR / "templates"

BAD_LINKS = open(BASE_DIR / "bad_links.txt").readlines()
