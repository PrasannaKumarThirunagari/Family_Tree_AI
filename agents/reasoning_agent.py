# agents/reasoning_agent.py

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(
    name="family_memory",
    embedding_function=embedding_function
)

def ingest_documents(docs):
    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc],
            ids=[f"doc_{i}"]
        )

def query_family_question(query_text):
    results = collection.query(query_texts=[query_text], n_results=3)
    retrieved_docs = [doc for doc in results["documents"][0]]

    prompt = (
        "Based on the following information, answer the question:\n\n"
        + "\n".join(retrieved_docs)
        + f"\n\nQuestion: {query_text}\nAnswer:"
    )

    response = os.popen(f'ollama run llama3 "{prompt}"').read()
    return response
