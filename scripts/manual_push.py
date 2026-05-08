# ChronicleForge/scripts/manual_push.py
import os
import json
from dotenv import load_dotenv

from .utils import LOCAL_REGISTRY, get_repo_folder_name
from . import git_sync
from .config import FORGE_CONFIG

load_dotenv()

def run_manual_push():
    """
    Reads the CURRENT local campaign-registry.json and pushes all local 
    campaign data and the registry itself to their respective repositories.
    """
    if not os.path.exists(LOCAL_REGISTRY):
        print(f"❌ Error: Local registry not found at {LOCAL_REGISTRY}")
        return

    print("\n" + "="*60)
    print("🚀 MANUAL GIT PUSH: Synchronizing Local Cache to GitHub")
    print("="*60)

    # 1. Load the local registry
    with open(LOCAL_REGISTRY, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    campaigns = registry.get("campaigns", {})
    
    # 2. Sync each Campaign
    processed_repos = set()
    for camp_key, camp_data in campaigns.items():
        repo = camp_data.get('repository')
        branch = camp_data.get('branch', 'main')
        
        if not repo:
            continue
            
        repo_folder = get_repo_folder_name(repo)
        
        # Prevent duplicate pushes for the same repo
        if repo_folder in processed_repos:
            continue
            
        processed_repos.add(repo_folder)

        print(f"\n📂 Processing Repository: {repo_folder}")
        try:
            push_res = git_sync.push_updates(repo_folder, branch=branch)
            if isinstance(push_res, str):
                print(f"   ❌ {repo_folder} failed to sync: {push_res}")
            else:
                print(f"   ✅ {repo_folder} is synchronized.")
        except Exception as e:
            print(f"   💥 [Error] Failed syncing {repo_folder}: {e}")

    # 3. Sync the Master Registry to the Website Repo
    website_repo = FORGE_CONFIG.website_repo
    website_branch = FORGE_CONFIG.website_branch
    
    if website_repo:
        print(f"\n🌐 Syncing Master Registry to Website: {website_repo}...")
        try:
            # We pass the dictionary we loaded at the start
            success = git_sync.sync_website_registry(website_repo, registry, branch=website_branch)
            if isinstance(success, str):
                print(f"   ❌ Master Registry failed to sync: {success}")
            else:
                print("   ✅ Master Registry synchronized.")
        except Exception as e:
            print(f"   💥 [Error] Failed syncing Website Registry: {e}")
    else:
        print("\n⚠️  Skipping Website Sync: WEBSITE_REPO not defined in .env")

    print("\n" + "="*60)
    print("🏁 Manual Push Sequence Complete.")
    print("="*60 + "\n")

if __name__ == "__main__":
    confirm = input("This will push all local changes to GitHub. Continue? (y/n): ")
    if confirm.lower() == 'y':
        run_manual_push()
    else:
        print("Aborted.")
