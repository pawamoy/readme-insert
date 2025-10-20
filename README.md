# README Sponsors

A GitHub Action that updates `README.md` to list sponsors.

It will open a PR if the README changed.

## Usage

### Basic Example

Create a workflow file (e.g., `.github/workflows/update-readme.yml`) in your repository:

```yaml
name: Update README

on:
  schedule:
    # Run every day at midnight UTC
    - cron: '0 0 * * *'
  workflow_dispatch: # Allow manual triggers

permissions:
  contents: write
  pull-requests: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Update README and create PR
        uses: pawamoy/readme-sponsors@main
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `logo-data-source` | URL or local file path to JSON file containing logo data for sponsors | No | `''` (empty) |
| `file-path` | Path to the file to update | No | `README.md` |
| `marker-line` | Marker line in the file where sponsors content should be inserted | No | `## Sponsors` |
| `branch-name` | Name of the branch to create for the PR | No | `update-readme-sponsors` |
| `base-branch` | Base branch to target for the PR | No | `main` |
| `commit-message` | Commit message for the changes | No | `chore: Update sponsors list` |
| `pr-title` | Title for the pull request | No | `chore: Automated spsonsors update` |
| `pr-body` | Body text for the pull request | No | `''` (empty) |

## Example

```yaml
jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Update README and create PR
        uses: pawamoy/readme-sponsors@main
        with:
            logo-data-source: https://pawamoy.github.io/sponsors-logo.json
            file-path: SPONSORS.md
            marker-line: "<!-- Insert sponsors here -->"
            branch-name: chore/update-readme
            base-branch: master
            commit-message: Update SPONSORS.md
            pr-title: Update sponsors
            pr-body: The sponsor list is now updated.
```

## Requirements

### Permissions

Your workflow **must** include these permissions:

```yaml
permissions:
  contents: write        # To push changes
  pull-requests: write   # To create PRs
```

### Logo Data Format

The `logo-data-source` input accepts either a URL or local file path to a JSON file containing sponsor logo information. The JSON format should be:

```json
{
  "sponsor-username": {
    "name": "Sponsor Display Name",
    "url": "https://sponsor-website.com",
    "logo": "https://example.com/logo.svg",
    "height": 200
  }
}
```

For sponsors with dark/light mode logos, use an array:

```json
{
  "sponsor-username": {
    "name": "Sponsor Name",
    "url": "https://sponsor-website.com",
    "logo": [
      "https://example.com/logo-light.svg",
      "https://example.com/logo-dark.svg"
    ],
    "height": 60
  }
}
```

**Fields:**
- `name`: Display name for the sponsor
- `url`: Website URL to link to
- `logo`: Logo image URL (string) or [light, dark] array for theme-aware logos
- `height`: Logo height in pixels

If no logo data is provided for a sponsor, their profile image will be used instead.

### Dependencies

The action uses [`uv`](https://docs.astral.sh/uv/) to run the Python script with inline dependency declarations (PEP 723). The script includes its dependencies in a special comment block at the top:

```python
# /// script
# dependencies = [
#   "insiders",
# ]
# ///
```

### Authentication

The action uses `github.token` (automatically provided by GitHub Actions) for authentication with the `gh` CLI. No additional secrets are required.

## How It Works

1. Installs `uv` (Python package manager)
2. Runs Python script with `uv run` (automatically installs inline dependencies)
3. Checks if the target file has changes using `git diff`
4. If changes exist:
   - Creates a new branch
   - Commits the changes
   - Pushes the branch
   - Creates a PR using `gh pr create`
