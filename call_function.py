from typing import Callable
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *


available_functions = types.Tool(
  function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
  ],
)


def call_function(function_call: types.FunctionCall, verbose: bool=False) -> types.Content:
  name = function_call.name or ""
  args = dict(function_call.args) if function_call.args else {}

  if verbose:
    print(f"Calling function: {name}({args})")
  else:
    print(f" - Calling function: {name}")
  
  function_map: dict[str, Callable] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
  }

  if name not in function_map:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
          name=name,
          response={"error": f"Unknown function: {name}"},
        ),
      ],
    )
  
  args["working_directory"] = "./calculator"

  function_result = function_map[name](**args)

  return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
        name=name,
        response={"result": function_result},
      ),
    ],
  )
