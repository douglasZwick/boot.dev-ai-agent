import os
from google.genai import types


def write_file(working_directory, file_path, content):
  header_str = f'Writing to file "{file_path}":'
  output = [header_str]

  try:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    
    if os.path.commonpath([working_dir_abs_path, target_path]) != working_dir_abs_path:
      output.append(f'    Error: Cannot write to "{file_path}" because it is outside the permitted working directory')
      return "\n".join(output)
    
    if os.path.isdir(target_path):
      output.append(f'    Error: Cannot write to "{file_path}" because it is a directory')
      return "\n".join(output)
    
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)

    with open(target_path, "w") as f:
      chars_written = f.write(content)
      output.append(f'  Successfully wrote to "{file_path}" ({chars_written} characters written)')

    return "\n".join(output)

  except Exception as ex:
    output.append(f'    Error: {ex}')
    return "\n".join(output)


schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes the given content to a file at the specified path",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Local path to the desired output file. "
          "Will be overwritten if it already exists",
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="The content to write to the file",
      ),
    },
    required=["file_path", "content"],
  ),
)
