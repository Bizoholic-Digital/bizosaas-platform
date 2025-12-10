import unittest
from unittest.mock import AsyncMock, patch, Mock
from app.connectors.fluent_crm import FluentCRMConnector
from app.connectors.woocommerce import WooCommerceConnector
from app.connectors.trello import TrelloConnector
from app.connectors.plane import PlaneConnector
from app.connectors.lago import LagoConnector
from app.ports.billing_port import Customer

class TestConnectors(unittest.IsolatedAsyncioTestCase):

    async def test_fluentcrm_get_contacts(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "data": [
                    {"id": 1, "email": "test@example.com", "first_name": "Test", "last_name": "User", "tags": [1, 2]}
                ]
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            connector = FluentCRMConnector("tenant1", {"url": "https://wp.example.com", "username": "user", "application_password": "pass"})
            contacts = await connector.get_contacts()
            
            self.assertEqual(len(contacts), 1)
            self.assertEqual(contacts[0].email, "test@example.com")
            self.assertEqual(contacts[0].first_name, "Test")

    async def test_woocommerce_get_products(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": 101, "name": "Shirt", "price": "19.99", "status": "publish"}
            ]
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            connector = WooCommerceConnector("tenant1", {"url": "https://shop.example.com", "consumer_key": "ck_1", "consumer_secret": "cs_1"})
            products = await connector.get_products()
            
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0].name, "Shirt")
            self.assertEqual(products[0].price, 19.99)

    async def test_trello_get_boards(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": "board1", "name": "My Board", "url": "https://trello.com/b/1"}
            ]
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            connector = TrelloConnector("tenant1", {"api_key": "key", "api_token": "token"})
            boards = await connector.get_boards()
            
            self.assertEqual(len(boards), 1)
            self.assertEqual(boards[0].name, "My Board")

    async def test_plane_get_projects(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [
                    {"id": "proj1", "name": "Project Alpha", "identifier": "PA"}
                ]
            }
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            connector = PlaneConnector("tenant1", {"url": "https://plane.so", "api_key": "key", "workspace_slug": "slug"})
            projects = await connector.get_projects()
            
            self.assertEqual(len(projects), 1)
            self.assertEqual(projects[0].name, "Project Alpha")

    async def test_lago_create_customer(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "customer": {"external_id": "cust_1", "name": "New Customer", "email": "c@example.com", "currency": "USD"}
            }
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            connector = LagoConnector("tenant1", {"api_url": "http://lago", "api_key": "key"})
            new_cust = Customer(id="cust_1", email="c@example.com", name="New Customer")
            
            result = await connector.create_customer(new_cust)
            
            self.assertEqual(result.name, "New Customer")

if __name__ == '__main__':
    unittest.main()
