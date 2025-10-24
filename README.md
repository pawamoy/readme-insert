# README Insert

A GitHub Action that fetches markup from a URL and inserts it into a file, automatically creating a pull request when changes are detected.

## Features

- 🔄 **Simple**: Fetches markup from any URL and inserts it into your file
- 🎯 **Smart**: Only creates PRs when content actually changes
- 🚀 **Zero dependencies**: Uses only Python standard library
- 🔒 **No secrets needed**: Works with the built-in `GITHUB_TOKEN`
- ⚡ **Fast**: Minimal overhead, no package installation required

## Usage

### Basic Example

Add this workflow to your repository (e.g., `.github/workflows/update-readme.yml`):

```yaml
name: Update README

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger

permissions:
  contents: write
  pull-requests: write

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update readme
        uses: pawamoy/readme-insert@main
        with:
          markup-url: 'https://your-domain.com/content.html'
```

### Advanced Example

Customize all options:

```yaml
jobs:
  update-content:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update custom file
        uses: pawamoy/readme-insert@main
        with:
          markup-url: 'https://example.com/content-fragment.html'
          file-path: 'CUSTOM.md'
          start-marker: '<!-- content-start -->'
          end-marker: '<!-- content-end -->'
          branch-name: 'automated/update-content'
          base-branch: 'main'
          commit-message: 'chore: Update content'
          pr-title: '🎉 Update Content'
          pr-body: |
            Automated content update.

            Please review and merge if everything looks correct.
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `markup-url` | URL to fetch the markup content from | ✅ Yes | - |
| `file-path` | Path to the file to update | No | `README.md` |
| `start-marker` | Start marker line in the file (content will be inserted after this) | No | `<!-- start-insert -->` |
| `end-marker` | End marker line in the file (content will be inserted before this) | No | `<!-- end-insert -->` |
| `branch-name` | Name of the branch to create for the PR | No | `update-readme` |
| `commit-message` | Commit message for the changes | No | `chore: Update docs` |
| `pr-title` | Title for the pull request | No | `chore: Update docs` |
| `pr-body` | Body text for the pull request | No | `Docs updated automatically.` |
| `base-branch` | Base branch to target for the PR | No | `main` |

## How It Works

1. **Fetch**: Downloads markup content from the specified URL using Python's `urllib`
2. **Insert**: Finds the marker line in your file and inserts the content after it
3. **Detect**: Uses `git diff` to check if the file actually changed
4. **Create PR**: If changes exist, creates a new branch, commits, and opens a PR via `gh` CLI

## Setup Requirements

### 1. Workflow Permissions

Your workflow must have these permissions:

```yaml
permissions:
  contents: write        # To push commits
  pull-requests: write   # To create PRs
```

You must also allow the creation of PRs from GitHub actions in your repository settings, at https://github.com/username/repo/settings/actions.

### 2. Marker Lines in File

Your target file must contain both the start and end marker lines. The content between these markers will be replaced with the fetched markup on each run, while the markers themselves are preserved.

**Example `README.md`:**

```markdown
# My Awesome Project

Description of your project here.

## Dynamic Content

<!-- start-insert -->
<!-- end-insert -->

## Installation

More content here...
```

After the action runs, it becomes:

```markdown
# My Awesome Project

Description of your project here.

## Dynamic Content

<!-- start-insert -->
<div>Your dynamic content here</div>
<!-- end-insert -->

## Installation

More content here...
```

**Key points:**
- Both markers must be present in the file
- Content between the markers is completely replaced on each update
- The markers themselves are preserved, allowing subsequent updates
- You can place the markers anywhere in the file, not just at the end

## Markup Format

The URL you provide should return plain HTML or Markdown. The action doesn't care about the format: it just inserts whatever content it fetches.

**Example HTML:**

```html
<div align="center">
  <a href="https://sponsor1.com">
    <img src="https://sponsor1.com/logo.png" alt="Sponsor 1" height="80">
  </a>
  <a href="https://sponsor2.com">
    <img src="https://sponsor2.com/logo.png" alt="Sponsor 2" height="80">
  </a>
</div>
```

**Example Markdown:**

```markdown
- [Sponsor 1](https://sponsor1.com) - Amazing sponsor
- [Sponsor 2](https://sponsor2.com) - Great supporter
```

## Generating Content

You can generate the markup however you prefer:

- **Static file**: Host on GitHub Pages, GitLab Pages, etc.
- **API endpoint**: Build a serverless function that queries an API
- **Separate workflow**: Use another action to generate and host the file
- **External service**: Use a third-party service

The action simply fetches from the URL. You control how that content is created.

## Local Testing

Test the script locally:

```bash
export MARKUP_URL="https://your-domain.com/content.html"
export FILE_PATH="README.md"
export START_MARKER="<!-- start-insert -->"
export END_MARKER="<!-- end-insert -->"

python3 scripts/update_readme.py
```

Check the changes:

```bash
git diff README.md
```

## Troubleshooting

### Marker not found

**Error:** `Error: Start marker '<!-- start-insert -->' not found in README.md`
**Error:** `Error: End marker '<!-- end-insert -->' not found in README.md`

**Solution:** Ensure your file contains both exact marker lines (case-sensitive).

### URL fetch failed

**Error:** `Error fetching sponsors from URL`

**Solution:**
- Verify the URL is publicly accessible
- Check the URL returns valid content (not a 404/500 error)
- Ensure there are no network/firewall restrictions

### PR already exists

**Message:** `PR may already exist`

**Explanation:** The action will force-push to the same branch if it already exists, updating the existing PR rather than creating a new one.

## License

ISC

## Contributing

Contributions welcome! Feel free to open issues or pull requests.

## Sponsors

<!-- start-insert -->
<!-- end-insert -->
