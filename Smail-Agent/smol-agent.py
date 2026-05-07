import datetime
import time

import numpy as np
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel, tool

load_dotenv()

# Point to your LM Studio local server
model = OpenAIServerModel(
    model_id="qwen/qwen2.5-vl-7b",
    api_base="http://192.168.1.10:1234/v1",  # Verify your LM Studio port
    api_key="no-required",
    temperature=0,
)


@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."


# Standard CodeAgent as per Unit 2
agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=["datetime"],
)

# IMPORTANT: Adding the formatting hint avoids the Regex error
agent.run(
    """
    You are a professional Python calculator. Alfred needs to know the party time.
    Tasks: Drinks (30m), Decoration (60m), Menu (45m), Music (45m).

    Current Time: Use datetime.datetime.now()

    Task: Write a Python script to:
    1. Sum the durations.
    2. Add them to the current time.
    3. Use final_answer() to print the result.

    YOUR RESPONSE MUST BE IN THIS FORMAT:
    Thoughts: I will calculate the total time and add it to now.
    <code>
    import datetime
    # your code here
    final_answer(result)
    </code>
    """
)
