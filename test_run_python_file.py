from functions.run_python_file import *


test_cases = [
  ("calculator", "main.py"),
  ("calculator", "main.py", ["3 + 5"]),
  ("calculator", "tests.py"),
  ("calculator", "../main.py"),
  ("calculator", "nonexistent.py"),
  ("calculator", "lorem.txt"),
]

for test_case in test_cases:
  print("-" * 64)
  print(f"Results for test case {test_case}:")
  print("vvvv")
  print(run_python_file(*test_case))
  print("^^^^")
print("-" * 64)
