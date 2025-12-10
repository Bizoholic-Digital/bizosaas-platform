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

class CMSPort(ABC):
    """
    Abstract Port for Content Management Systems (WordPress, Webflow, etc).
    """
    
    @abstractmethod
    async def get_pages(self, limit: int = 100) -> List[Page]:
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
    async def get_posts(self, limit: int = 100) -> List[Post]:
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
