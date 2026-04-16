# ChronicleForge/scripts/navigator.py

import os
import json
import re
import requests
from .utils import save_registry, pad_timestamp, LOCAL_REGISTRY
from .notifier import send_update_email
import scripts.git_sync as git_sync 

# Narrative Types for Refinement logic (DCE Types mapped to API Integers)
# 0: Default, 19: Reply, 21: ThreadStarter
NARRATIVE_TYPES = FORGE_CONFIG.get("forensics", "narrative_types")
NSFW_KEYWORDS = FORGE_CONFIG.get("forensics", "nsfw_keywords")

class Navigator:
    def __init__(self, registry_data):
        self.registry = registry_data
        self.report_log = {}

    def update_report(self, camp_name, action, title, count=0, nsfw_count=0):
        """Logs activity or errors to the final Forge dispatch report."""
        if camp_name not in self.report_log:
            self.report_log[camp_name] = []
        
        self.report_log[camp_name].append({
            "action": action, 
            "title": title, 
            "count": count,
            "nsfw_count": nsfw_count
        })
    
    def analyze_and_merge(self, log_entry, refined_messages):
        """
        Forensic Audit: Deep-scans narrative content to calculate stats 
        and safety labels.
        """
        parent_id = str(log_entry.get("channelID"))
        # Initialize stats tracking for all known sub-threads
        t_stats = {str(t["threadID"]): {"total": 0, "nsfw": 0, "abs_last_id": ""} 
                   for t in log_entry.get("threads", [])}
        
        forensics = {
            "abs_max_id": 0,      
            "narrative_max_ts": "", 
            "narrative_max_id": 0,
            "parent_total": 0,
            "parent_nsfw": 0,
            "grand_total": 0,
            "grand_nsfw": 0,
            "thread_stats": t_stats
        }

        for msg in refined_messages:
            msg_id_int = int(msg.get("id"))
            msg_chan_id = str(msg.get("channel_id"))
            is_narrative = msg.get("type") in NARRATIVE_TYPES

            # A. Loop Breaker: Track absolute highest ID regardless of type
            if msg_id_int > forensics["abs_max_id"]:
                forensics["abs_max_id"] = msg_id_int

            # B. Narrative Audit (Counts and Safety)
            if is_narrative:
                forensics["grand_total"] += 1
                
                # NSFW Forensic Detection (Reactions + Content)
                is_msg_nsfw = False
                for r in msg.get("reactions", []):
                    ename = r.get("emoji", {}).get("name", "").lower()
                    if any(word in ename for word in NSFW_KEYWORDS):
                        is_msg_nsfw = True
                        break
                
                content = (msg.get("content") or "").lower()
                if not is_msg_nsfw and any(word in content for word in NSFW_KEYWORDS):
                    is_msg_nsfw = True

                if is_msg_nsfw:
                    forensics["grand_nsfw"] += 1

                # Hierarchical Calculation: Parent vs Thread
                if msg_chan_id == parent_id:
                    forensics["parent_total"] += 1
                    if is_msg_nsfw: forensics["parent_nsfw"] += 1
                elif msg_chan_id in forensics["thread_stats"]:
                    forensics["thread_stats"][msg_chan_id]["total"] += 1
                    if is_msg_nsfw: forensics["thread_stats"][msg_chan_id]["nsfw"] += 1
                
                # Temporal Tracking: Capture newest post timestamp
                if msg_id_int > forensics["narrative_max_id"]:
                    forensics["narrative_max_id"] = msg_id_int
                    forensics["narrative_max_ts"] = msg.get("timestamp")

            # C. Thread High-Water Mark Update
            if msg_chan_id in forensics["thread_stats"]:
                curr_abs = forensics["thread_stats"][msg_chan_id]["abs_last_id"]
                if not curr_abs or msg_id_int > int(curr_abs):
                    forensics["thread_stats"][msg_chan_id]["abs_last_id"] = str(msg_id_int)

        return forensics

    def apply_forensics_to_registry(self, log_entry, forensics, api_id_stamp=None):
        """Registry Smash: Finalizes the metadata state for deployment."""
        # 1. Hierarchical NSFW Logic
        # Only overwrite False -> True based on 90% density
        if not log_entry.get("isNSFW", False):
            p_total = forensics["parent_total"]
            parent_pct = forensics["parent_nsfw"] / p_total if p_total > 0 else 0
            if parent_pct >= 0.9:
                log_entry["isNSFW"] = True
            
        log_entry["messageCount"] = forensics["grand_total"]
        if forensics["narrative_max_ts"]:
            log_entry["lastMessageTimestamp"] = forensics["narrative_max_ts"]

        # 2. Sync Stamping (Loop Breaker)
        final_sync_id = api_id_stamp or str(forensics["abs_max_id"])
        if final_sync_id and final_sync_id != "0":
            log_entry["last_synced_id"] = final_sync_id

        # 3. Thread Synchronization & Auto-Stabilization
        for t in log_entry.get("threads", []):
            t_id = str(t.get("threadID"))
            if t_id in forensics["thread_stats"]:
                stats = forensics["thread_stats"][t_id]
                t["messageCount"] = stats["total"]
                
                # Independent Thread NSFW Threshold
                if not t.get("isNSFW", False):
                    t_total = stats["total"]
                    thread_pct = stats["nsfw"] / t_total if t_total > 0 else 0
                    if thread_pct >= 0.9:
                        t["isNSFW"] = True
                
                if stats["abs_last_id"]:
                    t["last_synced_id"] = stats["abs_last_id"]

    def should_sync(self, entry, token, force_all=False):
        """API Pre-Check: Evaluates narrative delta before triggering Miner."""
        if not entry.get("isActive", True): return False, None
        # Skip Miner for Legacy Archives
        if entry.get("syncStatus") == "legacy": return False, None

        last_id = str(entry.get("last_synced_id", ""))
        target_id = entry.get("channelID") or entry.get("threadID")
        camp_name = entry.get("title", target_id)
        
        headers = {"Authorization": f"Bot {token}"}
        url = f"https://discord.com/api/v10/channels/{target_id}/messages?limit=10"
        
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                err = resp.json().get('message', 'Access Denied')
                self.update_report("System", "⚠️ ACCESS DENIED", f"{camp_name}: {err}")
                return False, None
            
            messages = resp.json()
            if not messages: return False, None

            # Find the newest NARRATIVE Snowflake (v10 API Mapping)
            latest_ic_id = None
            for msg in messages:
                if msg.get("type") in NARRATIVE_TYPES:
                    latest_ic_id = str(msg.get("id"))
                    break
            
            if not latest_ic_id: return False, None

            has_new = False
            if not last_id:
                has_new = True
            else:
                try:
                    has_new = int(latest_ic_id) > int(last_id)
                except ValueError:
                    has_new = latest_ic_id != last_id

            # Forge Wake-Up Logic
            if has_new and entry.get("syncStatus") == "stable":
                print(f"      [Wake-Up] Activity detected in stable chapter: {camp_name}")
                entry["syncStatus"] = "active"

            if force_all: return True, latest_ic_id
            if entry.get("syncStatus") == "stable": return False, latest_ic_id

            return has_new, latest_ic_id

        except Exception as e:
            self.update_report("System", "💥 TIMEOUT", f"Check failed for {camp_name}: {str(e)}")
            return False, None

    def finalize_run(self, is_dry_run=False):
        """Saves registry, synchronizes brain to GitHub, and dispatches Forge reports."""
        save_registry(self.registry)

        if not is_dry_run:
            website_repo = os.getenv("WEBSITE_REPO")
            website_branch = os.getenv("WEBSITE_BRANCH", "main")
            if website_repo:
                print(f"\n🚀 Syncing Forge Brain to: {website_repo}")
                git_sync.sync_website_registry(website_repo, self.registry, branch=website_branch)
        
        # Dispatch Heartbeat Email
        if not self.report_log:
            self.update_report("Forge", "STATUS", "All narratives synchronized/No new activity.")

        send_update_email(self.report_log, is_dry_run)