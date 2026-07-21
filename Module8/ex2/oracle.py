import os
import sys

try:
    from dotenv import load_dotenv
except ImportError as e:
    print(f"ERROR: {e}")
    sys.exit(1)


if __name__== "__main__":
    env_exists = os.path.exists(".env")

    load_dotenv()

    matrix_mode = os.environ.get("MATRIX_MODE", "development").lower()
    database_url = os.environ.get("DATABASE_URL", "Not ste")
    api_key = os.environ.get("API_KEY", "Not set")
    log_level = os.environ.get("LOG_LEVEL", "Not set")
    zion_endpoint = os.environ.get("ZION_ENDPOINT", "Not set")

    if not matrix_mode and not database_url and not api_key:
        print("\nORACLE STATUS: Reading the Matrix...\n")
        print("Configuration loaded:")
        print("Mode: None")
        print("Database: Disconnected")
        print("API Access: Denied")
        print("Log Level: None")
        print("Zion Network: offline")
        print("Enveronment Securty check:")
        print("[WARNING] missing configuration")
        sys.exit(2)

    if matrix_mode:
        mode_str = matrix_mode.lower()
    else:
        mode_str = "development"
    if log_level:
        log_str = log_level.upper()
    else:
        log_str = "DEBUG"

    print("\nORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {mode_str}")

    if mode_str == "production":
        print("Database: Connected to live cloud instance")
        print("API Access: Production mode secured")
        print(f"Log Level: {log_level.upper() if log_level else 'WARNING'}")
        print("Zion Network: Live Mainnet")

    elif mode_str == "development":
        if database_url:
            print("Databese: Connected to local instance")
        else:
            print("Database: Missing URL")
        if api_key:
            print("API Access: Authenticated")
        else:
            print("API Access: Missing key")
        print(f"log level: {log_str}")
        if zion_endpoint:
            print("Zion Network: online")
        else:
            print("Zion network: offline")
    else:
        print(f"Database: Unknown environment ({mode_str})")
        print(f"Log Level: {log_str}")
        
    print("\nEnvironment security check:")

    if api_key and "your_key" not in api_key:
        print("[OK] No hardcoded secrets detected")
    else:
        print("[FAIL] hardcoded secret detected")
    
    if env_exists:
        print("[OK] .env file proprerly configured")
    else:
        print("[INFO] operating entirely via system terminal variables")

    gitignore_protected = False
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            if ".env" in f.read().splitlines():
                gitignore_protected = True

    if gitignore_protected:
        print("[OK] .env is properly ignored in .gitignore")

    print("[OK] Production overrides available")
    print("\n The oracle sees all configuration")
            