import io
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image

from .models import Book, ReadingList, ReadingListBook
from .serializers import BookSerializer

User = get_user_model()

STORAGES_FOR_TEST = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

def create_dummy_image(filename="cover.jpg"):
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color=(73, 109, 137))
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile(filename, file.read(), content_type="image/jpeg")

def create_dummy_pdf(filename="sample.pdf"):
    return SimpleUploadedFile(filename, b"%PDF-1.4 dummy pdf content", content_type="application/pdf")


@override_settings(STORAGES=STORAGES_FOR_TEST)
class BookValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testauthor",
            email="author@example.com",
            password="StrongPassword!#2026",
            is_active=True
        )

    def test_valid_book_data(self):
        data = {
            "title": "Clean Architecture",
            "author": "Robert C. Martin",
            "genre": "Software Engineering",
            "publication_date": "2017-09-20",
            "description": "A comprehensive guide to software structure and design.",
        }
        files = {
            "pdf_file": create_dummy_pdf(),
            "cover_image": create_dummy_image(),
        }
        serializer = BookSerializer(data={**data, **files})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_missing_required_fields(self):
        # Empty dictionary to verify all fields are required
        serializer = BookSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("author", serializer.errors)
        self.assertIn("genre", serializer.errors)
        self.assertIn("publication_date", serializer.errors)
        self.assertIn("description", serializer.errors)
        self.assertIn("pdf_file", serializer.errors)
        self.assertIn("cover_image", serializer.errors)

    def test_invalid_author_regex(self):
        data = {
            "title": "Clean Code",
            "author": "Robert 123 @Martin!",
            "genre": "Programming",
            "publication_date": "2008-08-01",
            "description": "A handbook of agile software craftsmanship.",
            "pdf_file": create_dummy_pdf(),
            "cover_image": create_dummy_image(),
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("author", serializer.errors)

    def test_invalid_genre_regex(self):
        data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "genre": "Prog_123$!",
            "publication_date": "2008-08-01",
            "description": "A handbook of agile software craftsmanship.",
            "pdf_file": create_dummy_pdf(),
            "cover_image": create_dummy_image(),
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("genre", serializer.errors)

    def test_invalid_pdf_extension(self):
        invalid_pdf = SimpleUploadedFile("sample.txt", b"not a pdf", content_type="text/plain")
        data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "genre": "Programming",
            "publication_date": "2008-08-01",
            "description": "A handbook of agile software craftsmanship.",
            "pdf_file": invalid_pdf,
            "cover_image": create_dummy_image(),
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("pdf_file", serializer.errors)

    def test_invalid_cover_image_extension(self):
        invalid_img = SimpleUploadedFile("cover.txt", b"not an image", content_type="text/plain")
        data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "genre": "Programming",
            "publication_date": "2008-08-01",
            "description": "A handbook of agile software craftsmanship.",
            "pdf_file": create_dummy_pdf(),
            "cover_image": invalid_img,
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cover_image", serializer.errors)

    def test_case_sensitive_duplicate_title(self):
        Book.objects.create(
            owner=self.user,
            title="Refactoring",
            author="Martin Fowler",
            genre="Computer Science",
            publication_date="1999-07-08",
            description="Improving the design of existing code.",
            pdf_file=create_dummy_pdf(),
            cover_image=create_dummy_image()
        )

        # Exact case match should fail
        exact_duplicate = {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "genre": "Computer Science",
            "publication_date": "1999-07-08",
            "description": "Improving the design of existing code duplicate.",
            "pdf_file": create_dummy_pdf(),
            "cover_image": create_dummy_image(),
        }
        serializer1 = BookSerializer(data=exact_duplicate)
        self.assertFalse(serializer1.is_valid())
        self.assertIn("title", serializer1.errors)

        # Different case is allowed for case-sensitive duplicate check
        different_case = {
            "title": "refactoring",
            "author": "Martin Fowler",
            "genre": "Computer Science",
            "publication_date": "1999-07-08",
            "description": "Improving the design of existing code in lowercase.",
            "pdf_file": create_dummy_pdf(),
            "cover_image": create_dummy_image(),
        }
        serializer2 = BookSerializer(data=different_case)
        self.assertTrue(serializer2.is_valid(), serializer2.errors)


@override_settings(STORAGES=STORAGES_FOR_TEST)
class BookSoftDeleteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="owner_user",
            email="owner@example.com",
            password="StrongPassword!#2026",
            is_active=True
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other@example.com",
            password="StrongPassword!#2026",
            is_active=True
        )

        self.book = Book.objects.create(
            owner=self.owner,
            title="Design Patterns",
            author="Gang of Four",
            genre="Software Architecture",
            publication_date="1994-10-31",
            description="Elements of Reusable Object-Oriented Software.",
            pdf_file=create_dummy_pdf(),
            cover_image=create_dummy_image()
        )

    def test_soft_delete_by_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Book deleted successfully.")

        # Verify soft deletion in database
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_deleted)
        self.assertIsNotNone(self.book.deleted_at)

    def test_soft_deleted_book_not_in_list_or_detail(self):
        self.book.is_deleted = True
        self.book.save()

        self.client.force_authenticate(user=self.owner)

        # Check list endpoint
        list_response = self.client.get("/api/books/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        results = list_response.data.get("results", list_response.data)
        self.assertEqual(len(results), 0)

        # Check detail endpoint
        detail_response = self.client.get(f"/api/books/{self.book.id}/")
        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_permission_denied_for_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.book.refresh_from_db()
        self.assertFalse(self.book.is_deleted)

    def test_cannot_add_soft_deleted_book_to_reading_list(self):
        self.book.is_deleted = True
        self.book.save()

        reading_list = ReadingList.objects.create(
            owner=self.owner,
            name="My Favorites"
        )

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            f"/api/books/reading-lists/{reading_list.id}/books/",
            {"book_id": self.book.id}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
