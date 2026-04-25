from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, TYPE_CHECKING

# These imports are only for type-hinting/IDE support and don't run at runtime
if TYPE_CHECKING:
    from .identity import DiscordUser, DiscordRole
    from .content import DiscordEmoji

@dataclass
class DiscordThreadMetadata:
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: Optional[bool] = None
    create_timestamp: Optional[str] = None # Added in API v10

@dataclass
class DiscordChannel:
    id: str
    type: int
    # --- Basic Metadata ---
    name: Optional[str] = None
    guild_id: Optional[str] = None
    parent_id: Optional[str] = None
    topic: Optional[str] = None
    position: Optional[int] = None
    nsfw: bool = False
    permissions: Optional[str] = None
    
    # --- Thread & Message Stats ---
    # Unified thread_metadata to prevent redefinition errors
    thread_metadata: Optional[DiscordThreadMetadata] = None
    last_message_id: Optional[str] = None
    last_pin_timestamp: Optional[str] = None
    message_count: int = 0
    member_count: int = 0
    total_message_sent: int = 0
    
    # --- Thread Specifics (The "Stealth" Keys) ---
    owner_id: Optional[str] = None
    member: Optional[Any] = None # ThreadMemberObject

    # --- Voice/Video Defaults ---
    bitrate: int = 64000
    user_limit: int = 0
    rtc_region: Optional[str] = None
    video_quality_mode: int = 1

    # --- Forum & Default Settings ---
    rate_limit_per_user: int = 0
    default_auto_archive_duration: int = 1440
    default_thread_rate_limit_per_user: int = 0
    default_sort_order: Optional[int] = None
    default_forum_layout: int = 0

    # --- Complex Collections ---
    permission_overwrites: List[Any] = field(default_factory=list)
    recipients: List['DiscordUser'] = field(default_factory=list)
    available_tags: List[Any] = field(default_factory=list)
    applied_tags: List[str] = field(default_factory=list)

    # --- Icons & Reactions ---
    icon: Optional[str] = None
    default_reaction_emoji: Optional[Any] = None

    # --- System Flags ---
    # Unified flags to a single definition
    flags: int = 0
    application_id: Optional[str] = None
    managed: bool = False

    @property
    def is_thread(self) -> bool:
        return self.type in [10, 11, 12]

    @property
    def is_category(self) -> bool:
        return self.type == 4

    @property
    def is_forum(self) -> bool:
        return self.type == 15
