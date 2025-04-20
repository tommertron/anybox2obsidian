# 📚 Anybox to Obsidian Markdown Exporter

This script converts a JSON export from [Anybox](https://anybox.app/) into individual `.md` files formatted for use with Obsidian.

Each bookmark becomes its own Markdown file, complete with:

- YAML frontmatter (`title`, `url`, `dateAdded`, `description`, `tags`)
- Tags with spaces automatically converted to hyphenated form (e.g. `"video games"` → `video-games`)
- An Obsidian-style callout showing the added date and any personal comment
- Obsidian-friendly date linking (`[[YYYY-MM-DD]]`) for backlinking from daily notes

## 🔧 How to Use

1. Export your bookmarks from Anybox to a `.json` file.
2. Run the script using Python 3, passing the input and output folders as arguments:

   ```bash
   python3 anybox2obsidian.py --input path/to/anybox_export.json --output path/to/output/folder