from smolagents import CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel

search_tool = DuckDuckGoSearchTool()

model = OpenAIServerModel(
    model_id="qwen/qwen2.5-vl-7b",
    api_base="http://192.168.1.10:1234/v1",  # Verify your LM Studio port
    api_key="no-required",
    temperature=0,
)

agent = CodeAgent(
    model=model,
    tools=[search_tool],
)


prompt = """
    Search for luxury superhero party ideas.
    Also based on party idea create top 10 english pop song list
    Provide a concise summary in a single python string using final_answer().
"""

response = agent.run(prompt)

print(response)
