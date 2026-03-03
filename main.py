import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from client_interface import run
from diagnostics import ErrorCode, get_error_code, get_error_value


MAX_ITERATIONS = 20

def vprint(*args, v=False, **kwargs):
  if v: print(*args, **kwargs)

def main() -> None:
  load_dotenv()
  api_key = os.environ.get("GEMINI_API_KEY")
  if api_key is None: raise RuntimeError("GEMINI_API_KEY not found")

  parser = argparse.ArgumentParser(description="Chatbot")
  parser.add_argument("user_prompt", type=str, help="User prompt")
  parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
  args = parser.parse_args()

  client = genai.Client(api_key=api_key)
  messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

  responses = run(client, messages, args.verbose)

  for response in responses:
    print(response)
  
  if get_error_code() == ErrorCode.NoConclusionReached:
    print("The agent was unable to reach a conclusion within the allotted iterations.")


if __name__ == "__main__":
  main()
  sys.exit(get_error_value())
