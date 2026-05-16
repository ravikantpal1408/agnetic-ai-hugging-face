from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    model="qwen/qwen2.5-vl-7b",
    api_base="http://192.168.1.10:1234/v1",
    api_key="fake-key",  # LM Studio doesn't need a real one, but the field is required
    is_chat_model=True,
    timeout=600,
    temperature=0.7,
)

response = llm.complete("Hello, how are you?")
print(response)
