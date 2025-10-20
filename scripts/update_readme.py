#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "insiders",
# ]
# ///
from itertools import groupby
import json
import os
from contextlib import nullcontext
from pathlib import Path
from typing import Iterator
from urllib.request import urlopen

from insiders import GitHub, Polar, Sponsors, Sponsorship

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
POLAR_TOKEN = os.getenv("POLAR_TOKEN")
LOGO_DATA_SOURCE = os.getenv("LOGO_DATA_SOURCE", "")
FILE_PATH = os.getenv("FILE_PATH", "README.md")
MARKER_LINE = os.getenv("MARKER_LINE", "## Sponsors")

TIERS = (1000, 500, 200, 100)


def load_logo_data() -> dict:
    if not LOGO_DATA_SOURCE:
        return {}
    if LOGO_DATA_SOURCE.startswith(("http://", "https://")):
        with urlopen(LOGO_DATA_SOURCE) as response:
            return json.loads(response.read().decode("utf8"))
    return json.loads(Path(LOGO_DATA_SOURCE).read_text(encoding="utf8"))


def get_tier(sponsorship: Sponsorship) -> int:
    for amount in TIERS:
        if sponsorship.amount >= amount:
            return amount
    return 0


def html(sponsorship: Sponsorship, logo_data: dict) -> str:
    if sponsorship.account.name in logo_data:
        name = logo_data[sponsorship.account.name]["name"]
        url = logo_data[sponsorship.account.name]["url"]
        image = logo_data[sponsorship.account.name]["logo"]
        height = logo_data[sponsorship.account.name]["height"]
        style = ""
    else:
        name = sponsorship.account.name
        url = sponsorship.account.url
        image = sponsorship.account.image
        height = None
        style = "border-radius: 100%;"
    if not name or not url or not image:
        return ""
    height = height or 32
    if isinstance(image, str):
        return f'<a href="{url}"><img alt="{name}" src="{image}" style="height: {height}px; {style}"></a>'
    return (
        f'<a href="{url}"><picture>'
        f'<source media="(prefers-color-scheme: light)" srcset="{image[0]}">'
        f'<source media="(prefers-color-scheme: dark)" srcset="{image[1]}">'
        f'<img alt="{name}" src="{image[0]}" style="height: {height}px; {style}"></picture>'
        f'</a>'
    )


def list_sponsors() -> Iterator[str]:
    logo_data = load_logo_data()

    github_context = GitHub(GITHUB_TOKEN) if GITHUB_TOKEN else nullcontext()
    polar_context = Polar(POLAR_TOKEN) if POLAR_TOKEN else nullcontext()
    with github_context as github, polar_context as polar:
        sponsors = Sponsors()
        if github:
            sponsors.merge(github.get_sponsors(exclude_private=False))
        if polar:
            sponsors.merge(polar.get_sponsors(exclude_private=False))

    # Sort (sponsorship, tier) by tier descending, then by sponsorship creation date ascending.
    sorted_sponsorships = sorted(((sp, get_tier(sp)) for sp in sponsors.sponsorships), key=lambda x: (-x[1], x[0].created))

    # Group by tier.
    private = 0
    yield '<div id="premium-sponsors" style="text-align: center;">'
    for tier, group in groupby(sorted_sponsorships, key=lambda x: x[1]):
        newline = "\n"
        if tier == 1000:
            yield '\n\n<div id="platinum-sponsors"><b>Platinum sponsors</b><p>\n'
        elif tier == 500:
            yield '\n\n<div id="gold-sponsors"><b>Gold sponsors</b><p>\n'
        elif tier == 200:
            yield '\n\n<div id="silver-sponsors"><b>Silver sponsors</b><p>\n'
        elif tier == 100:
            yield '\n\n<div id="bronze-sponsors"><b>Bronze sponsors</b><p>\n'
        else:
            yield '\n</div>\n\n---\n\n<div id="sponsors"><p>\n'
            newline = ""
        for sponsorship, _ in group:
            if sponsorship.private and sponsorship.account.name not in logo_data:
                private += 1
                continue
            yield html(sponsorship, logo_data) + newline
        yield '\n</p></div>'
    if private:
        yield f"\n\n*And {private} more private sponsor(s).*"


def yield_updated_readme(filepath: Path, marker_line: str) -> Iterator[str]:
    with filepath.open("r", encoding="utf8") as file:
        for line in file:
            yield line
            if line == marker_line:
                yield from list_sponsors()
                break


def update_readme(filepath: Path, marker_line: str) -> None:
    filepath.write_text(
        "".join(yield_updated_readme(filepath, marker_line)),
        encoding="utf8",
    )


def main() -> int:
    update_readme(Path(FILE_PATH), MARKER_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
