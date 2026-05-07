from smolagents import OpenAIServerModel, ToolCallingAgent, WebSearchTool

model = OpenAIServerModel(
    model_id="qwen/qwen2.5-vl-7b",
    api_base="http://192.168.1.10:1234/v1",  # Verify your LM Studio port
    api_key="no-required",
    temperature=0,
)

agent = ToolCallingAgent(tools=[WebSearchTool()], model=model)


agent.run(
    "Search for the best music recommendations for a party at the Wayne's mansion."
)
