# 🌐 Web Gallery Setup Guide

This guide explains how to configure and deploy the integrated Web Gallery for your ChronicleForge instance. The gallery is a customizable Jekyll (GitHub Pages) site that reads directly from your `campaign-registry.json`.

---

## 1. Customize Your Branding
Before deploying, you should update the site's metadata to match your group.

Open the `_config.yml` file in the root of the repository and update the following lines:
```yaml
title: "Your Chronicle Hub"
description: "A centralized repository for our roleplay campaigns."
url: "https://yourusername.github.io/your-repo-name" # Set this after enabling GitHub Pages
```

### Replace the Logos
By default, the gallery looks for two images in the `assets/` folder:
1. `logo.png` (Used in the navigation bar)
2. `gc_banner.png` (Used as the default hero image if a campaign doesn't specify one)

Simply overwrite these files with your own PNG images using the exact same filenames.

---

## 2. Configure the Registry
The website dynamically loads narratives based on the `assets/campaign-registry.json` file. 

Open `assets/campaign-registry.json` and fill out your first campaign details. It starts with a template:
```json
{
  "campaigns": {
    "your-campaign-slug": {
      "name": "My Epic Campaign",
      "guild_id": "123456789012345678",
      "category_id": "123456789012345678",
      "auto_scan_pattern": "ch|chapter|prelude",
      "repository": "self",
      "branch": "main",
      "dataPath": "./vault/your-campaign-slug",
      "paths": {
        "json": "json/",
        "media": "media/",
        "avatars": "avatars/",
        "emoji": "emoji/",
        "wiki": ""
      },
      "logs": []
    }
  }
}
```
* **Note:** As long as `repository` is set to `"self"`, the gallery will know to look inside its own repository's `vault/` folder for the JSON logs!

---

## 3. Deploy via GitHub Pages
Because the website code is integrated directly into the Forge, deployment is simple:

1. Push all your changes (including your customized `_config.yml` and `campaign-registry.json`) to your GitHub repository.
2. On GitHub, navigate to your repository **Settings**.
3. Click on **Pages** in the left sidebar.
4. Under **Build and deployment > Source**, select **Deploy from a branch**.
5. Select `main` (or your default branch) and `/ (root)`.
6. Click **Save**.

GitHub will now build your site. Once complete, you will receive a URL (e.g., `https://username.github.io/repo-name`). 
*Don't forget to update the `url` variable in your `_config.yml` with this new link!*

---

## 4. Run the Forge!
Now that the gallery is deployed, you can use the Forge to pull your Discord logs.

Run the standard Miner command:
```bash
python3 -m scripts.pull_logs
```
The engine will mine the channels, convert the JSON, save it to `vault/`, update the `assets/campaign-registry.json`, and push it all to GitHub. Within 60 seconds, your Web Gallery will automatically refresh and display your new chapters!
