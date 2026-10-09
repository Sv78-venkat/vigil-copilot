
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "medical_sources.json"
DB_DIR = BASE_DIR / "data" / "chroma_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 900
OVERLAP = 150


def split_into_chunks(text):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - OVERLAP

    return chunks


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Medical data is missing. Run fetch_medical_data.py first."
        )

    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    if not records:
        raise ValueError("No medical records found.")

    print("Loading the embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=str(DB_DIR))

    collection = client.get_or_create_collection(
        name="medical_knowledge",
        metadata={
            "description": "MedlinePlus health topic summaries"
        },
    )

    ids = []
    documents = []
    metadatas = []

    for record_number, record in enumerate(records):
        chunks = split_into_chunks(record["summary"])

        for chunk_number, chunk in enumerate(chunks):
            ids.append(
                f"topic_{record_number}_chunk_{chunk_number}"
            )
            documents.append(chunk)

            metadatas.append({
                "topic": record["topic"],
                "title": record["title"],
                "source": record["source"],
                "url": record["url"],
            })

    if not documents:
        raise ValueError("No text chunks were created.")

    print(f"Medical text chunks: {len(documents)}")
    print("Creating embeddings. This may take a while...")

    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()

    for start in range(0, len(documents), 100):
        end = start + 100

        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
            embeddings=embeddings[start:end],
        )

    print("\nKnowledge base built successfully!")
    print(f"Indexed chunks: {collection.count()}")
    print(f"Database location: {DB_DIR}")


if __name__ == "__main__":
    main()