from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from .serializers import RegisterSerializer

class RegisterPasswordValidationTest(TestCase):
    def test_valid_password(self):
        serializer = RegisterSerializer(data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_short_password(self):
        serializer = RegisterSerializer(data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_common_password(self):
        serializer = RegisterSerializer(data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_entirely_numeric_password(self):
        serializer = RegisterSerializer(data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "1234567890"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_password_similar_to_username(self):
        serializer = RegisterSerializer(data={
            "username": "johnsmith123",
            "email": "johnsmith123@example.com",
            "password": "johnsmith123"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class RegisterUsernameValidationTest(TestCase):
    def test_invalid_username_characters(self):
        serializer = RegisterSerializer(data={
            "username": "test user!",
            "email": "test@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_short_username(self):
        serializer = RegisterSerializer(data={
            "username": "ab",
            "email": "test@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_case_insensitive_duplicate_username(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username="ExistingUser", email="first@example.com", password="StrongSecretPass!#2026")

        serializer = RegisterSerializer(data={
            "username": "existinguser",
            "email": "second@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_username_without_alphabets(self):
        # Numeric only
        serializer1 = RegisterSerializer(data={
            "username": "123456",
            "email": "num@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer1.is_valid())
        self.assertIn("username", serializer1.errors)

        # Underscores only
        serializer2 = RegisterSerializer(data={
            "username": "____",
            "email": "und@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer2.is_valid())
        self.assertIn("username", serializer2.errors)

        # Underscores and numbers only
        serializer3 = RegisterSerializer(data={
            "username": "_123_456_",
            "email": "undnum@example.com",
            "password": "StrongSecretPass!#2026"
        })
        self.assertFalse(serializer3.is_valid())
        self.assertIn("username", serializer3.errors)


class EditProfileAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="original_user",
            email="original@example.com",
            password="StrongSecretPass!#2026",
            is_active=True
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other@example.com",
            password="StrongSecretPass!#2026",
            is_active=True
        )

    def test_edit_profile_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch("/api/auth/profile/", {"username": "new_valid_username"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Profile updated successfully.")
        self.assertEqual(response.data["user"]["username"], "new_valid_username")

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_valid_username")

    def test_edit_profile_same_username(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch("/api/auth/profile/", {"username": "original_user"})
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_duplicate_username(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch("/api/auth/profile/", {"username": "other_user"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_edit_profile_invalid_username(self):
        self.client.force_authenticate(user=self.user)
        # Without letters
        response = self.client.patch("/api/auth/profile/", {"username": "123456"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

        # Invalid characters
        response2 = self.client.patch("/api/auth/profile/", {"username": "user!name"})
        self.assertEqual(response2.status_code, 400)
        self.assertIn("username", response2.data)

    def test_edit_profile_unauthenticated(self):
        response = self.client.patch("/api/auth/profile/", {"username": "new_username"})
        self.assertEqual(response.status_code, 401)



