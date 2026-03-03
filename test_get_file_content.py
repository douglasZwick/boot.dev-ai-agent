from functions.get_file_content import *


# lorem_output = get_file_content("calculator", "lorem.txt")
# print(lorem_output)

test_cases = [
  ("calculator", "main.py"),
  ("calculator", "pkg/calculator.py"),
  ("calculator", "/bin/cat"),
  ("calculator", "pkg/does_not_exist.py"),
]

for test_case in test_cases:
  print("-" * 64)
  print(f"Results for test case {test_case}:")
  print("vvvv")
  print(get_file_content(*test_case))
  print("^^^^")
print("-" * 64)
