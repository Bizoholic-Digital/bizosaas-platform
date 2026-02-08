import os
import sys
import uuid
from datetime import datetime

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.models.gaming import Game, GameCompany, HumanPlayerProfile
from app.models.user import User
from dotenv import load_dotenv
load_dotenv()

def seed_gaming_data():
    db = SessionLocal()
    try:
        print("Seeding Expanded Gaming Data...")
        
        # 1. Companies
        companies = [
            {
                "name": "Riot Games",
                "slug": "riot-games",
                "type": "developer",
                "description": "Developer of League of Legends and Valorant.",
                "headquarters": "Los Angeles, CA",
                "wiki_content": {"milestones": ["Founded 2006", "Acquired by Tencent 2011"], "news": ["Arcane Season 2 Launch"]}
            },
            {
                "name": "Valve Corporation",
                "slug": "valve",
                "type": "developer",
                "description": "Creator of Steam and Dota 2.",
                "headquarters": "Bellevue, WA",
                "wiki_content": {"milestones": ["Half-Life Launch 1998", "Steam Launch 2003"]}
            }
        ]
        
        company_objs = {}
        for c_data in companies:
            comp = db.query(GameCompany).filter_by(slug=c_data["slug"]).first()
            if not comp:
                comp = GameCompany(**c_data)
                db.add(comp)
            else:
                for key, value in c_data.items():
                    setattr(comp, key, value)
            db.flush()
            company_objs[c_data["slug"]] = comp

        # 2. Games
        games_data = [
            {
                "name": "Valorant", 
                "slug": "valorant", 
                "genre": "FPS", 
                "description": "Tactical hero shooter",
                "developer_id": company_objs["riot-games"].id,
                "wiki_data": {"engine": "Unreal Engine 4", "release_year": 2020}
            },
            {
                "name": "Dota 2", 
                "slug": "dota-2", 
                "genre": "MOBA", 
                "description": "Multiplayer online battle arena",
                "developer_id": company_objs["valve"].id,
                "wiki_data": {"engine": "Source 2", "release_year": 2013}
            }
        ]
        
        for g_data in games_data:
            game = db.query(Game).filter_by(slug=g_data["slug"]).first()
            if not game:
                game = Game(**g_data)
                db.add(game)
            else:
                for key, value in g_data.items():
                    setattr(game, key, value)

        # 3. Human Player Profiles
        # Find a test user or create one
        test_user = db.query(User).first()
        if test_user:
            profile_data = {
                "user_id": test_user.id,
                "nickname": "Antigravity_Ace",
                "full_name": "John Doe",
                "bio": "Veteran FPS player and strategy enthusiast.",
                "spouse_name": "Jane Doe",
                "kids_names": ["Alice", "Bob"],
                "news_mentions": [
                    {"title": "Ace wins local tournament", "url": "https://example.com/news/1"},
                    {"title": "New record in Valorant path", "url": "https://example.com/news/2"}
                ]
            }
            
            profile = db.query(HumanPlayerProfile).filter_by(user_id=test_user.id).first()
            if not profile:
                profile = HumanPlayerProfile(**profile_data)
                db.add(profile)
            else:
                for key, value in profile_data.items():
                    setattr(profile, key, value)

        db.commit()
        print("Gaming wiki and profiles seeded successfully!")
    except Exception as e:
        print(f"Error seeding gaming data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_gaming_data()
