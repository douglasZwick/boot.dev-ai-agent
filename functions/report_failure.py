from google.genai import types
from diagnostics import set_no_conclusion_reached


def report_failure(*args, **kwargs) -> None:
  set_no_conclusion_reached()


schema_report_failure = types.FunctionDeclaration(
  name="report_failure",
  description="Reports to the system that you were unable to solve the given problem",
)
