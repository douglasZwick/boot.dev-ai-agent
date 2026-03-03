import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import call_function, available_functions


def vprint(*args, v=False, **kwargs):
  if v: print(*args, **kwargs)

def main():
  load_dotenv()
  api_key = os.environ.get("GEMINI_API_KEY")
  if api_key is None: raise RuntimeError("GEMINI_API_KEY not found")

  parser = argparse.ArgumentParser(description="Chatbot")
  parser.add_argument("user_prompt", type=str, help="User prompt")
  parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
  args = parser.parse_args()
  v = args.verbose

  client = genai.Client(api_key=api_key)

  messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
      tools=[available_functions],
      system_instruction=system_prompt,
    ),
  )
  usage_metadata = response.usage_metadata
  if usage_metadata is None: raise RuntimeError("Failed API request or something")
  prompt_tokens = usage_metadata.prompt_token_count
  response_tokens = usage_metadata.candidates_token_count

  vprint(f"User prompt: {args.user_prompt}", v=v)
  vprint(f"Prompt tokens: {prompt_tokens}", v=v)
  vprint(f"Response tokens: {response_tokens}", v=v)
  vprint("Response:", v=v)

  calls = response.function_calls
  results = []
  if calls:
    for call in calls:
      function_call_result = call_function(call, v)
      parts = function_call_result.parts

      if not parts or len(parts) <= 0:
        raise Exception(f'Empty or nonexistent parts list ({parts}) '
          f'on call result from "{call.name}"')

      function_response = parts[0].function_response

      if not function_response:
        raise Exception(f'Invalid parts in parts list ({parts}) '
          f'on call result from "{call.name}"')
      
      returned_value = function_response.response
      if not returned_value:
        raise Exception(f'Invalid returned value in call result from "{call.name}"')
      
      results.append(parts[0])
      vprint(f'  -> {returned_value}', v=v)

  else:
    print(response.text)


if __name__ == "__main__":
  main()
