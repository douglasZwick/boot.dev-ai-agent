from functions.get_files_info import *


test_cases = [
  ("calculator", "."),
  ("calculator", "pkg"),
  ("calculator", "/bin"),
  ("calculator", "../"),
]

for test_case in test_cases:
  print(get_files_info(*test_case))
