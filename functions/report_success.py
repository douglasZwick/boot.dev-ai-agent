from google.genai import types
from diagnostics import set_ok


def report_success(*args, **kwargs) -> None:
  set_ok()


schema_report_success = types.FunctionDeclaration(
  name="report_success",
  description="Reports to the system that you successfully solved the given problem",
)
