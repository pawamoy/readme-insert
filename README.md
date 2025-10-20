# README Sponsors

A GitHub Action that fetches sponsors markup from a URL and inserts it into a file, automatically creating a pull request when changes are detected.

## Features

- 🔄 **Simple**: Fetches markup from any URL and inserts it into your file
- 🎯 **Smart**: Only creates PRs when content actually changes
- 🚀 **Zero dependencies**: Uses only Python standard library
- 🔒 **No secrets needed**: Works with the built-in `GITHUB_TOKEN`
- ⚡ **Fast**: Minimal overhead, no package installation required

## Usage

### Basic Example

Add this workflow to your repository (e.g., `.github/workflows/update-sponsors.yml`):

```yaml
name: Update Sponsors

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:      # Manual trigger

permissions:
  contents: write
  pull-requests: write

jobs:
  update-sponsors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update sponsors
        uses: pawamoy/readme-sponsors@main
        with:
          markup-url: 'https://your-domain.com/sponsors.html'
```

### Advanced Example

Customize all options:

```yaml
jobs:
  update-sponsors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update SPONSORS.md
        uses: pawamoy/readme-sponsors@main
        with:
          markup-url: 'https://example.com/sponsors-fragment.html'
          file-path: 'SPONSORS.md'
          marker-line: '<!-- insert-sponsors -->'
          branch-name: 'automated/update-sponsors'
          base-branch: 'main'
          commit-message: 'chore: Update sponsors list'
          pr-title: '🎉 Update Sponsors'
          pr-body: |
            Automated sponsors list update.

            Please review and merge if everything looks correct.
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `markup-url` | URL to fetch the sponsors markup content from | ✅ Yes | - |
| `file-path` | Path to the file to update | No | `README.md` |
| `marker-line` | Marker line in the file where sponsors content will be inserted | No | `## Sponsors` |
| `branch-name` | Name of the branch to create for the PR | No | `update-readme-sponsors` |
| `commit-message` | Commit message for the changes | No | `chore: Update sponsors` |
| `pr-title` | Title for the pull request | No | `chore: Update sponsors` |
| `pr-body` | Body text for the pull request | No | `Sponsors updated automatically.` |
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

### 3. Marker Line in File

Your target file must contain the marker line **at the end of the file**. We don't currently support inserting contents in the middle of a file. The action only rewrites contents from the marker line up to the end of the file.

**Example `README.md`:**

```markdown
# My Awesome Project

Description of your project here.

## Sponsors
```

After the action runs, it becomes:

```markdown
# My Awesome Project

Description of your project here.

## Sponsors

<div>Your sponsors markup here</div>
```

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

## Generating Sponsors Content

You can generate the sponsors markup however you prefer:

- **Static file**: Host on GitHub Pages, GitLab Pages, etc.
- **API endpoint**: Build a serverless function that queries GitHub Sponsors API
- **Separate workflow**: Use another action to generate and host the file
- **External service**: Use a third-party service

The action simply fetches from the URL. You control how that content is created.

## Local Testing

Test the script locally:

```bash
export MARKUP_URL="https://your-domain.com/sponsors.html"
export FILE_PATH="README.md"
export MARKER_LINE="## Sponsors"

python3 scripts/update_readme.py
```

Check the changes:

```bash
git diff README.md
```

## Troubleshooting

### Marker line not found

**Error:** `Warning: Marker line '## Sponsors' not found in README.md`

**Solution:** Ensure your file contains the exact marker line (case-sensitive).

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

<!-- sponsors -->
