import sys
import importlib.metadata


PACKAGES = ['pandas', 'numpy', 'requests', 'matplotlib']
descriptions = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "requests": "Network access ready",
    "matplotlib": "Visualization ready",
}

def dependencies():
    try:
        import numpy
        import pandas
        import matplotlib.pyplot
        print("Checking dependencies:")
        for pkg in PACKAGES:
            version = importlib.metadata.version(pkg)
            print(f"[OK] {pkg} ({version}) - {descriptions[pkg]}")

    except ImportError:
        print("[ERROR] Missing required module: numpy")
        print("[ERROR] Missing required module: pandas")
        print("[ERROR] Missing required module: matplotlib.pyplot\n")
        print("To install dependencies, run: \npip install -r requirements.txt \n or\npoetry install")
        sys.exit(1)

def run_simulation():
    print("LOADING STATUS: Loading programs...\n")
    dependencies()
    print("Analyzing Matrix data...")
    print("Processing 1000 data points...")
    
    time_steps = numpy.arange(0, 1000)
    signal = numpy.sin(time_steps * 0.05) + numpy.random.normal(0, 0.1, 1000)
    df = pandas.DataFrame({"Time": time_steps, "Signal": signal})
    
    print("Generating visualization...")
    matplotlib.pyplot.figure(figsize=(10, 4))
    matplotlib.pyplot.plot(df["Time"], df["Signal"], color="#00FF00", label="Matrix Stream")
    matplotlib.pyplot.title("The Construct Data Feed")
    matplotlib.pyplot.grid(True, linestyle="--", alpha=0.5)
    matplotlib.pyplot.savefig("matrix_analysis.png")
    
    print("Analysis complete!\nResults saved to: matrix_analysis.png")

if __name__ == "__main__":
    run_simulation()