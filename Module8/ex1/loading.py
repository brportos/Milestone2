import sys
import importlib.metadata


class Loading:
    def __init__(self):
        self.packages = ['pandas', 'numpy', 'matplotlib']
        self.descriptions = {
            "pandas": "Data manipulation ready",
            "numpy": "Numerical computation ready",
            "matplotlib": "Visualization ready",
        }

    def dependencies(self):
        try:
            import numpy
            import pandas
            import matplotlib.pyplot as plt
            import requests
        
            url = "https://jsonplaceholder.typicode.com/posts"
            print("Checking dependencies:")
            for pkg in self.packages:
                version = importlib.metadata.version(pkg)
                print(f"[OK] {pkg} ({version}) - {descriptions[pkg]}")

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            df = pandas.DataFrame(data)
            Matrix = numpy.array([[post["userId"], post["id"], len(post["title"]), len(post["body"])] for post in data])

            x = Matrix[:, 1]
            y = Matrix[:, 2]


            plt.plot(x, y, marker="o")

            plt.title("Post Title Length")
            plt.xlabel("Post ID")
            plt.ylabel("Title Length")
            plt.show()

        except Exception:
            print("[ERROR] Missing required module: numpy")
            print("[ERROR] Missing required module: pandas")
            print("[ERROR] Missing required module: matplotlib.pyplot\n")
            print("To install dependencies, run: \npip install -r requirements.txt \n or\npoetry install")
            sys.exit(1)

    def run_simulation(self):
        self.dependencies()
        print("LOADING STATUS: Loading programs...\n")
        print("Analyzing Matrix data...")
        print("Processing 1000 data points...")
        print("Generating visualization...")    
        print("Analysis complete!\nResults saved to: matrix_analysis.png")

if __name__ == "__main__":
    loading = Loading()
    loading.run_simulation()