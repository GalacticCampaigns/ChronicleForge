# Choosing Your `dataPath`

The `dataPath` variable in your `campaign-registry.json` is a critical setting that tells the Chronicle Forge exactly **where** to store your synchronized narrative data within your GitHub repository. This guide will help you choose the correct path based on your setup.

---

### 1. What is `dataPath`?
Think of `dataPath` as the "Home Address" for a specific campaign's files inside your repository. The Forge uses this path to save:
* **Narrative JSON**: The actual story text.
* **Media Assets**: Images and attachments from Discord.
* **User Avatars**: The global character portrait cache.

### 2. The Multi-Campaign Isolation Rule
If you are tracking multiple games (campaigns) in the **same repository**, each one must have its own unique `dataPath`.
* **The Risk**: If two campaigns have the same `dataPath`, they will attempt to write over each other, potentially corrupting your story logs.
* **The Fix**: Always include a unique subfolder name for each campaign.

---

### 3. Step-by-Step: Finding Your Path
Follow these steps to determine the correct string for your `dataPath`:

1. **Open your target repository** on GitHub (the one you set in the `repository` field).
2. **Decide on a folder structure**. 
    * If you want your logs in a folder named `archives`, that is your base.
3. **Format the string**: 
    * Start with `./` to indicate the root of the repo.
    * Add your folder names.
    * **Always end with a trailing slash `/`**.

---

### 4. Common Configuration Scenarios

#### Scenario A: Mono-Repo (Engine + Website + Data)
You are using a single repository for everything. You want your data to live in the `public/data/` folder so your website can easily display it.
* **Campaign 1**: `"./public/data/forgotten-ones/"`
* **Campaign 2**: `"./public/data/star-wars-legacy/"`

#### Scenario B: Split-Repo (Dedicated Log Vault)
You have a separate repository just for your story logs. You want each game to have its own folder at the top level.
* **Campaign 1**: `"./forgotten-ones/"`
* **Campaign 2**: `"./star-wars-legacy/"`

#### Scenario C: Single-Game Repository
You have a dedicated repository for only one game and want the data at the very top level.
* **`dataPath` Value**: `"./"`

---

### 5. Final Validation Checklist
Before running your first sync, check your `dataPath` for these three things:
1. **Uniqueness**: Is this folder name different from every other campaign in this repository?
2. **Format**: Does it start with `./` and end with `/`?
3. **Existence**: You do not need to create these folders manually; the Forge will build them for you during the first run.

---
*Developed for the Galactic Campaigns preservation project.*