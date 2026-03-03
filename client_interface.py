from google import genai
from google.genai import types
from prompts import get_system_prompt
from call_function import call_function, get_available_functions
from config import MAX_ITERATIONS, MODEL
from diagnostics import ErrorCode, get_error_code


Client = genai.Client
Content = types.Content
Response = types.GenerateContentResponse


def run(client: Client, messages: list[Content], verbose:bool=False) -> list[str]:
  prompt_token_count = 0
  response_token_count = 0

  response_text = []

  for iteration_index in range(MAX_ITERATIONS):
    response = client.models.generate_content(
      model=MODEL,
      contents=messages,
      config=types.GenerateContentConfig(
        tools=[get_available_functions(MAX_ITERATIONS, iteration_index)],
        system_instruction=get_system_prompt(MAX_ITERATIONS, iteration_index)
      ),
    )

    usage_metadata = response.usage_metadata
    if not usage_metadata: raise RuntimeError("Failed API request or something")

    prompt_token_count += usage_metadata.prompt_token_count or 0
    response_token_count += usage_metadata.candidates_token_count or 0

    if response.candidates:
      for candidate in response.candidates:
        if candidate.content: messages.append(candidate.content)

    calls = response.function_calls
    if calls:
      results = []
      for call in calls:
        function_call_result = call_function(call, verbose)
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
        if verbose:
          response_text.append(f"  -> {returned_value}")

      messages.append(Content(role="user", parts=results))

    code = get_error_code()

    if code == ErrorCode.OK or code == ErrorCode.NoConclusionReached:
      response_text.append(f"Iterations used: {iteration_index + 1} / {MAX_ITERATIONS}")
      response_text.append(response.text)
      break

  return response_text
