import os
from google.genai import types
from config import MAX_READ


def get_file_content(working_directory, file_path):
  header_str = f"Reading file {file_path}:"
  output = [header_str]

  try:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    target_dir = os.sep.join(target_path.split(os.sep)[:-1])
    
    if os.path.commonpath([working_dir_abs_path, target_dir]) != working_dir_abs_path:
      output.append(f'    Error: Cannot read "{file_path}" because it is outside the permitted working directory')
      return "\n".join(output)
    
    if not os.path.isfile(target_path):
      output.append(f'    Error: File "{file_path}" not found, or it is not a regular file')
      return "\n".join(output)
    
    with open(target_path, "r") as f:
      output.append(f.read(MAX_READ))
      
      if f.read(1):
        output.append(f'[...File "{file_path}" truncated at {MAX_READ} characters]')
    
    return "\n".join(output)
    
  except Exception as ex:
    output.append(f'    Error: {ex}')
    return "\n".join(output)


schema_get_file_content = types.FunctionDeclaration(
  name="get_file_content",
  description="Retrieves the contents of the specified file",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Local path to the desired file",
      ),
    },
    required=["file_path"],
  ),
)
