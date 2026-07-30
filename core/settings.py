# @Author: LeonSong
# @Date:   2026-07-30 22:29
# @Description: System settings

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "")
