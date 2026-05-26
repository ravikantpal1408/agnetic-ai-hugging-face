from pathlib import Path

import chromadb
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai_like import OpenAILike
from llama_index.vector_stores.chroma import ChromaVectorStore

# 1. Global Settings (LLM & Embeddings)
Settings.llm = OpenAILike(
    model="qwen/qwen2.5-vl-7b",
    api_base="http://192.168.1.10:1234/v1",  # Your remote machine's IP
    api_key="not-needed",
    temperature=0,
    is_chat_model=True,
)

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

# 2. Setup Paths & Components
script_dir = Path(__file__).parent

text_splitter = SentenceSplitter(
    chunk_size=512,  # Maximum size of each chunk (in tokens)
    chunk_overlap=50,  # Number of overlapping tokens between chunks
)

# 3. Setup ChromaDB Vector Store
db = chromadb.PersistentClient(path=str(script_dir / "chroma_db"))
chroma_collection = db.get_or_create_collection("nodejs_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# 4. SMART INGESTION: Only process the PDF if ChromaDB is empty
# This saves time and stops duplicate vectors from stacking up!
if chroma_collection.count() == 0:
    print("ChromaDB collection is empty. Starting ingestion pipeline...")

    # Load the specific PDF
    reader = SimpleDirectoryReader(input_files=[script_dir / "nodejs.pdf"])
    documents = reader.load_data()

    # Create and run the pipeline
    pipeline = IngestionPipeline(
        transformations=[text_splitter, embed_model],
        vector_store=vector_store,
    )
    nodes = pipeline.run(documents=documents)
    print(f"Successfully processed and stored {len(nodes)} nodes in ChromaDB!")
else:
    print(
        f"ChromaDB already contains {chroma_collection.count()} vectors. Skipping ingestion."
    )

# 5. Connect LlamaIndex to the vector store to query it
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context,
    embed_model=Settings.embed_model,  # Ensures embeddings match if needed
)

# 6. Test Query
query_engine = index.as_query_engine(llm=Settings.llm)

print("Sending query to remote LM Studio...")
response = query_engine.query("What are the core features of Node.js?")

print("\nResponse from Remote LM Studio:")
print(response)

"""
Your RAG Lifecycle checklist:
1- Parsing & Loading (Done via SimpleDirectoryReader)
2- Chunking & Embedding (Done via IngestionPipeline)
3- Storing (Done via ChromaDB)
4- Querying (Done via VectorStoreIndex Query Engine)
5- Evaluation (Next step: Look into LlamaIndex's 'llama_index.core.evaluation' module)
"""
