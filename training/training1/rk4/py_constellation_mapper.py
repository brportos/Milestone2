For this exercise, you must implement the `constellation_mapper` function. The function must:
- Take as a parameter a list of tuples, each consisting of an int(row) and an int(col).
- Return a list[str] representing a grid of size `size` * `size`, composed of "." and "*" characters based on the coordinates provided in the `stars` variable.
- Ignore coordinates that fall outside the grid boundaries.
- Ignore duplicate coordinates.

def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:




Input
constellation_mapper([(0, 0), (1, 1), (2, 2)], 3)
Output
["*..", ".*.", "..*"]

Input
constellation_mapper([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3)
Output
["***", ".*.", "..*"]

Input
constellation_mapper([(0, 0), (5, 5), (2, 2)], 3)
Output
["*..", "...", "..*"]

Input
constellation_mapper([(0, 0), (5, 5)], 2)
Output
["*.", ".."]



//py_array_rotation_detector.py

Assignment
Write a Python function that takes two lists (arrays) as parameters and determines if the second list is a rotation of the first list (left or right).

A rotation means that the elements are shifted circularly. For example, shifting [1, 2, 3] to the right by one position results in [3, 1, 2].

The function must return True if arr2 is a rotation of arr1, and False otherwise.
If the arrays have different lengths, they cannot be rotations of each other.
Two empty arrays are considered rotations of each other.
Function signature
def array_rotation_detector(arr1: list, arr2: list) -> bool:
Examples
Input
array_rotation_detector([1, 2, 3, 4, 5], [4, 5, 1, 2, 3])
Output
True
Input
array_rotation_detector([1, 2, 3, 4, 5], [5, 1, 2, 3, 4])
Output
True
Input
array_rotation_detector([1, 2, 3], [3, 2, 1])
Output
False
Input
array_rotation_detector([1, 2], [1, 2, 3])
Output
False
Input
array_rotation_detector([], [])
Output
True

py_list_intersection_finder
py_list_intersection_finder.py
Suggest Exercise
Help grow this exam bank
Suggest a new subject, report a wrong brief, or flag outdated text. Short Google form.
✕
⚡
moulinetteTitle
Allowed functions: None. Only standard C library functions explicitly allowed by the prompt may be used.
Assignment
Write a function that finds the intersection of multiple sorted lists.
Return a new list containing elements that appear in ALL input lists, in sorted order.

The function should:
- Return elements that appear in ALL lists
- Result should be sorted in ascending order
- Remove duplicates from the result
- Handle empty input or empty lists gracefully
- If any list is empty, the intersection is empty
Function signature
def list_intersection_finder(lists: list[list[int]]) -> list[int]:
Examples
Input
list_intersection_finder([[1, 2, 3], [2, 3, 4], [2, 3, 5]])
Output
[2, 3]
Input
list_intersection_finder([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]])
Output
[4]
Input
list_intersection_finder([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]])
Output
[1, 2, 3]
Input
list_intersection_finder([[1, 2, 3], [4, 5, 6]])
Output
[]
Input
list_intersection_finder([])
Output
[]
Input
list_intersection_finder([[1, 2, 3], []])
Output
[]
Input
list_intersection_finder([[5]])
Output
[5]

#04
Level 2
py_merge_sorted_list
py_merge_sorted_list.py
Suggest Exercise
Help grow this exam bank
Suggest a new subject, report a wrong brief, or flag outdated text. Short Google form.
✕
⚡
moulinetteTitle
Forbidden built-ins / modules: sorted(), .sort(), heapq.merge(). Implement the algorithm manually!
Assignment
You are given a list of sorted integer sublists in any order.
Merge all sublists into a single sorted list in ascending order and return it.

Constraints:
- The outer list may be empty -> return []
- Empty sublists may exist and should be ignored.
- Values can repeat (keep the duplicates).
- Each sublist is already sorted individually.
Function signature
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
Examples
Input
merge_sorted_list([[1, 4, 5], [1, 3, 4], [2, 6]])
Output
[1, 1, 2, 3, 4, 4, 5, 6]
Input
merge_sorted_list([[1, 2, 3], [], [0, 4]])
Output
[0, 1, 2, 3, 4]
Input
merge_sorted_list([])
Output
[]
Input
merge_sorted_list([[], []])
Output
[]

#05
Level 2
palindrome_partitioner
py_palindrome_partitioner.py
Suggest Exercise
Help grow this exam bank
Suggest a new subject, report a wrong brief, or flag outdated text. Short Google form.
✕
⚡
moulinetteTitle
Allowed functions: None. Only standard C library functions explicitly allowed by the prompt may be used.
Assignment
Given a string `s`, find the minimum number of cuts needed to partition it such that every resulting substring is a palindrome.

A cut divides the string between two characters. With `c` cuts, the string is split into `c + 1` substrings. We want the minimum number of cuts `c` such that all parts are palindromes.

Return this minimum number of cuts (an integer).

Constraints:
- An empty string or a string of length 1 is already a palindrome -> 0 cuts.
- If the entire string is already a palindrome -> 0 cuts.
- In the worst case (all characters are distinct), the result is len(s) - 1 cuts.
Function signature
def palindrome_partitioner(s: str) -> int:
Examples
Input
palindrome_partitioner("aab")
Output
1
Input
palindrome_partitioner("aba")
Output
0
Input
palindrome_partitioner("abc")
Output
2

#06
Level 2
sliding_window_maximium
py_sliding_window_maximium.py
Suggest Exercise
Help grow this exam bank
Suggest a new subject, report a wrong brief, or flag outdated text. Short Google form.
✕
⚡
moulinetteTitle
Allowed functions: None. Only standard C library functions explicitly allowed by the prompt may be used.
Assignment
Given a list of integers `nums` and an integer `k`, consider a "window" of size `k` sliding from left to right, one position at a time.

For each window position, find the maximum value within it.
Return the list of all these maximum values, in the order the windows appear.

Constraints:
- 1 <= k <= len(nums) in normal cases.
- If nums is empty or k <= 0, return [].
- The number of windows (and maximums) is: len(nums) - k + 1.
Function signature
def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
Examples
Input
sliding_window_maximium([1, 3, -1, -3, 5, 3, 6, 7], 3)
Output
[3, 3, 5, 5, 6, 7]
Input
sliding_window_maximium([4, 2, 12, 11, -5], 2)
Output
[4, 12, 12, 11]
Input
sliding_window_maximium([], 3)
Output
[]

#07
Level 3
package_dependency_resolver
package_dependency_resolver.py
Suggest Exercise
Help grow this exam bank
Suggest a new subject, report a wrong brief, or flag outdated text. Short Google form.
✕
⚡
moulinetteTitle
Forbidden built-ins / modules: graphlib.TopologicalSorter. Implement the algorithm manually!
Assignment
Write a function that determines a valid package installation order by resolving dependencies. Use topological sorting to ensure dependencies are installed before the packages that require them.

The function should:
- Take a dictionary where keys are package names and values are lists of dependencies.
- Return packages in installation order (dependencies first).
- Return an empty list ([]) if no valid order exists (e.g., circular dependencies or self-dependencies).
- Handle empty inputs and isolated dependency chains gracefully.
- Ignore references to packages that are not present as keys in the input dictionary.
- Ensure a package cannot be installed until all its dependencies are installed.

Algorithm Details & Edge Cases:
- Topological Sorting: Use a topological sort algorithm (e.g., Kahn's algorithm).
- Dependency Priority: Process packages with no remaining dependencies first.
- Deterministic Output: When multiple valid packages can be processed at the same time (choices exist), process them alphabetically to ensure deterministic output.
- Empty Input: Return an empty list.
- Multiple Independent Chains: Process all chains, respecting the alphabetical order rule.
- Missing Dependencies: Ignore missing packages (treat them as if they don't exist in the requirements).
Function signature
def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
Examples
Input
package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []})
Output
["driver", "database", "app"]
Input
package_dependency_resolver({"A": [], "B": ["A"], "C": ["A", "B"]})
Output
["A", "B", "C"]
Input
package_dependency_resolver({})
Output
[]
Input
package_dependency_resolver({"X": ["Y"], "Y": ["X"]})
Output
[]
Input
package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]})
Output
["api", "web", "backend", "frontend"]