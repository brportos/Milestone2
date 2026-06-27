import sys
import importlib.metadata

REQUIRED_PACKAGES = ['pandas', 'numpy', 'requests', 'matplotlib']

def check_dependencies():
    all_ok = True
    status_report = []
    for pkg in REQUIRED_PACKAGES:
        try:
            version = importlib.metadata.version(pkg)
            status_report.append(f"[OK] {pkg} ({version})")
        except importlib.metadata.PackageNotFoundError:
            status_report.append(f"[MISSING] {pkg}")
            all_ok = False
    return all_ok, status_report

def run_simulation():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    print("Analyzing Matrix data...")
    print("Processing 1000 data points...")
    time_steps = np.arange(0, 1000)
    signal = np.sin(time_steps * 0.05) + np.random.normal(0, 0.1, 1000)

    df = pd.DataFrame({"Time": time_steps, "Signal": signal})
    
    print("Generating visualization...")
    plt.figure(figsize=(10, 4))
    plt.plot(df["Time"], df["Signal"], color="#00FF00", label="Matrix Stream")
    plt.title("The Construct Data Feed")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig("matrix_analysis.png")
    print("Analysis complete!\nResults saved to: matrix_analysis.png")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...\nChecking dependencies:")
    dependencies_passed, report = check_dependencies()
    
    for line in report:
        print(line)
    if not dependencies_passed:
        is_poetry = "poetry" in "".join(sys.argv) or any("POETRY" in k for k in sys.environ)
        
        print("\n[ERROR] Missing required Matrix sub-modules.")
        print("To load them into your environment, run:")
        if is_poetry:
            print("  poetry install")
        else:
            print("  pip install -r requirements.txt")
        sys.exit(1)
    run_simulation()