import random
import uuid
from locust import HttpUser, task, between

class BrainGatewayUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Executed when a simulated user starts.
        We'll use a mock token or assume auth is bypassed for testing if configured.
        """
        # In a real scenario, we'd login or use a pre-shared test token
        self.headers = {
            "Authorization": "Bearer test-admin-token",
            "X-Tenant-ID": str(uuid.uuid4())
        }

    @task(3)
    def get_health(self):
        """Check system health"""
        self.client.get("/health")

    @task(5)
    def list_connectors(self):
        """Browse connector marketplace or status"""
        self.client.get("/api/connectors", headers=self.headers)
        self.client.get("/api/connectors/types", headers=self.headers)

    @task(2)
    def get_metrics(self):
        """Fetch metrics summary used by dashboard"""
        self.client.get("/api/brain/metrics/summary", headers=self.headers)

    @task(1)
    def agent_chat_sim(self):
        """Simulate agent interaction"""
        agent_id = str(uuid.uuid4())
        self.client.post(
            f"/api/brain/agents/{agent_id}/chat",
            json={"message": "What is the status of my campaign?"},
            headers=self.headers
        )

    @task(1)
    def sync_data_sim(self):
        """Simulate a data sync trigger"""
        self.client.get(
            "/api/connectors/hubspot/sync/contacts",
            headers=self.headers
        )
