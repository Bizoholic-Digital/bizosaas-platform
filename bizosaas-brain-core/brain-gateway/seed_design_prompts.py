import os
import sys
import asyncio
from uuid import uuid4

# Setup paths
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.models.prompt import PromptTemplate

async def seed_design_prompts():
    print("Seeding Design & UI/UX Prompt Templates...")
    db = SessionLocal()
    
    try:
        # 1. UI/UX Specialist Template
        ui_specialist = PromptTemplate(
            name="ui_ux_specialist",
            category="instruction",
            template_text="""You are a world-class UI/UX Design Specialist. 
Your goal is to create stunning, user-centric interfaces.

Available Tools:
- Google Stitch: Use for design extraction and generating screens from text.
- Figma: Use to fetch variables, styles, and assets from Figma files.
- Canva: Use for social media assets and marketing templates.
- V0.dev: Use for converting design screenshots into functional React + Tailwind code.

Task: {task}
Context: {context}

Analytical Approach:
1. Understand the user's brand and design DNA.
2. Use Figma or Stitch to extract existing patterns if available.
3. Propose a modern, high-fidelity design.
4. If code is requested, leverage V0.dev to generate the React implementation.

Always prioritize accessibility (WCAG), responsiveness, and micro-animations.""",
            variables={"task": "str", "context": "str"},
            strategy="chain_of_thought",
            is_default=True
        )
        
        # Check if exists
        existing = db.query(PromptTemplate).filter(PromptTemplate.name == "ui_ux_specialist").first()
        if not existing:
            db.add(ui_specialist)
            print("Created 'ui_ux_specialist' prompt template.")
        else:
            existing.template_text = ui_specialist.template_text
            existing.strategy = ui_specialist.strategy
            print("Updated 'ui_ux_specialist' prompt template.")
            
        db.commit()
        print("Design prompts seeded successfully.")
        
    except Exception as e:
        print(f"Error seeding design prompts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_design_prompts())
