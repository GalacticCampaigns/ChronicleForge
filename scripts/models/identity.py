from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class DiscordRole:
    id: str
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    flags: int
    icon: Optional[str] = None
    unicode_emoji: Optional[str] = None
    tags: Optional[dict] = None  

@dataclass
class DiscordUser:
    id: str
    username: str
    discriminator: str = "0000"
    global_name: Optional[str] = None
    display_name: Optional[str] = None
    pronouns: Optional[str] = None 
    avatar: Optional[str] = None
    bot: bool = False
    system: bool = False
    mfa_enabled: bool = False
    locale: str = "en-US"
    verified: bool = False
    email: Optional[str] = None
    flags: int = 0
    premium_type: int = 0
    public_flags: int = 0
    clan: Optional[Any] = None
    primary_guild: Optional[Any] = None

    # --- Decoration & Effects ---
    banner: Optional[str] = None
    banner_color: Optional[str] = None
    accent_color: Optional[int] = None
    avatar_decoration: Optional[str] = None
    avatar_decoration_data: Optional[Dict[str, Any]] = field(
        default_factory=lambda: {"asset": None, "sku_id": None}
    )
    # Profile Effects (The flashy animations behind a user)
    profile_effect_id: Optional[str] = None