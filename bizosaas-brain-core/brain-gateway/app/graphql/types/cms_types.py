import strawberry
from typing import Optional, List, Dict, Any
from datetime import datetime

@strawberry.type
class CMSPageType:
    id: Optional[str]
    title: str
    slug: str
    content: str
    status: str
    author_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    parent_id: Optional[str] = None

@strawberry.type
class CMSPostType:
    id: Optional[str]
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str
    categories: List[str]
    tags: List[str]
    featured_image: Optional[str] = None
    author_id: Optional[str] = None
    published_at: Optional[datetime] = None

@strawberry.type
class CMSStatsType:
    pages: int
    posts: int
    media: int
    last_sync: Optional[datetime] = None

@strawberry.type
class CMSPluginType:
    id: str
    name: str
    description: Optional[str] = None
    status: str
    version: Optional[str] = None
    author: Optional[str] = None
    icon: Optional[str] = None
    installed: bool

@strawberry.input
class CMSPageInput:
    title: str
    slug: str
    content: str
    status: str = "draft"
    author_id: Optional[str] = None
    parent_id: Optional[str] = None

@strawberry.input
class CMSPostInput:
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    featured_image: Optional[str] = None
