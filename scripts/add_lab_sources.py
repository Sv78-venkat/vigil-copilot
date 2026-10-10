
import json
import re
import time
from pathlib import Path
from html.parser import HTMLParser

import requests

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "medical_sources.json"

SOURCES = [
    {
        "topic": "HbA1c test",
        "title": "Hemoglobin A1C (HbA1c) Test",
        "url": "https://medlineplus.gov/lab-tests/hemoglobin-a1c-hba1c-test/",
    },
    {
        "topic": "complete blood count",
        "title": "Complete Blood Count (CBC)",
        "url": "https://medlineplus.gov/lab-tests/complete-blood-count-cbc/",
    },
    {
        "topic": "blood testing",
        "title": "What You Need to Know About Blood Testing",
        "url": "https://medlineplus.gov/lab-tests/what-you-need-to-know-about-blood-testing/",
    },
]


class MedicalPageParser(HTMLParser):
    """Extract readable text from a page's main content."""

    SKIP_TAGS = {
        "script", "style", "nav", "footer", "header",
        "noscript", "svg"
    }

    BLOCK_TAGS = {
        "p", "div", "section", "article", "main", "h1",
        "h2", "h3", "h4", "li", "br", "tr"
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main_depth = 0
        self.skip_depth = 0
        self.main_parts = []
        self.all_parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if tag in {"main", "article"}:
            self.main_depth += 1

        if tag in self.BLOCK_TAGS:
            self.all_parts.append(" ")
            if self.main_depth > 0:
                self.main_parts.append(" ")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1
            return

        if tag in {"main", "article"} and self.main_depth > 0:
            self.main_depth -= 1

        if tag in self.BLOCK_TAGS:
            self.all_parts.append(" ")
            if self.main_depth > 0:
                self.main_parts.append(" ")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return

        self.all_parts.append(data)
        if self.main_depth > 0:
            self.main_parts.append(data)

    def get_text(self):
        main_text = " ".join(self.main_parts)
        all_text = " ".join(self.all_parts)

        def clean(text):
            text = re.sub(r"\s+", " ", text)
            return text.strip()

        main_text = clean(main_text)
        all_text = clean(all_text)

        # Prefer the main content. Fall back if the site layout changes.
        if len(main_text) >= 500:
            return main_text
        return all_text


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find existing medical data: {DATA_FILE}"
        )

    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    if not isinstance(records, list):
        raise ValueError("medical_sources.json must contain a JSON list.")

    existing_urls = {
        record.get("url", "").rstrip("/")
        for record in records
        if isinstance(record, dict)
    }

    added = 0
    failed = 0

    headers = {
        "User-Agent": "MedicalKnowledgeCopilot/1.0 (educational project)"
    }

    with requests.Session() as session:
        session.headers.update(headers)

        for source in SOURCES:
            url = source["url"]
            print(f"\nDownloading: {source['title']}")

            if url.rstrip("/") in existing_urls:
                print("  Already present; skipping duplicate.")
                continue

            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()

                parser = MedicalPageParser()
                parser.feed(response.text)
                summary = parser.get_text()

                if len(summary) < 500:
                    raise ValueError(
                        "Not enough readable page text was extracted."
                    )

                record = {
                    "topic": source["topic"],
                    "title": source["title"],
                    "url": url,
                    "summary": summary,
                    "source": (
                        "MedlinePlus, U.S. National Library of Medicine"
                    ),
                    "retrieved_at": time.strftime(
                        "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                    ),
                }

                records.append(record)
                existing_urls.add(url.rstrip("/"))
                added += 1

                print(f"  Extracted {len(summary)} characters.")
                print("  Source added successfully.")

            except (requests.RequestException, ValueError) as error:
                failed += 1
                print(f"  Could not add this source: {error}")

            time.sleep(1)

    # Preserve every existing record and add only successful downloads.
    DATA_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n========== SUMMARY ==========")
    print(f"New sources added: {added}")
    print(f"Sources that failed: {failed}")
    print(f"Total records now: {len(records)}")
    print(f"Saved to: {DATA_FILE}")

    if added == 0 and failed > 0:
        print(
            "No new sources were added. Existing records were preserved; "
            "check your internet connection and try again."
        )

if __name__ == "__main__":
    main()