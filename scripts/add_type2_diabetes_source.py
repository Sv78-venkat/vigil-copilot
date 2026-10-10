
import json
import shutil
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "medical_sources.json"
URL = "https://medlineplus.gov/diabetestype2.html"


def main():
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    if any(record.get("url") == URL for record in records):
        print("Source already exists. No changes made.")
        return

    print("Downloading the official MedlinePlus page...")

    response = requests.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "HealthcareCopilotEducationalProject/1.0"
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup.select(
        "script, style, nav, footer, header, aside, "
        "form, noscript"
    ):
        element.decompose()

    content = soup.find("main") or soup.find("article") or soup.body

    if content is None:
        raise ValueError("Could not find the medical page content.")

    summary = content.get_text(separator="\n", strip=True)

    if len(summary) < 500:
        raise ValueError(
            "Downloaded page is unexpectedly short. "
            "The original source file has not been changed."
        )

    backup = DATA_FILE.with_name(
        "medical_sources_backup_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".json"
    )
    shutil.copy2(DATA_FILE, backup)

    records.append({
        "topic": "type 2 diabetes",
        "title": "Type 2 Diabetes",
        "source": "MedlinePlus",
        "url": URL,
        "summary": summary,
    })

    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nSource added successfully!")
    print("Total sources:", len(records))
    print("Extracted characters:", len(summary))
    print("Backup created:", backup)


if __name__ == "__main__":
    main()
