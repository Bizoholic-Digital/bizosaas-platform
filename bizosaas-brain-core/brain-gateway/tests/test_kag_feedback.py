
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.mcp import Base, KagRelationship
from app.services.knowledge_graph import KnowledgeGraph

class TestKagFeedback(unittest.TestCase):
    def setUp(self):
        # Create in-memory SQLite for testing
        self.engine = create_engine('sqlite:///:memory:')
        # Re-import specifically to avoid full metadata creation errors
        from app.models.mcp import KagRelationship
        KagRelationship.__table__.create(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()
        self.kg = KnowledgeGraph()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(self.engine)

    def test_record_new_interaction(self):
        # Test creating a new emergent relationship
        source = "agent1"
        target = "tool1"
        
        self.kg.record_interaction(self.db, source, target, success=True)
        
        # Verify in DB
        rel = self.db.query(KagRelationship).filter_by(source_tool=source, target_tool=target).first()
        self.assertIsNotNone(rel)
        self.assertEqual(rel.strength, 10)
        self.assertEqual(rel.evidence_count, 1)
        self.assertEqual(rel.relationship_type, "emergent_workflow")

    def test_strengthen_interaction(self):
        # Test strengthening an existing relationship
        source = "agent1"
        target = "tool1"
        
        # Initial recording
        self.kg.record_interaction(self.db, source, target, success=True)
        
        # Strengthen
        self.kg.record_interaction(self.db, source, target, success=True)
        
        # Verify in DB
        rel = self.db.query(KagRelationship).filter_by(source_tool=source, target_tool=target).first()
        self.assertEqual(rel.strength, 15) # 10 + 5
        self.assertEqual(rel.evidence_count, 2)

    def test_weaken_interaction(self):
        # Test weakening on failure
        source = "agent1"
        target = "tool1"
        
        # Initial recording
        self.kg.record_interaction(self.db, source, target, success=True) # strength 10
        
        # Weaken
        self.kg.record_interaction(self.db, source, target, success=False)
        
        # Verify in DB
        rel = self.db.query(KagRelationship).filter_by(source_tool=source, target_tool=target).first()
        self.assertEqual(rel.strength, 0) # 10 - 10

if __name__ == '__main__':
    unittest.main()
