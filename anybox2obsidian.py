import json
import os
import re
import argparse
from datetime import datetime
from pathlib import Path

# --- Argument parser setup ---
parser = argparse.ArgumentParser(
    description="Convert an Anybox JSON export into Obsidian-friendly Markdown files."
)
parser.add_argument("--input", required=True, help="Path to the Anybox JSON export file")
parser.add_argument("--output", required=True, help="Folder to save the exported Markdown files")

args = parser.parse_args()

input_file = Path(args.input)
output_dir = Path(args.output)
output_dir.mkdir(parents=True, exist_ok=True)

# --- Load Anybox JSON ---
try:
    with input_file.open("r", encoding="utf-8") as f:
        bookmarks = json.load(f)
except Exception as e:
    print(f"❌ Failed to load JSON: {e}")
    exit(1)

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)[:100]  # Remove illegal chars

for entry in bookmarks:
    title = entry.get("title", "Untitled")
    url = entry.get("url", "")
    date_raw = entry.get("dateAdded", "")[:10]
    date = date_raw if date_raw else datetime.today().strftime("%Y-%m-%d")
    description = entry.get("description", "").strip()
    comment = entry.get("comment", "").strip()

    # Normalize tags and replace spaces with hyphens
    raw_tags = entry.get("tags", [])
    tags = [tag.replace(" ", "-") for group in raw_tags for tag in group]
    tags_list = '\n  - "' + '"\n  - "'.join(tags) + '"' if tags else ""

    # Build Markdown content
    filename = sanitize_filename(title) + ".md"
    callout = f"""> [!info]
> **Added:** [[{date}]]  
> **Comment:**  
"""
    if comment:
        callout += f"> {comment}\n"

    content = f"""---
title: "{title}"
url: "{url}"
dateAdded: {date}
description: "{description}"
tags:{tags_list if tags else ' []'}
---

{callout}"""

    # Write Markdown file
    output_path = output_dir / filename
    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ Exported {len(bookmarks)} markdown files to {output_dir.resolve()}")