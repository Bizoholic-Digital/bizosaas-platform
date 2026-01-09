import unittest
from unittest.mock import AsyncMock, patch, Mock
from app.connectors.hubspot import HubSpotConnector
from app.ports.crm_port import Contact, Deal

class TestHubSpotConnector(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.credentials = {
            "access_token": "token123",
            "refresh_token": "refresh123"
        }
        self.connector = HubSpotConnector("tenant1", self.credentials)

    async def test_get_contacts(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [
                    {
                        "id": "1",
                        "properties": {
                            "email": "john@example.com",
                            "firstname": "John",
                            "lastname": "Doe"
                        }
                    }
                ]
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            contacts = await self.connector.get_contacts()
            
            self.assertEqual(len(contacts), 1)
            self.assertEqual(contacts[0].email, "john@example.com")
            self.assertEqual(contacts[0].first_name, "John")

    async def test_create_deal(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": "deal_123",
                "properties": {
                    "dealname": "Large Deal",
                    "amount": "50000.0"
                }
            }
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            deal = Deal(title="Large Deal", value=50000.0, stage="closedwon")
            result = await self.connector.create_deal(deal)
            
            self.assertEqual(result.id, "deal_123")
            self.assertEqual(result.value, 50000.0)

if __name__ == '__main__':
    unittest.main()
