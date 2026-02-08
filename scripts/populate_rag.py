import os
import sys
import json
import asyncio
import httpx
from glob import glob

# Add gateway to path to import rag_service
sys.path.append(os.path.join(os.getcwd(), 'bizosaas-brain-core/brain-gateway'))

async def populate_rag():
    print("🚀 Populating RAG knowledge base...")
    
    # Try to connect to RAG service via API
    api_url = "http://localhost:8000/api/brain/rag/ingest"
    
    # Find all documentation files
    docs = glob("*.md") + glob("docs/**/*.md", recursive=True)
    
    if not docs:
        print("⚠️ No documentation found to ingest.")
        return

    async with httpx.AsyncClient(timeout=30.0) as client:
        for doc_path in docs:
            print(f"📄 Processing {doc_path}...")
            try:
                with open(doc_path, 'r') as f:
                    content = f.read()
                
                # Split content into chunks (simple version)
                chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
                
                for i, chunk in enumerate(chunks):
                    # Ingest via API
                    try:
                        resp = await client.post(api_url, json={
                            "content": chunk,
                            "metadata": {
                                "source": doc_path,
                                "chunk": i
                            },
                            "tenant_id": "platform",
                            "agent_id": "general"
                        })
                        if resp.status_code == 200:
                             print(f"  ✅ Ingested chunk {i}")
                        else:
                             print(f"  ❌ Failed to ingest via API: {resp.status_code}")
                             # Fallback: direct import if possible
                    except Exception as e:
                        print(f"  ❌ API connection failed: {e}")
                        break
            except Exception as e:
                print(f"  ❌ Failed to process {doc_path}: {e}")

if __name__ == "__main__":
    asyncio.run(populate_rag())
