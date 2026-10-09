
import json
import re
import html
import time
from pathlib import Path
import xml.etree.ElementTree as ET

import requests

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "medical_sources.json"

API_URL = "https://wsearch.nlm.nih.gov/ws/query"

TOPICS = [
    "diabetes",
    "high blood pressure",
    "asthma",
    "anemia",
    "dengue",
    "malaria",
    "heart attack",
    "stroke",
    "kidney disease",
    "nutrition",
]

def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    seen_urls = set()

    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "LocalHealthcareCopilot/0.1"
        })

        for topic in TOPICS:
            print(f"\nSearching MedlinePlus: {topic}")

            try:
                response = session.get(
                    API_URL,
                    params={
                        "db": "healthTopics",
                        "term": topic,
                        "rettype": "brief",
                        "tool": "LocalHealthcareCopilot",
                    },
                    timeout=30,
                )
                response.raise_for_status()
                root = ET.fromstring(response.content)

                documents = root.findall(".//document")
                saved = False

                for document in documents:
                    url = document.attrib.get("url", "").strip()

                    # Read title and summary from XML content elements.
                    fields = {}
                    for content in document.findall("./content"):
                        name = content.attrib.get("name", "").lower()
                        value = "".join(content.itertext())
                        fields.setdefault(name, []).append(value)

                    title = clean_text(
                        " ".join(fields.get("title", []))
                    )
                    summary = clean_text(
                        " ".join(fields.get("fullsummary", []))
                    )

                    if not title or not summary or not url:
                        continue

                    if not url.startswith("https://medlineplus.gov/"):
                        continue

                    if url in seen_urls:
                        saved = True
                        break

                    records.append({
                        "topic": topic,
                        "title": title,
                        "url": url,
                        "summary": summary,
                        "source": "MedlinePlus, U.S. National Library of Medicine",
                        "retrieved_at": time.strftime(
                            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                        ),
                    })

                    seen_urls.add(url)
                    print(f"  Saved: {title}")
                    saved = True
                    break

                if not saved:
                    print("  No complete matching record found.")

            except requests.RequestException as error:
                print(f"  Request failed: {error}")
            except ET.ParseError as error:
                print(f"  XML parsing failed: {error}")

            time.sleep(1.5)

    OUTPUT_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nRecords downloaded: {len(records)}")
    print(f"Output: {OUTPUT_FILE}")

    if not records:
        print("No records downloaded. Inspect the API response.")
    else:
        print("Download complete. Verify the data before indexing.")

if __name__ == "__main__":
    main()