# @Author: LeonSong
# @Date:   2026-07-30 22:29
# @Description: System settings

import os

from dotenv import load_dotenv

load_dotenv()


class settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    DATABASE_LOG_ECHO = os.getenv("DATABASE_LOG_ECHO") == "1"

    JWT_ACCESS_TOKEN_DURATION = int(
        os.getenv("JWT_ACCESS_TOKEN_DURATION", str(60 * 24))
    )  # minute

    JWT_KEY = os.getenv("JWT_KEY", "MMoje7EdXMUI5qaRELZTwhMb4O0UWJoax6HDIUXRahY=")

    ATTACHMENTS_DIR_ROOT = os.getenv("ATTACHMENTS_DIR_ROOT", "attachments")

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]
