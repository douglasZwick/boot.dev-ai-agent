from functions.write_file import *


test_cases = [
  ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
  ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
  ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]

for test_case in test_cases:
  print("-" * 64)
  print(f"Results for test case {test_case}:")
  print("vvvv")
  print(write_file(*test_case))
  print("^^^^")
print("-" * 64)
