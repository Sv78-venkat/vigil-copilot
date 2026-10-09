
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "chroma_db"

def main():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection("medical_knowledge")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    question = input("Enter a medical question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    query_embedding = model.encode(
        question,
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(3, collection.count()),
    )

    print("\nRelevant medical information:\n")

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        print(f"Result {i + 1}: {metadata['title']}")
        print(f"Topic: {metadata['topic']}")
        print(f"Source: {metadata['source']}")
        print(f"URL: {metadata['url']}")
        print(f"Passage: {document}\n")
        print("-" * 60)

if __name__ == "__main__":
    main()