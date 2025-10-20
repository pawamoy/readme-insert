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


<div id="premium-sponsors" style="text-align: center;">

<div id="silver-sponsors"><b>Silver sponsors</b><p>
<a href="https://squidfunk.github.io/mkdocs-material/"><img alt="Material for MkDocs" src="https://raw.githubusercontent.com/squidfunk/mkdocs-material/master/.github/assets/logo.svg" style="height: 320px; "></a><br>
<a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/img/logo-margin/logo-teal.png" style="height: 200px; "></a><br>
<a href="https://docs.pydantic.dev/latest/"><img alt="Pydantic" src="https://pydantic.dev/assets/for-external/pydantic_logfire_logo_endorsed_lithium_rgb.svg" style="height: 180px; "></a><br>
</p></div>

<div id="bronze-sponsors"><b>Bronze sponsors</b><p>
<a href="https://www.nixtla.io/"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.nixtla.io/img/logo/full-black.svg"><source media="(prefers-color-scheme: dark)" srcset="https://www.nixtla.io/img/logo/full-white.svg"><img alt="Nixtla" src="https://www.nixtla.io/img/logo/full-black.svg" style="height: 60px; "></picture></a><br>
</p></div>
</div>

---

<div id="sponsors"><p>
<a href="https://github.com/ofek"><img alt="ofek" src="https://avatars.githubusercontent.com/u/9677399?u=386c330f212ce467ce7119d9615c75d0e9b9f1ce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/samuelcolvin"><img alt="samuelcolvin" src="https://avatars.githubusercontent.com/u/4039449?u=42eb3b833047c8c4b4f647a031eaef148c16d93f&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/tlambert03"><img alt="tlambert03" src="https://avatars.githubusercontent.com/u/1609449?u=922abf0524b47739b37095e553c99488814b05db&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ssbarnea"><img alt="ssbarnea" src="https://avatars.githubusercontent.com/u/102495?u=c7bd9ddf127785286fc939dd18cb02db0a453bce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/femtomc"><img alt="femtomc" src="https://avatars.githubusercontent.com/u/34410036?u=f13a71daf2a9f0d2da189beaa94250daa629e2d8&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmarqu"><img alt="cmarqu" src="https://avatars.githubusercontent.com/u/360986?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/kolenaIO"><img alt="kolenaIO" src="https://avatars.githubusercontent.com/u/77010818?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ramnes"><img alt="ramnes" src="https://avatars.githubusercontent.com/u/835072?u=3fca03c3ba0051e2eb652b1def2188a94d1e1dc2&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/machow"><img alt="machow" src="https://avatars.githubusercontent.com/u/2574498?u=c41e3d2f758a05102d8075e38d67b9c17d4189d7&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/BenHammersley"><img alt="BenHammersley" src="https://avatars.githubusercontent.com/u/99436?u=4499a7b507541045222ee28ae122dbe3c8d08ab5&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/trevorWieland"><img alt="trevorWieland" src="https://avatars.githubusercontent.com/u/28811461?u=74cc0e3756c1d4e3d66b5c396e1d131ea8a10472&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/laenan8466"><img alt="laenan8466" src="https://avatars.githubusercontent.com/u/21331242?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/MarcoGorelli"><img alt="MarcoGorelli" src="https://avatars.githubusercontent.com/u/33491632?u=7de3a749cac76a60baca9777baf71d043a4f884d&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/analog-cbarber"><img alt="analog-cbarber" src="https://avatars.githubusercontent.com/u/7408243?u=642fc2bdcc9904089c62fe5aec4e03ace32da67d&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/OdinManiac"><img alt="OdinManiac" src="https://avatars.githubusercontent.com/u/22727172?u=36ab20970f7f52ae8e7eb67b7fcf491fee01ac22&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rstudio-sponsorship"><img alt="rstudio-sponsorship" src="https://avatars.githubusercontent.com/u/58949051?u=0c471515dd18111be30dfb7669ed5e778970959b&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/schlich"><img alt="schlich" src="https://avatars.githubusercontent.com/u/21191435?u=6f1240adb68f21614d809ae52d66509f46b1e877&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/SuperCowPowers"><img alt="SuperCowPowers" src="https://avatars.githubusercontent.com/u/6900187?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/butterlyn"><img alt="butterlyn" src="https://avatars.githubusercontent.com/u/53323535?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/livingbio"><img alt="livingbio" src="https://avatars.githubusercontent.com/u/10329983?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/NemetschekAllplan"><img alt="NemetschekAllplan" src="https://avatars.githubusercontent.com/u/912034?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/EricJayHartman"><img alt="EricJayHartman" src="https://avatars.githubusercontent.com/u/9259499?u=7e58cc7ec0cd3e85b27aec33656aa0f6612706dd&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/15r10nk"><img alt="15r10nk" src="https://avatars.githubusercontent.com/u/44680962?u=f04826446ff165742efa81e314bd03bf1724d50e&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cdwilson"><img alt="cdwilson" src="https://avatars.githubusercontent.com/u/14631?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/activeloopai"><img alt="activeloopai" src="https://avatars.githubusercontent.com/u/34816118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/roboflow"><img alt="roboflow" src="https://avatars.githubusercontent.com/u/53104118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/wrath-codes"><img alt="wrath-codes" src="https://avatars.githubusercontent.com/u/90050913?u=b26582409dfff8ce2b60016fd119be09309708da&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/leodevian"><img alt="leodevian" src="https://avatars.githubusercontent.com/u/167141781?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmclaughlin"><img alt="cmclaughlin" src="https://avatars.githubusercontent.com/u/1061109?u=ddf6eec0edd2d11c980f8c3aa96e3d044d4e0468&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/blaisep"><img alt="blaisep" src="https://avatars.githubusercontent.com/u/254456?u=97d584b7c0a6faf583aa59975df4f993f671d121&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/RapidataAI"><img alt="RapidataAI" src="https://avatars.githubusercontent.com/u/104209891?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rodolphebarbanneau"><img alt="rodolphebarbanneau" src="https://avatars.githubusercontent.com/u/46493454?u=6c405452a40c231cdf0b68e97544e07ee956a733&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/theSymbolSyndicate"><img alt="theSymbolSyndicate" src="https://avatars.githubusercontent.com/u/111542255?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/blakeNaccarato"><img alt="blakeNaccarato" src="https://avatars.githubusercontent.com/u/20692450?u=bb919218be30cfa994514f4cf39bb2f7cf952df4&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ChargeStorm"><img alt="ChargeStorm" src="https://avatars.githubusercontent.com/u/26000165?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/Alphadelta14"><img alt="Alphadelta14" src="https://avatars.githubusercontent.com/u/480845?v=4" style="height: 32px; border-radius: 100%;"></a>
</p></div>


*And 8 more private sponsor(s).*

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
