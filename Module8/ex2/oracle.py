import os
import sys
from dotenv import load_dotenv


def main():
    load_dotenv()
    matrix_mode = os.environ.get("MATRIX_MODE", "development").lower()
    database_url = os.environ.get("DATABASE_URL")
    api_key = os.environ.get("API_KEY")
    log_level = os.environ.get("LOG_LEVEL")
    zion_endpoint = os.environ.get("ZION_ENDPOINT_URL")

    if not database_url or not api_key or not zion_endpoint:
        print("[ERROR] Missing vital mainframe configuration!", file=sys.stderr)
        print("Please check DATABASE_URL, API_KEY, and ZION_ENDPOINT", file=sys.stderr)
        sys.exit(1)
    if matrix_mode == "development":
        