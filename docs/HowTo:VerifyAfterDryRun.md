# Verifying Vault Data After a Dry Run

This guide explains how to confirm your narrative files were captured correctly before you commit to a live production sync.

### 1. Understanding the File Hierarchy
The Forge is designed to keep your "Engine" (the code) separate from your "Vault" (the data). 
* **The Engine:** Lives in the `ChronicleForge/` folder.
* **The Vault:** Lives in a folder named `vault/` located **one level above** your code.

Because the `vault/` folder is outside the main repository folder, it will not appear in the standard GitHub "Code" tab on the web. You must view it while your Codespace is active.

---

### 2. Verifying via the Codespace Web Editor (Recommended)
If you are using the default browser-based editor provided by GitHub Codespaces, follow these steps:

1. **Open the Explorer:** Click the "Files" icon (top-left) in the sidebar.
2. **Access the Root:** By default, you only see the `ChronicleForge` folder. To see the Vault:
   * Click **File > Open Folder...** in the top menu.
   * Type `/workspaces/` and press Enter.
3. **Navigate to the Data:** You will now see two main folders:
   * `ChronicleForge/` (Your engine)
   * `vault/` (Your data)
4. **Inspect JSON:** Drill down through `vault/ > [Your-Campaign-Name] > json/`. Click on any `.json` file to verify the narrative content was successfully mined.

---

### 3. Verifying via the Integrated Terminal
If you prefer using commands, or if your sidebar view is restricted, use the terminal at the bottom of your screen:

* **List all captured chapters:**
  ```bash
  ls -R ../vault/
  ```
* **Read a specific chapter's content:**
  ```bash
  cat ../vault/[campaign-slug]/json/[chapter-file].json
  ```
* **Check for media assets:**
  ```bash
  ls ../vault/[campaign-slug]/media/
  ```

---

### 4. Verifying via the GitHub "Code" Tab (Web UI Only)
During a dry run, you **cannot** verify files via the standard GitHub repository web interface. The files exist only in the temporary cloud storage of your Codespace.

To see these files on the GitHub Web UI, you must perform a **Live Production Run**:
1. Run the command without the `-d` flag: `python3 -m scripts.pull_logs`.
2. The Forge will finalize the run and push the files to your repository.
3. Refresh your GitHub repository page; the files will now appear in the location you defined in your `dataPath`.

---

### 🛡️ Post-Run Verification Checklist
After your dry run, check for these three specific things to ensure a successful "Smelt":
1. **JSON Size:** Is the JSON file larger than 2KB? (Ensures it captured more than just a header).
2. **Avatar Cache:** Check the `avatars/` folder. Do you see character ID folders with `.png` files inside?
3. **Report Log:** Check your project root for `forge_report_latest.log`. It will show exactly how many "Potential Posts" were detected during the simulation.