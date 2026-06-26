import os
import site
import sys

if __name__ == "__main__":
    try:
        if (sys.prefix == sys.base_prefix):
            print("MATRIX STATUS: You're still plugged in\n")
            print(f"Current Python: {sys.executable}")
            print("Virtual Environment: None detected\n")
            print("WARNING: You're in the global environment!")
            print("The machines can see everything you install.\n")
            print("To enter the construct, run:")
            print("python -m venv matrix_env")
            print("source matrix_env/bin/activate # On Unix")
            print("matrix_env\\Scripts\\activate # On Windows")
            print("\nThen run this program again.")
        else:
            venv_name = os.path.basename(sys.prefix)
            pkg_paths = site.getsitepackages()
            if pkg_paths:
                pkg_path = pkg_paths[0]
            else:
                pkg_path = "Unknown"
            print("MATRIX STATUS: Welcome to the construct")
            print(f"Current Python: {sys.executable}")
            print(f"Virtual Environment: {venv_name}")
            print(f"Environment Path: {sys.prefix}")
            print(f"\nSUCCESS: You're in an isolated environment!")
            print("Safe to install packages without affecting")
            print("the global system.\n")
            print(f"Package installation path:\n{pkg_path}")
    except Exception as e:
        print(f"Error: {e}")
