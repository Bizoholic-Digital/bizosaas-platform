import pytest
import json
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.rag import RAGService

@pytest.fixture
def mock_engine():
    return MagicMock()

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def rag_service(mock_engine, mock_session):
    with patch("sqlalchemy.create_engine", return_value=mock_engine), \
         patch("sqlalchemy.orm.sessionmaker", return_value=mock_session):
        # We also need to patch _init_db to avoid actual DB connection
        with patch.object(RAGService, "_init_db"):
            service = RAGService()
            service.engine = mock_engine
            service.Session = mock_session
            return service

@pytest.mark.asyncio
async def test_get_embeddings_mocked(rag_service):
    # Test fallback to zeroes when API key is missing
    with patch("os.getenv", return_value=None):
        rag_service.openai_api_key = None
        embedding = await rag_service._get_embeddings("test")
        assert len(embedding) == 1536
        assert all(v == 0.0 for v in embedding)

@pytest.mark.asyncio
async def test_get_embeddings_api(rag_service):
    rag_service.openai_api_key = "test_key"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"embedding": [0.1, 0.2]}]}
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        embedding = await rag_service._get_embeddings("test")
        assert embedding == [0.1, 0.2]

@pytest.mark.asyncio
async def test_ingest_knowledge(rag_service, mock_session):
    rag_service._get_embeddings = AsyncMock(return_value=[0.1, 0.2])
    
    mock_s = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_s
    mock_s.execute.return_value.scalar.return_value = 1
    
    doc_id = await rag_service.ingest_knowledge("content", {"meta": "data"}, "tenant", "agent")
    
    assert doc_id == "1"
    mock_s.commit.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_context(rag_service, mock_session):
    rag_service._get_embeddings = AsyncMock(return_value=[0.1, 0.2])
    
    mock_s = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_s
    mock_s.execute.return_value = [MagicMock(content="result1"), MagicMock(content="result2")]
    
    results = await rag_service.retrieve_context("query", "agent", 2)
    
    assert len(results) == 2
    assert results[0] == "result1"
    assert results[1] == "result2"
