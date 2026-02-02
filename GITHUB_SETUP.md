# GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name:** `hinen-solar-homeassistant`
   - **Description:** `Home Assistant integration for Hinen solar inverters, battery storage, and PV systems`
   - **Public or Private:** Choose **Public** (for HACS compatibility)
   - **Initialize:** Leave all checkboxes **UNCHECKED** (we already have files)
3. Click **Create repository**

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /c/Users/jc/OneDrive/Documents/Coding/hacs/Solartrack

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/hinen-solar-homeassistant.git

# Push the code
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username!

## Step 3: Add Repository Topics

On your GitHub repository page:
1. Click the ⚙️ (gear icon) next to "About"
2. Add these topics:
   - `home-assistant`
   - `hacs`
   - `homeassistant-integration`
   - `solar`
   - `hinen`
   - `solar-energy`
   - `battery`
   - `inverter`
3. Click **Save changes**

## Step 4: Create the Issue

Once the repository is created, create an issue to track the OAuth bug:

1. Go to your repository's **Issues** tab
2. Click **New issue**
3. Copy the content from `GITHUB_ISSUE_TEMPLATE.md` (created separately)
4. Click **Submit new issue**

## Step 5: Create a Release (After OAuth is Fixed)

When Hinen fixes the OAuth page and you've tested the integration:

```bash
# Tag the release
git tag -a v1.0.0 -m "Initial release - Hinen Solar integration"
git push origin v1.0.0
```

Then on GitHub:
1. Go to **Releases** → **Create a new release**
2. Choose tag `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description: Copy from release notes below
5. Click **Publish release**

## Release Notes Template (for v1.0.0)

```markdown
# Hinen Solar Home Assistant Integration v1.0.0

First stable release of the Hinen Solar integration for Home Assistant!

## Features

- ✅ OAuth2 authentication with automatic token refresh
- ✅ Multi-region support (Europe, Asia-Pacific, Australia)
- ✅ 35 sensors covering PV, battery, grid, and energy statistics
- ✅ 2 binary sensors (online status, battery charging)
- ✅ Energy Dashboard compatible
- ✅ HACS ready

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click ⋮ → "Custom repositories"
4. Add: `https://github.com/YOUR_USERNAME/hinen-solar-homeassistant`
5. Category: "Integration"
6. Click "Download"
7. Restart Home Assistant

### Manual Installation

1. Download `Source code (zip)` from this release
2. Extract to `config/custom_components/hinen/`
3. Restart Home Assistant

## Configuration

See [Quick Start Guide](QUICK_START.md) for detailed setup instructions.

## Known Issues

- See [Issue #1](../../issues/1) - Requires Hinen AU OAuth page fix

## Credits

Developed for the Home Assistant community.
Integration created with Claude AI assistance.
```

## Optional: Enable GitHub Pages (for Documentation)

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **root**
4. Click **Save**

This will make your README available at:
`https://YOUR_USERNAME.github.io/hinen-solar-homeassistant/`

## What's Next?

After pushing to GitHub:
1. Share the repository link with Hinen support (shows you're serious)
2. Wait for OAuth fix
3. Test the integration
4. Create v1.0.0 release
5. Submit to HACS default repository (optional)
6. Share with Home Assistant community

## Repository URL

Your repository will be at:
```
https://github.com/YOUR_USERNAME/hinen-solar-homeassistant
```

Replace `YOUR_USERNAME` with your actual GitHub username!
