
from pathlib import Path

import chromadb
import requests
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "chroma_db"

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection("medical_knowledge")

    print("Loading embedding model...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    print("\nHealthcare Copilot is ready!")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            query_embedding = embedding_model.encode(
                question,
                normalize_embeddings=True,
            ).tolist()

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(3, collection.count()),
            )

            passages = []
            sources = []

            for document, metadata in zip(
                results["documents"][0],
                results["metadatas"][0],
            ):
                passages.append(
                    f"Title: {metadata['title']}\n"
                    f"Topic: {metadata['topic']}\n"
                    f"Information: {document}"
                )

                source = (
                    metadata["title"],
                    metadata["url"],
                )

                if source not in sources:
                    sources.append(source)

            context = "\n\n---\n\n".join(passages)

            system_prompt = """
You are a cautious healthcare information assistant.

- Explain medical information in simple language.
- Use the supplied medical passages as evidence.
- Do not invent facts, diagnoses, or test results.
- If the passages are insufficient, say so.
- Never claim to diagnose a disease.
- Do not prescribe medicines or dosages.
- Encourage consultation with a qualified clinician
  for personal symptoms and medical decisions.
- For severe chest pain, stroke symptoms, severe
  breathing difficulty, or unconsciousness, advise
  immediate emergency medical care.
- Clearly distinguish general information from
  personal medical advice.
"""

            user_prompt = (
                f"Reference passages:\n{context}\n\n"
                f"User question: {question}\n\n"
                "Answer clearly and mention any limitations."
            )

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    "stream": False,
                    "options": {"temperature": 0.2},
                },
                timeout=180,
            )

            response.raise_for_status()
            answer = response.json()["message"]["content"]

            print(f"\nHealthcare Copilot:\n{answer}\n")
            print("Reference sources:")

            for title, url in sources:
                print(f"- {title}: {url}")

            print("\n" + "=" * 60 + "\n")

        except requests.ConnectionError:
            print("Cannot connect to Ollama. Check that it is running.")

        except requests.Timeout:
            print("The model took too long to respond. Please retry.")

        except requests.RequestException as error:
            print(f"Ollama request failed: {error}")

        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()