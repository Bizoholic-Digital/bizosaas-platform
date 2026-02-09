from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class Page(BaseModel):
    id: Optional[str] = None
    title: str
    slug: str
    content: str
    status: str = "draft"  # draft, published, private
    author_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    parent_id: Optional[str] = None

class Post(BaseModel):
    id: Optional[str] = None
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"
    categories: List[str] = []
    tags: List[str] = []
    featured_image: Optional[str] = None
    author_id: Optional[str] = None
    published_at: Optional[datetime] = None

class CMSStats(BaseModel):
    pages: int
    posts: int
    media: int
    last_sync: Optional[datetime] = None

class Plugin(BaseModel):
    id: str  # textdomain or slug
    name: str
    description: Optional[str] = None
    status: str = "inactive" # active, inactive
    version: Optional[str] = None
    author: Optional[str] = None
    icon: Optional[str] = None # URL to icon
    installed: bool = False

class CMSPort(ABC):
    """
    Abstract Port for Content Management Systems (WordPress, Webflow, etc).
    """

    @abstractmethod
    async def get_stats(self) -> CMSStats:
        pass
    
    @abstractmethod
    async def get_pages(self, limit: int = 100, **kwargs) -> List[Page]:
        pass
    
    @abstractmethod
    async def get_page(self, page_id: str) -> Optional[Page]:
        pass

    @abstractmethod
    async def create_page(self, page: Page) -> Page:
        pass
        
    @abstractmethod
    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> Page:
        pass
    
    @abstractmethod
    async def delete_page(self, page_id: str) -> bool:
        pass
    
    @abstractmethod
    async def get_posts(self, limit: int = 100, **kwargs) -> List[Post]:
        pass
        
    @abstractmethod
    async def get_post(self, post_id: str) -> Optional[Post]:
        pass
    
    @abstractmethod
    async def create_post(self, post: Post) -> Post:
        pass
        
    @abstractmethod
    async def update_post(self, post_id: str, updates: Dict[str, Any]) -> Post:
        pass
    
    @abstractmethod
    async def delete_post(self, post_id: str) -> bool:
        pass

    @abstractmethod
    async def get_plugins(self) -> List[Plugin]:
        pass

    @abstractmethod
    async def install_plugin(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def activate_plugin(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def deactivate_plugin(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def delete_plugin(self, slug: str) -> bool:
        pass

    @abstractmethod
    async def get_categories(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def create_category(self, category: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update_category(self, category_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def delete_category(self, category_id: str) -> bool:
        pass

    @abstractmethod
    async def list_media(self, limit: int = 100) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def upload_media(self, file_data: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def delete_media(self, media_id: str) -> bool:
        pass
