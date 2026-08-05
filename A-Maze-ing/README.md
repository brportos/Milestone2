*This project has been created as part of the 42 curriculum by herinaan, and brportos.*

# A-Maze-ing

## Description
A-Maze-ing is a 2D maze generator and visualizer written in Python.
The goal of this project is to implement a reusable, packaged maze generation module (`mazegen`) and render the generated maze interactively using MiniLibX (`mlx`).

---

## Instructions
### Prerequisites
* Python 3.10+
* GNU Make

### Installation & Build
To create the virtual environment and install all dependencies (including local packages):
```bash
make install
```
To build the standalone .whl package inside dist/:
```bash
make build
```
### Execution
To run the application with the configuration file:
```bash
make or make run or python3 a_maze_ing.py config.txt
```
## Resources
Website
- https://share.google/G2pGIEU7unbXqX5IX
- https://share.google/2ux1tghLyWZ9x5f2q
AI 
- AI tools were used for explanations of concepts and function specifications.
## Additional sections
### Configuration File Structure
The configuration file (config.txt) controls the generation parameters:
- WIDTH=20
- HEIGHT=20
- ENTRY_X=0
- ENTRY_Y=0
- EXIT_X=19
- EXIT_Y=19
- SEED=42
- PERFECT=true
- `WIDTH / HEIGHT`: Grid dimensions of the maze.
- `ENTRY`: Starting cell coordinates.
- `EXIT`: Goal/exit cell coordinates.
- `SEED`: Optional random seed for reproducible maze generation.
- `PERFECT`: true generates a single path between any two points (no loops); false adds loops.
## Algorithms

### Chosen Algorithms
* **Maze Generation:** Randomized Depth-First Search (DFS / Recursive Backtracker)
* **Maze Solving / Path Finding:** Breadth-First Search (BFS)

### Why DFS for Generation?
* **Long, Complex Corridors:** DFS dives deeply in one direction before backtracking, producing long, winding, and visually challenging paths rather than short clustered loops.
* **Perfect Maze Guarantee:** DFS generates a valid spanning tree over the grid, ensuring that every cell is reachable and there are no isolated regions or loops (unless `PERFECT=false` is set).
* **Implementation Simplicity:** Using a Stack data structure allows fast generation with minimal overhead.

### Why BFS for Solving?
* **Optimal Solution:** BFS explores cells in concentric waves level-by-level, which guarantees finding the shortest path from `ENTRY` to `EXIT`.
* **Visual Appeal:** BFS pathing provides a clear contrast against DFS generation when rendering solution overlays in the visualizer.
### Code Reusability

The core maze logic is completely decoupled from the MiniLibX (`mlx`) graphical engine and packaged as a standalone, zero-GUI Python library named `mazegen`. 

1. **`mazegen.generator` (`MazeGenerator`)**:
   * Contains the pure implementation of the **Randomized DFS algorithm** for generating the maze matrix.
   * Contains the **BFS algorithm** for solving the maze and calculating the shortest path between any two points (`ENTRY` and `EXIT`).
   * Handles configuration validation (`WIDTH`, `HEIGHT`, coordinates, `SEED`, `PERFECT`).

2. **`mazegen.grid` (`Maze` / `Cell`)**:
   * Data structure representing the grid, wall states (North, South, East, West), and entry/exit coordinates.
   * Provides helper methods to export the maze to matrix representations, raw string ASCII grids, or JSON data for external applications.

---

### How to Reuse It

#### Install as a Python Wheel (`.whl`)
Once built via `make build`, the `.whl` package in `dist/` can be installed into any independent Python project or virtual environment:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Roles of Team Members
* **`brportos`:**
  - Randomized Depth-First Search (DFS).
  - Breadth-First Search (BFS) solution path.
  - Imperfect Maze algorithm
  - 3x3 cell representation
* **`herinaan`:**
  - MiniLibX (`mlx`)
  - Parsing

---

#### What Worked Well
* **Clear Task Separation:** Dividing the core generation (DFS/BFS/3x3 logic) cleanly from the MLX display interface allowed us to develop and test algorithms independently via unit tests without needing the visualizer running.
* **Complementary Algorithms:** Pairing DFS generation with BFS pathfinding created a great balance—DFS produces long, challenging branches while BFS guarantees finding the mathematically optimal solution route.

#### What Could Be Improved
* **Early Build System Integration:** We left Python wheel packaging (`build`/`poetry`) until the end, which caused late blockages with path resolution in `/tmp/`. Setting up the packaging pipeline earlier would have saved time.
* **Grid Scaling Standard:** Initial differences in how cell coordinates were mapped to the 3x3 internal layout required refactoring mid-project to align pathfinding with wall rendering.

---

### Tools Used
* **Python 3.10+ / Standard Library:** Primary programming language and core data structures (`collections.deque` for BFS).
* **MiniLibX (`mlx`):** Graphical rendering library for window management and real-time visualization.
* **GNU Make:** Makefile automation for compilation, virtual environment management, linting, and building.
* **Poetry & Build:** Python package management and wheel creation (`.whl`).
* **Flake8 & MyPy:** Static code analysis, type enforcement, and formatting checks.
* **Git & GitHub:** Branch management, code reviews, and version control.