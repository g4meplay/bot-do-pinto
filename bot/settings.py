from pathlib import Path
from os import getenv as env
from dotenv import load_dotenv as load

BASE_DIR = Path(__file__).parent.parent

load(BASE_DIR / ".env", override=True)
load(BASE_DIR / ".env.example", override=False)

TOKEN = env("TOKEN")
