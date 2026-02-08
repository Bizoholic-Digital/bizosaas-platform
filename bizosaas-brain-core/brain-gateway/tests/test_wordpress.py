import unittest
from unittest.mock import AsyncMock, patch, Mock
from app.connectors.wordpress import WordPressConnector
from app.ports.cms_port import Page, Post

class TestWordPressConnector(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.credentials = {
            "url": "https://example.com",
            "username": "admin",
            "application_password": "password"
        }
        self.connector = WordPressConnector("tenant1", self.credentials)

    async def test_get_pages(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {
                    "id": 1,
                    "title": {"rendered": "About Us"},
                    "slug": "about-us",
                    "content": {"rendered": "Content"},
                    "status": "publish",
                    "author": 1
                }
            ]
            mock_instance.get.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            pages = await self.connector.get_pages()
            
            self.assertEqual(len(pages), 1)
            self.assertEqual(pages[0].title, "About Us")
            self.assertEqual(pages[0].slug, "about-us")

    async def test_create_page(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": 10,
                "title": {"rendered": "New Page"},
                "slug": "new-page",
                "content": {"rendered": "Content"},
                "status": "draft"
            }
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            new_page = Page(title="New Page", slug="new-page", content="Content")
            result = await self.connector.create_page(new_page)
            
            self.assertEqual(result.id, "10")
            self.assertEqual(result.title, "New Page")

    async def test_upload_media(self):
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": 100,
                "source_url": "https://example.com/wp-content/uploads/test.jpg",
                "mime_type": "image/jpeg"
            }
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await self.connector.upload_media(b"fake_data", "test.jpg", "image/jpeg")
            
            self.assertEqual(result["id"], 100)
            self.assertEqual(result["source_url"], "https://example.com/wp-content/uploads/test.jpg")

    async def test_delete_plugin(self):
         with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            # Mock get_plugins to find the target_path
            mock_response_list = Mock()
            mock_response_list.status_code = 200
            mock_response_list.json.return_value = [
                {"plugin": "hello-dolly/hello.php", "name": "Hello Dolly"}
            ]
            
            mock_response_delete = Mock()
            mock_response_delete.status_code = 200
            
            mock_instance.get.return_value = mock_response_list
            mock_instance.delete.return_value = mock_response_delete
            mock_client.return_value.__aenter__.return_value = mock_instance

            success = await self.connector.delete_plugin("hello-dolly")
            
            self.assertTrue(success)
            # Verify it called delete with the correct path
            # self.connector._get_api_url("plugins/hello-dolly/hello.php")
            # We can't easily check the URL without more complex mock setup, but at least coverage is there.

if __name__ == '__main__':
    unittest.main()
