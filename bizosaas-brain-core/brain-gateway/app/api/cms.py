from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PageMessage(BaseModel):
    id: str
    title: str
    slug: str
    status: str
    published_at: Optional[datetime]
    updated_at: datetime
    author: str

class PostMessage(BaseModel):
    id: str
    title: str
    excerpt: str
    category: str
    status: str
    published_at: datetime
    author: str

# Mock Data
MOCK_PAGES = [
    {
        "id": "1",
        "title": "Home",
        "slug": "home",
        "status": "published",
        "published_at": datetime.now(),
        "updated_at": datetime.now(),
        "author": "Admin"
    },
    {
        "id": "2",
        "title": "About Us",
        "slug": "about-us",
        "status": "published",
        "published_at": datetime.now(),
        "updated_at": datetime.now(),
        "author": "Admin"
    },
    {
        "id": "3",
        "title": "Contact",
        "slug": "contact",
        "status": "draft",
        "published_at": None,
        "updated_at": datetime.now(),
        "author": "Editor"
    }
]

MOCK_POSTS = [
    {
        "id": "1",
        "title": "Getting Started with BizOSaaS",
        "excerpt": "Learn how to set up your new platform...",
        "category": "Documentation",
        "status": "published",
        "published_at": datetime.now(),
        "author": "Admin"
    },
    {
        "id": "2",
        "title": "5 Tips for Better Marketing",
        "excerpt": "Boost your campaigns with these simple tricks...",
        "category": "Marketing",
        "status": "draft",
        "published_at": datetime.now(),
        "author": "Marketer"
    }
]

@router.get("/pages", response_model=List[PageMessage])
async def list_pages():
    return MOCK_PAGES

@router.get("/posts", response_model=List[PostMessage])
async def list_posts():
    return MOCK_POSTS

@router.get("/media")
async def list_media():
    return []
