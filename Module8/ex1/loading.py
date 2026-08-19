import sys
import importlib.metadata


class Loading:
    def __init__(self) -> None:
        self.descriptions = {
            "pandas": "Data manipulation ready",
            "numpy": "Numerical computation ready",
            "requests": "Network access ready",
            "matplotlib": "Visualization ready",
        }

    def dependencies(self) -> None:
        installed_pkgs = {}
        for pkg, description in self.descriptions.items():
            try:
                __import__(pkg)
                version = importlib.metadata.version(pkg)
                installed_pkgs[pkg] = version
            except ImportError:
                print(f"[{pkg}] is missing from the environment.")
                print(
                    "\nTo install dependencies, run: "
                    "\npip install -r requirements.txt"
                    "\n or\npoetry install"
                )
                sys.exit(1)

        import numpy                        # type: ignore
        import pandas                       # type: ignore
        import matplotlib.pyplot as plt     # type: ignore
        import requests

        print("LOADING STATUS: Loading programs...\n")
        print("Checking dependencies:")

        for pkg, version in installed_pkgs.items():
            print(f"[OK] {pkg} ({version}) - {self.descriptions[pkg]}")

        print("\nAnalyzing Matrix data...")
        print("Processing 1000 data points...")
        print("Generating visualization...\n")
        try:
            url = "https://jsonplaceholder.typicode.com/posts"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            pandas.DataFrame(data)
            Matrix = numpy.array([
                [
                    post["userId"],
                    post["id"],
                    len(post["title"]),
                    len(post["body"])
                ]
                for post in data
            ])
            x = Matrix[:, 1]
            y = Matrix[:, 2]
            plt.plot(x, y, marker="o")
            plt.title("Post Title Length")
            plt.xlabel("Post ID")
            plt.ylabel("Title Length")
            plt.savefig('matrix_analysis.png')
            plt.close()

        except Exception as e:
            print(f"ERROR: {e}")


if __name__ == "__main__":
    loading = Loading()
    loading.dependencies()
    print("Analysis complete!\nResults saved to: matrix_analysis.png")
