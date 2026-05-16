import json
import re

import requests
from smolagents import LiteLLMModel


def get_weather(city):
    """Get the current weather for a city using wttr.in API."""
    try:
        # Using wttr.in - a free weather API that doesn't require authentication
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            current_condition = data["current_condition"][0]
            temp = current_condition["temp_C"]
            description = current_condition["weatherDesc"][0]["value"]
            return f"In {city}: {description}, Temperature: {temp}°C"
        else:
            return f"Error: Unable to fetch weather data for {city}."
    except Exception as e:
        return f"Error: Unable to fetch weather data for {city}. ({str(e)})"


SYSTEM_PROMPT = """You are a helpful weather assistant. You have access to a weather tool.

When the user asks about weather, you MUST use the get_weather tool.

Available tools:
- get_weather(city): Returns the current weather for a given city

When you need to call a tool, respond ONLY with valid JSON in this format:
{
  "action": "get_weather",
  "action_input": {"city": "city name"}
}

If you have the weather information, provide a friendly response."""


def parse_action_from_response(response_text):
    """Parse the JSON action from the LLM response."""
    try:
        # Try to find JSON in code blocks first
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", response_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except json.JSONDecodeError:
        pass

    try:
        # Try to find raw JSON
        match = re.search(r'\{.*?"action".*?\}', response_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except json.JSONDecodeError:
        pass

    return None


def run_weather_agent(user_query, max_iterations=5):
    """Run the agent loop for weather queries."""

    model = LiteLLMModel(
        model_id="openai/google/gemma-3-4b",
        api_base="http://192.168.1.10:1234/v1",
        api_key="not-needed",
        num_ctx=8192,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n--- Agent Iteration {iteration} ---")

        try:
            # Get response from LLM
            response = model(messages)

            # Handle None response
            if response is None:
                print("❌ Error: LLM returned None")
                break

            response_text = response.content

            # Handle None content
            if response_text is None:
                print("❌ Error: LLM response.content is None")
                print(f"Response object: {response}")
                break

            print(f"LLM: {response_text}")

            # Try to parse action from response
            action = parse_action_from_response(response_text)

            if action is None:
                # If no action found, the LLM is giving a direct response
                print(f"\n✅ Response: {response_text}")
                return response_text

            action_name = action.get("action")
            action_input = action.get("action_input", {})

            print(f"🛠️  Using tool: {action_name}")
            print(f"📝 Input: {action_input}")

            # Execute the tool
            if action_name == "get_weather":
                city = action_input.get("city")
                observation = get_weather(city)
                print(f"✅ Result: {observation}")
            else:
                observation = f"Error: Unknown tool '{action_name}'"
                print(f"❌ {observation}")

            # Add to message history
            messages.append({"role": "assistant", "content": response_text})
            messages.append(
                {
                    "role": "user",
                    "content": f"Tool result: {observation}. Now provide the final answer to the user.",
                }
            )

        except KeyboardInterrupt:
            print("\n⚠️  Agent interrupted by user.")
            break
        except AttributeError as e:
            print(f"❌ AttributeError: {e}")
            print(f"Response type: {type(response)}")  # pyright: ignore[reportPossiblyUnboundVariable]
            print(f"Response: {response}")  # pyright: ignore[reportPossiblyUnboundVariable]
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()
            break

    print("\n⚠️  Max iterations reached.")
    return None


if __name__ == "__main__":
    # Test the agent
    print("🌤️  Weather Agent")
    print("=" * 50)

    # Test queries
    test_queries = [
        "What's the weather in London?",
        "Tell me the weather in New York",
        "How's the weather in Tokyo?",
    ]

    for query in test_queries:
        print(f"\n📍 User: {query}")
        result = run_weather_agent(query)
        print(f"\n{'=' * 50}")
