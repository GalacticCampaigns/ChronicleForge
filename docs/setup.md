This guide details the setup for the **Chronicle Forge**, an automated archival engine designed to preserve Discord roleplay narratives in a permanent, system-agnostic format.

---

# ⚒️ Chronicle Forge Setup Guide

The Chronicle Forge supports two primary deployment architectures:
1.  **Mono-Repo (Unified):** Code, Website UI, and Narrative Data live in a single repository fork.
2.  **Split-Repo (Distributed):** The Forge engine is separate from your existing Website and Campaign repositories.

## Part 1: Discord Bot Foundation
The Forge requires a dedicated Discord Bot to act as its "eyes" and download assets.

1.  **Create Application:** Open the [Discord Developer Portal](https://discord.com/developers/applications) and create a **New Application**.
2.  **Generate Token:** In the **Bot** tab, click **Reset Token** and save your `DISCORD_TOKEN`.
3.  **Required Gateway Intents:** You **MUST** enable these three switches:
    * **Presence Intent**.
    * **Server Members Intent** (Required for processing user avatars).
    * **Message Content Intent** (Required to read the story).
4.  **Invite Bot:** Under **OAuth2** > **URL Generator**, select `bot` and `Administrator` (or `Read Message History` + `View Channels`) and use the generated link to invite the bot to your server.

---

## Part 2: Choose Your Architecture

### Scenario A: Mono-Repo (Recommended)
*Use this if you want a single "all-in-one" fork that contains your engine, your data, and your gallery.*

1.  **Fork the Project:** Fork the main **ChronicleForge** repository to your GitHub account.
2.  **Configure Secrets:** Add `DISCORD_TOKEN` to your GitHub repository secrets.
3.  **Set Website Target:** In your `.env` or Secrets, set `WEBSITE_REPO="self"`.
4.  **Local Data Path:** In your `campaign-registry.json`, set the `dataPath` to a subfolder within the repo (e.g., `./public/data/`).

### Scenario B: Split-Repo
*Use this if you already have separate repositories for your Website and Campaign logs.*

1.  **Prepare Destination Repos:** Ensure you have repositories ready for your **Website** and each **Campaign**.
2.  **Configure Secrets:** * `DISCORD_TOKEN`: Your bot token.
    * `WEBSITE_REPO`: Shorthand for your website repo (e.g., `User/my-site`).
    * `REGISTRY_URL`: The Raw GitHub URL to your `campaign-registry.json`.
3.  **SSH Aliasing (Local/Pi Only):** If running on hardware, update `~/.ssh/config` with aliases matching your `refinery-config.json`.

---

## Part 3: Engine Configuration (`refinery-config.json`)
Create this file in the project root to control Forge logic without editing code.

```json
{
  "scout": {
    "auto_scan_pattern": "ch|chapter|prelude",
    "ignore_keywords": ["ooc", "gm", "staff", "test"],
    "forum_is_chapter": true
  },
  "refinery": {
    "truncation_limit": 100,
    "content_scan_version": 4
  },
  "forensics": {
    "nsfw_threshold": 0.90,
    "nsfw_keywords": ["nsfw", "🔞", "underage", "18+"],
    "narrative_types": [0, 19, 21]
  },
  "git_aliases": {
    "YourGitHubUser": "github.com-alias"
  }
}
```

### `scout`: Discovery & Filtering
The Scout determines which Discord channels and threads are worthy of being mined. Its primary job is to separate "In-Character" (IC) storytelling from "Out-of-Character" (OOC) chatter.

* **`auto_scan_pattern`**: A Regular Expression (regex) string. The Scout looks at every channel name in your target category; if the name matches this pattern (e.g., `ch5` or `prelude-wes`), it is added to the registry.
* **`ignore_keywords`**: A safety list. If a channel name contains any of these words (like `ooc` or `staff`), the Scout will mark it as `isActive: false` in your registry, ensuring private or non-narrative data is never accidentally made public.
* **`forum_is_chapter`**: A boolean (`true`/`false`). When enabled, individual threads within a Forum Channel are treated as standalone Chapters rather than just threads within a Chapter.

### `refinery`: Data Hygiene & System Safety
This section handles the "Gold Standard" conversion, ensuring the data is clean, consistent, and safe for all operating systems.

* **`truncation_limit`**: **(Pillar 3 Compatibility)** Sets the maximum character length for filenames (default `100`). This prevents the Pi or Linux nodes from throwing "Filename too long" errors when dealing with long Discord attachment names.
* **`content_scan_version`**: An internal version tracker. If the Forge updates its markdown parsing logic in the future, increasing this number can trigger a re-scan of older files.
* **`standard_discriminator`**: Discord moved away from #0000 discriminators, but the Forge uses this to keep the author objects uniform in your JSON database.

### `forensics`: Narrative Accuracy & Safety
Forensics analyzes the *content* of the messages to determine the "vibe" and safety level of the chapter.

* **`nsfw_threshold`**: (Default `0.90`) This is a percentage. If 90% of the messages in a channel contain NSFW reactions or keywords, the Forge automatically flips the `isNSFW` flag to `true` in the registry. 
    * *Note: This follows the "Sticky True" rule—the engine can turn the flag ON, but only a human can turn it back OFF.*
* **`nsfw_keywords`**: A list of emojis or words that trigger the safety counter.
* **`narrative_types`**: Defines which Discord message integers count as "Story."
    * `0`: Default text.
    * `19`: Replies.
    * `21`: Thread Starter messages.
    * *System messages (joins, pins, boosts) are ignored to keep the chronicle cinematic.*

### `git_aliases`: Identity Abstraction
This is crucial for **Pillar 4 (Portability)**. It allows the Forge to manage multiple GitHub accounts on a single machine (like your Pi) using SSH keys.

* **The Mapping**: You map your GitHub username (the owner of the repo) to an SSH alias defined in your `~/.ssh/config`.
* **Example**: If your owner is `GalacticCampaigns`, the Forge looks here to see it should use `github.com-alicia86` to authenticate the push.
* **Cloud Mode**: When running in **GitHub Codespaces**, the Forge automatically ignores these aliases and uses standard HTTPS/Token auth, making the settings "Environment Aware."

---

### Summary of Configuration Impact

| Setting Section | Primary Goal | User Impact |
| :--- | :--- | :--- |
| **Scout** | Automation | You don't have to manually add new chapters. |
| **Refinery** | System Safety | Prevents "Filename too long" errors on your Pi. |
| **Forensics** | Quality Control | Automatically blurs mature content for the web. |
| **Git Aliases** | Permissions | Handles multiple GitHub accounts automatically. |

---

## Part 4: The Brain (`campaign-registry.json`)
Initialize your registry file. The Forge will "Self-Heal" missing keys automatically during the first run.

```json
{
  "campaigns": {
    "my-campaign": {
      "name": "My Epic RP",
      "guild_id": "123456789...",
      "category_id": "987654321...",
      "repository": "self",
      "branch": "main",
      "dataPath": "./vault/my-campaign",
      "paths": { "json": "json/", "media": "media/", "avatars": "avatars/" },
      "logs": []
    }
  }
}
```
* **`repository`**: Set to `"self"` for Mono-Repo or `User/repo-name` for Split-Repo.
* **`dataPath`**: The relative folder where narrative JSON and media will be "Deep Frozen".

---

## Part 5: Operation
The Forge detects if it is in the **CLOUD** (Codespaces) or **LOCAL** (Pi/Linux) and adjusts permissions accordingly.

### 1. Discovery (The Scout)
Populate your registry with new channels and threads:
```bash
python3 -m scripts.pull_logs -d
```

### 2. Full Sync (The Deep Freeze)
Mine the history, mirror all assets to the Vault, and push to GitHub:
```bash
python3 -m scripts.pull_logs
```

### 3. Forensic Audit
Force a re-scan of existing "Gold" JSON to update message counts or safety labels:
```bash
python3 -m scripts.pull_logs -f
```

---
*Developed for the Galactic Campaigns preservation project.*