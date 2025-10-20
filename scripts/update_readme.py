import os
import sys
from pathlib import Path
from urllib.request import urlopen

MARKUP_URL = os.getenv("MARKUP_URL", "")
FILE_PATH = os.getenv("FILE_PATH", "README.md")
MARKER_LINE = os.getenv("MARKER_LINE", "## Sponsors")


def fetch_sponsors_markup() -> str:
    with urlopen(MARKUP_URL) as response:
        return response.read().decode("utf8")


def update_file() -> None:
    filepath = Path(FILE_PATH)

    if not filepath.exists():
        print(f"Error: File {FILE_PATH} not found", file=sys.stderr)
        return

    sponsors_markup = fetch_sponsors_markup()
    content = filepath.read_text(encoding="utf8")
    lines = content.splitlines(keepends=True)

    # Find marker line and insert sponsors markup after it
    output_lines = []
    found_marker = False

    for line in lines:
        output_lines.append(line)
        if line.rstrip() == MARKER_LINE and not found_marker:
            output_lines.append("\n" + sponsors_markup + "\n")
            found_marker = True

    if not found_marker:
        print(f"Warning: Marker line '{MARKER_LINE}' not found in {FILE_PATH}", file=sys.stderr)
        return

    filepath.write_text("".join(output_lines), encoding="utf-8")
    print(f"✓ Updated {FILE_PATH} with sponsors from {MARKUP_URL}")


def main() -> int:
    try:
        update_file()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
