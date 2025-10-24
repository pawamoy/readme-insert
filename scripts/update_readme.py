import os
import sys
from pathlib import Path
from urllib.request import urlopen

MARKUP_URL = os.getenv("MARKUP_URL", "")
FILE_PATH = os.getenv("FILE_PATH", "README.md")
START_MARKER = os.getenv("START_MARKER", "<!-- start-insert -->")
END_MARKER = os.getenv("END_MARKER", "<!-- end-insert -->")


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

    # Find start and end marker lines and replace content between them
    output_lines = []
    inside_markers = False
    found_start = False
    found_end = False

    for line in lines:
        if line.rstrip() == START_MARKER:
            output_lines.append(line)
            output_lines.append(sponsors_markup + "\n")
            inside_markers = True
            found_start = True
        elif line.rstrip() == END_MARKER:
            output_lines.append(line)
            inside_markers = False
            found_end = True
        elif not inside_markers:
            output_lines.append(line)

    if not found_start:
        print(f"Error: Start marker '{START_MARKER}' not found in {FILE_PATH}", file=sys.stderr)
        return

    if not found_end:
        print(f"Error: End marker '{END_MARKER}' not found in {FILE_PATH}", file=sys.stderr)
        return

    filepath.write_text("".join(output_lines), encoding="utf-8")
    print(f"✓ Updated {FILE_PATH} with markup from {MARKUP_URL}")


def main() -> int:
    try:
        update_file()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
