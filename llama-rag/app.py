# app.py
import os

from retriever import load_and_prepare_dataset
from smolagents import CodeAgent, InferenceClientModel
from tools import GuestInfoRetrieverTool


def main():
    # 1. Verification of HF Token setup
    if not os.getenv("HF_TOKEN"):
        print("⚠️ Warning: 'HF_TOKEN' environment variable not detected.")
        print("Please set your Hugging Face token before running the script.")
        return

    # 2. Process documents and initialize the tool
    docs = load_and_prepare_dataset()
    guest_info_tool = GuestInfoRetrieverTool(docs=docs)

    # 3. Initialize the model and Alfred agent
    print("Initializing Alfred with InferenceClientModel...")
    model = InferenceClientModel()
    alfred = CodeAgent(tools=[guest_info_tool], model=model)

    # 4. Test run interaction
    test_query = "Tell me about our guest named 'Lady Ada Lovelace' and suggest a quick conversation starter."
    print(f"\n🚀 Sending Task to Alfred: '{test_query}'\n")

    response = alfred.run(test_query)

    print("\n🎩 Alfred's Response:")
    print(response)


if __name__ == "__main__":
    main()
