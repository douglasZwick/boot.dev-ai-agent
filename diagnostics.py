from enum import Enum, auto

class ErrorCode(Enum):
  OK = 0
  NoConclusionReached = auto()

  NoStatusSet = -1


status = { "error_code": ErrorCode.NoStatusSet }

def get_error_code() -> ErrorCode:
  return status["error_code"]

def get_error_value() -> int:
  return status["error_code"].value

def set_ok() -> None:
  status["error_code"] = ErrorCode.OK

def set_no_conclusion_reached() -> None:
  status["error_code"] = ErrorCode.NoConclusionReached
