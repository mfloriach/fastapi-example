import unittest

from fastapi.testclient import TestClient

from app.core.database import get_session
from app.core.test_database import override_get_session
from app.main import app
from app.middlewares.test_verify_token import test_verify_token
from app.middlewares.verify_token import verify_token

from ..models import BookCreate, BookUpdate

client = TestClient(app)

app.dependency_overrides[get_session] = override_get_session
app.dependency_overrides[verify_token] = test_verify_token

class CreateBook(unittest.TestCase):
    def test_ok(self):
        book = BookCreate(
            title="books to do",
            num_pages=30,
            language=1,
            prize=20  
        )

        response = client.post("/api/v1", json=book.model_dump(mode='json'))
        self.assertEqual(response.status_code, 201)
        data = response.json()
        
        self.assertEqual(type(data["id"]), int, "Incorrect input")
        self.assertEqual(type(data["created_at"]), str, "Incorrect input")
        self.assertEqual(data["title"], book.title)

class GetBook(unittest.TestCase):
    def test_params_validation(self):
        response = client.get("/api/v1/-12")
        self.assertEqual(response.status_code, 422)

    def test_not_found(self):
        response = client.get("/api/v1/12")
        self.assertEqual(response.status_code, 404)

    def test_ok(self):
        book = BookCreate(
            title="books to do",
            num_pages=30,
            language=1,
            prize=20  
        )

        response = client.post("/api/v1", json=book.model_dump(mode='json'))
        data_created = response.json()

        response = client.get(f"/api/v1/{data_created["id"]}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], data_created["id"])
        self.assertEqual(data["updated_at"], data_created['updated_at'])

class DeleteBook(unittest.TestCase):
    def test_params_validation(self):
        response = client.delete("/api/v1/-12")
        self.assertEqual(response.status_code, 422)

    def test_not_found(self):
        response = client.delete("/api/v1/12")
        self.assertEqual(response.status_code, 404)
    
class UpdateBook(unittest.TestCase):
    def test_params_validation(self):
        book = BookUpdate(
            title="books to do",
            num_pages=30,
            language=1,
            prize=20  
        )

        response = client.put("/api/v1/-12", json=book.model_dump(mode='json'))
        self.assertEqual(response.status_code, 422)

    def test_not_found(self):
        book = BookUpdate(
            title="books to do",
            num_pages=30,
            language=1,
            prize=20  
        )

        response = client.put("/api/v1/12", json=book.model_dump(mode='json'))
        self.assertEqual(response.status_code, 404)

class GetBooks(unittest.TestCase):
    def test_ok(self):
        book = BookCreate(
            title="books to do",
            num_pages=30,
            language=1,
            prize=20  
        )

        response = client.post("/api/v1", json=book.model_dump(mode='json'))
        self.assertEqual(response.status_code, 201)
        data = response.json()
        
        self.assertEqual(type(data["id"]), int, "Incorrect input")
        self.assertEqual(type(data["created_at"]), str, "Incorrect input")
        self.assertEqual(data["title"], book.title)