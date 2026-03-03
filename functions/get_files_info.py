import os
from google.genai import types


def get_files_info(working_directory, directory="."):
  header_str = f"Result for {"current" if directory == "." else directory} directory:"
  files_info = [header_str]

  try:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))

    if os.path.commonpath([working_dir_abs_path, target_dir]) != working_dir_abs_path:
      files_info.append(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
      return "\n".join(files_info)
    
    if not os.path.isdir(target_dir):
      files_info.append(f'    Error: "{directory}" is not a directory')
      return "\n".join(files_info)
    
    for item in os.listdir(target_dir):
      path = os.path.join(target_dir, item)
      name = item
      file_size = os.path.getsize(path)
      is_dir = os.path.isdir(path)
      files_info.append(f"  - {name}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(files_info)
  except Exception as ex:
    files_info.append(f'    Error: {ex}')
    return "\n".join(files_info)


schema_get_files_info = types.FunctionDeclaration(
  name="get_files_info",
  description="Lists files in a specified directory relative to the working directory, "
    "providing file size and directory status",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "directory": types.Schema(
        type=types.Type.STRING,
        description="Directory path to list files from, relative to the working directory "
          "(default is the working directory itself)",
      ),
    },
  ),
)
