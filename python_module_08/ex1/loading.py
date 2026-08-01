import sys
import importlib.metadata
from importlib.util import find_spec


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
        missing_pkg = []
        for pkg, description in self.descriptions.items():
            spec = find_spec(pkg)
            if spec is None:
                missing_pkg.append(pkg)
            else:
                try:
                    version = importlib.metadata.version(pkg)
                    installed_pkgs[pkg] = version
                except Exception:
                    installed_pkgs[pkg] = "Unknown version"
                    sys.exit(1)

        if missing_pkg:
            print("\n[ERROR] Missing depedencies such as:")
            for pkg in missing_pkg:
                print(f" -{pkg}")

            print("\nTo install dependencies, run: ")
            print("pip install -r requirements.txt")
            print("Or\npoetry install\n")
            sys.exit(0)

        try:
            import numpy
            import pandas
            import requests
            import matplotlib.pyplot as plt
        except ImportError as e:
            print(f"ERROR: {e}")
            sys.exit(2)

        print("\nLOADING STATUS: Loading programs...\n")
        print("Checking dependencies:")

        for pkg, version in installed_pkgs.items():
            print(f"[OK] {pkg} ({version}) - {self.descriptions[pkg]}")

        print(
            "\nPIP:\n"
            "-Installs packages, nothing else\n"
            "-Uses requirements.txt file\n"
            "-Dependency versions can conflict silently\n"
            )

        print(
            "POETRY:\n"
            "-Installs packages and manages the project\n"
            "-Uses pyproject.toml and poetry.lock files\n"
            "-Resolves dependency conflicts before installation\n"
            )

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
            plt.savefig('matrix_analysis.png')
            plt.close()

        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(3)


if __name__ == "__main__":
    loading = Loading()
    loading.dependencies()
    print("Analysis complete!\nResults saved to: matrix_analysis.png")
