# tools.py
from langchain_community.retrievers import BM25Retriever
from smolagents import Tool


class GuestInfoRetrieverTool(Tool):
    name = "guest_info_retriever"
    description = (
        "Retrieves detailed information about gala guests based on their name or relation. "
        "Use this to find emails, background bios, and relevant details to plan conversation starters."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "The name or relation of the guest you want information about.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(docs)

    def forward(self, query: str) -> str:
        results = self.retriever.invoke(query)
        if results:
            # Returns top 3 matches grouped cleanly
            return "\n\n".join([doc.page_content for doc in results[:3]])
        else:
            return "No matching guest information found."
