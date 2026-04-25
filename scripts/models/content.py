from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Union, TYPE_CHECKING

# These imports are only for type-hinting/IDE support and don't run at runtime
if TYPE_CHECKING:
    from .identity import DiscordUser
    from .structure import DiscordChannel

@dataclass
class DiscordGuild:
    id: str
    name: str
    owner_id: str
    
    # --- Visuals ---
    icon: Optional[str] = None
    icon_hash: Optional[str] = None
    splash: Optional[str] = None
    discovery_splash: Optional[str] = None
    banner: Optional[str] = None
    
    # --- Configuration & Levels ---
    afk_channel_id: Optional[str] = None
    afk_timeout: int = 300
    verification_level: int = 0
    default_message_notifications: int = 0
    explicit_content_filter: int = 0
    mfa_level: int = 0
    nsfw_level: int = 0
    premium_tier: int = 0
    premium_subscription_count: int = 0
    preferred_locale: str = "en-US"
    
    # --- Channels & Safety ---
    system_channel_id: Optional[str] = None
    system_channel_flags: int = 0
    rules_channel_id: Optional[str] = None
    public_updates_channel_id: Optional[str] = None
    safety_alerts_channel_id: Optional[str] = None
    
    # --- Limits & Stats ---
    max_presences: Optional[int] = None
    max_members: int = 500000
    approximate_member_count: Optional[int] = None
    approximate_presence_count: Optional[int] = None
    max_video_channel_users: int = 0
    max_stage_video_channel_users: int = 0
    
    # --- Collections ---
    roles: List['DiscordRole'] = field(default_factory=list)
    emojis: List[DiscordEmoji] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    stickers: List[Any] = field(default_factory=list)
    
    # --- Miscellaneous ---
    owner: bool = False
    widget_enabled: bool = False
    widget_channel_id: Optional[str] = None
    application_id: Optional[str] = None
    vanity_url_code: Optional[str] = None
    description: Optional[str] = None
    welcome_screen: Optional[Any] = None
    premium_progress_bar_enabled: bool = False
    permissions: Optional[str] = None

@dataclass
class DiscordMessage:
    # --- Required Fields (Present in DCE & Source) ---
    id: str
    channel_id: str
    author: 'DiscordUser' # We'll define this next
    content: str
    timestamp: str
    type: int
    
    # --- Structural Defaults (The "Stealth Keys") ---
    # These ensure the JSON always has the key, even if DCE leaves it out.
    tts: bool = False
    mention_everyone: bool = False
    pinned: bool = False
    edited_timestamp: Optional[str] = None
    
    # --- Collections (Always initialized as empty arrays) ---
    mentions: List['DiscordUser'] = field(default_factory=list)
    attachments: List['DiscordAttachment'] = field(default_factory=list)
    embeds: List[Any] = field(default_factory=list)
    mention_channels: List[Any] = field(default_factory=list)
    components: List[Any] = field(default_factory=list)
    sticker_items: List[Any] = field(default_factory=list)
    stickers: List[Any] = field(default_factory=list)
    reactions: List['DiscordReaction'] = field(default_factory=list)
    
    # --- Optional Metadata (Inferred or Contextual) ---
    webhook_id: Optional[str] = None
    application_id: Optional[str] = None
    position: Optional[int] = None
    nonce: Optional[Union[str, int]] = None
    flags: Optional[int] = 0
    
    # --- Complex Objects (Recursive or Nested) ---
    message_reference: Optional[dict] = None
    referenced_message: Optional['DiscordMessage'] = None
    thread: Optional['DiscordChannel'] = None
    interaction: Optional[Any] = None
    activity: Optional[Any] = None
    application: Optional[Any] = None
    role_subscription_data: Optional[Any] = None

    # --- New API v10 Fields ---
    interaction_metadata: Optional[Dict[str, Any]] = None # Who/What triggered the message
    poll: Optional[Dict[str, Any]] = None                # Native Poll data
    resolved: Optional[Dict[str, Any]] = None            # Cached data for mentions
    call: Optional[Dict[str, Any]] = None                # Metadata for voice calls
    
    # High-Fidelity Sync Check
    # Discord now includes a 'version' for some messages
    version: int = 0

    def __post_init__(self):
        """
        Mirrors the TS constructor logic.
        Ensures userName is always populated for 'Quick Filtering'.
        """
        if self.author:
            self.userName = self.author.username

@dataclass
class DiscordAttachment:
    id: str
    filename: str
    size: int
    url: str
    proxy_url: str
    content_type: Optional[str] = "image/png"
    original_content_type: Optional[str] = "image/png"
    height: Optional[int] = None
    width: Optional[int] = None
    ephemeral: bool = False
    duration_secs: Optional[float] = None
    waveform: Optional[str] = None
    flags: int = 0
    content_scan_version: int = 4
    placeholder: Optional[str] = None
    placeholder_version: int = 1
    # --- API v10 Metadata ---
    title: Optional[str] = None
    clip_created_at: Optional[str] = None
    clip_participants: List['DiscordUser'] = field(default_factory=list)

@dataclass
class EmbedFooter:
    text: str
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None

@dataclass
class EmbedImage:
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedThumbnail:
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedVideo:
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedProvider:
    name: Optional[str] = None
    url: Optional[str] = None

@dataclass
class EmbedAuthor:
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None

@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool = False

@dataclass
class DiscordEmbed:
    # Basic Fields
    title: Optional[str] = None
    type: str = "rich" # Default for most bot/narrative embeds
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    color: Optional[int] = None
    
    # Nested Objects
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    
    # Collections
    fields: List[EmbedField] = field(default_factory=list)

@dataclass
class DiscordEmoji:
    id: Optional[str] = None
    name: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    user: Optional['DiscordUser'] = None # Reference to Identity group
    require_colons: bool = False
    managed: bool = False
    animated: bool = False
    available: bool = True

@dataclass
class DiscordReaction:
    count: int
    emoji: 'DiscordEmoji'
    me: bool
    me_burst: bool
    burst_me: bool = False 
    burst_count: int = 0    
    burst_colors: List[str] = field(default_factory=list)
    count_details: Dict[str, int] = field(default_factory=lambda: {"burst": 0, "normal": 0})

    def __post_init__(self):
        """
        Since DCE only gives us a flat count, we ensure count_details 
        is initialized to match the total count as 'normal' reactions.
        """
        if self.count_details["normal"] == 0 and self.count > 0:
            self.count_details["normal"] = self.count
