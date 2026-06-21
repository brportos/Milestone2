import sys
import os
import site

def is_inside_env() -> bool:
    return sys.prefix != sys.base_prefix

def get_venv_path() -> str | None:
    return os.environ.get("VIRTUAL_ENV")

def get_venv_name(venv_path: str) -> str:
    return os.path.basename(venv_path)

def get_site_packages() -> str:
    packages = site.getsitepackages()
    return packages[0]

def display_outside_venv() -> None:
    print("MATRIX STATUS: You're still plugged in\n")
    print(f'Current Python: {sys.executable}')
    print("Virtual Environment: None detected")
    print("\nWARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print("\nTo enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")
    print("\nThen run this program again.")

def display_inside_venv(venv_path: str) -> None:
    venv_name: str = get_venv_name(venv_path)
    site_packages: str = get_site_packages()
    print("MATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print("\nSUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system")
    print("\nPackage installation path:")
    print(f"{site_packages}")


if __name__ == "__main__":
    if is_inside_env():
        venv_path: str | None = get_venv_path()
        if venv_path is None:
            venv_path = sys.prefix
        display_inside_venv(venv_path)
    else:
        display_outside_venv()
