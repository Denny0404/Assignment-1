import unittest
from user import Database, UserService, User
import os

class TestDatabase(unittest.TestCase):
    """Tests for the Database class"""

    def setUp(self):
        """Setup test database"""
        self.db = Database(":memory:")  # Use in-memory DB for tests

    def test_insert_user(self):
        """Test inserting a user"""
        user_id = self.db.insert_user("Alice", 25)
        self.assertIsInstance(user_id, int)
        user = self.db.get_user(user_id)
        self.assertEqual(user, (user_id, "Alice", 25))

    def test_update_user(self):
        """Test updating an existing user"""
        user_id = self.db.insert_user("Bob", 30)
        rows_updated = self.db.update_user(user_id, "Bob Updated", 35)
        self.assertEqual(rows_updated, 1)
        user = self.db.get_user(user_id)
        self.assertEqual(user, (user_id, "Bob Updated", 35))

    def test_update_non_existent_user(self):
        """Test updating a non-existent user"""
        rows_updated = self.db.update_user(999, "Fake Name", 40)
        self.assertEqual(rows_updated, 0)  # No updates should happen

    def test_delete_user(self):
        """Test deleting an existing user"""
        user_id = self.db.insert_user("Charlie", 40)
        rows_deleted = self.db.delete_user(user_id)
        self.assertEqual(rows_deleted, 1)
        user = self.db.get_user(user_id)
        self.assertIsNone(user)  # User should not exist anymore

    def test_delete_non_existent_user(self):
        """Test deleting a non-existent user"""
        rows_deleted = self.db.delete_user(999)
        self.assertEqual(rows_deleted, 0)  # No rows should be deleted

    def test_database_creation(self):
        """Ensure the users table is created properly"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)  # Table should exist


class TestUserService(unittest.TestCase):
    """Tests for UserService class"""

    def setUp(self):
        self.db = Database(":memory:")
        self.user_service = UserService(self.db)

    def test_create_user(self):
        response, status_code = self.user_service.create_user("John Doe", 30)
        self.assertEqual(status_code, 201)
        self.assertIn("user_id", response)
        self.assertEqual(response["name"], "John Doe")
        self.assertEqual(response["age"], 30)

    def test_get_user_found(self):
        user_id = self.db.insert_user("John Doe", 30)
        response, status_code = self.user_service.get_user(user_id)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"user_id": user_id, "name": "John Doe", "age": 30})

    def test_get_user_not_found(self):
        response, status_code = self.user_service.get_user(99)
        self.assertEqual(status_code, 404)
        self.assertEqual(response, {"error": "User not found"})

    def test_update_user(self):
        user_id = self.db.insert_user("Mark", 22)
        response, status_code = self.user_service.update_user(user_id, "Mark Updated", 23)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"message": "User updated successfully"})

    def test_update_user_not_found(self):
        response, status_code = self.user_service.update_user(99, "No Name", 40)
        self.assertEqual(status_code, 404)
        self.assertEqual(response, {"error": "User not found"})

    def test_delete_user(self):
        user_id = self.db.insert_user("Tom", 50)
        response, status_code = self.user_service.delete_user(user_id)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"message": "User deleted successfully"})

    def test_delete_user_not_found(self):
        response, status_code = self.user_service.delete_user(99)
        self.assertEqual(status_code, 404)
        self.assertEqual(response, {"error": "User not found"})


class TestUserModel(unittest.TestCase):
    """Tests for the User class"""

    def test_user_creation(self):
        user = User(1, "Alice", 25)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.age, 25)


if __name__ == "__main__":
    unittest.main()
