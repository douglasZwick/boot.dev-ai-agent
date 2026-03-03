import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
  header_str = f'Executing file "{file_path}":'
  output = [header_str]

  try:
    working_dir_abs_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    if os.path.commonpath([working_dir_abs_path, target_path]) != working_dir_abs_path:
      output.append(f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
      return "\n".join(output)
    
    if not os.path.isfile(target_path):
      output.append(f'    Error: File "{file_path}" does not exist or is not a regular file')
      return "\n".join(output)
    
    _, file_ext = os.path.splitext(file_path)

    if file_ext != ".py":
      output.append(f'    Error: "{file_path}" is not a Python file')
      return "\n".join(output)
    
    command = ["python", target_path]
    if args:
      command.extend(args)

    completed_subprocess = subprocess.run(command,
      cwd=working_directory,
      capture_output=True,
      text=True,
      timeout=30)
    
    returncode = completed_subprocess.returncode
    if returncode:
      output.append(f"  Process exited with code {returncode}")
    
    stdout, stderr = completed_subprocess.stdout, completed_subprocess.stderr
    if stdout == "" and stderr == "":
      output.append("  No output produced")
    else:
      output.append(f"STDOUT: {stdout}\nSTDERR: {stderr}")

    return "\n".join(output)

  except Exception as ex:
    output.append(f'    Error: {ex}')
    return "\n".join(output)


schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Executes the specified Python file",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="Local path to the file to execute",
      ),
      "args": types.Schema(
        type=types.Type.ARRAY,
        description="(Optional) The arguments to pass to the code being run. Defaults to None",
        items=types.Schema(
          type=types.Type.STRING,
        ),
      ),
    },
    required=["file_path"],
  ),
)
