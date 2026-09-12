import re
from rest_framework import serializers
from .models import Book, ReadingList, ReadingListBook

class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    title = serializers.CharField(required=True, allow_blank=False, max_length=255)
    author = serializers.CharField(required=True, allow_blank=False, max_length=255)
    genre = serializers.CharField(required=True, allow_blank=False, max_length=100)
    publication_date = serializers.DateField(required=True)
    description = serializers.CharField(required=True, allow_blank=False)
    pdf_file = serializers.FileField(required=True, allow_null=False)
    cover_image = serializers.ImageField(required=True, allow_null=False)

    class Meta:
        model = Book
        fields = [
            "id",
            "owner",
            "title",
            "author",
            "genre",
            "publication_date",
            "description",
            "pdf_file",
            "cover_image",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if not re.match(r"^[a-zA-Z0-9\s.,!?:;\-\'\"()]+$", value):
            raise serializers.ValidationError(
                "Title contains invalid characters. Only letters, numbers, spaces, and basic punctuation are allowed."
            )
        
        # Case-sensitive duplicate check
        query = Book.objects.filter(title__iexact=value, is_deleted=False)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if any(book.title == value for book in query):
            raise serializers.ValidationError("A book with this title already exists.")
        
        return value

    def validate_author(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError("Author name must be at least 2 characters long.")
        if not re.match(r"^[a-zA-Z\s.\'\-]+$", value):
            raise serializers.ValidationError(
                "Author can only contain letters, spaces, dots, hyphens, and apostrophes."
            )
        return value

    def validate_genre(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Genre cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError("Genre must be at least 2 characters long.")
        if not re.match(r"^[a-zA-Z\s\-&]+$", value):
            raise serializers.ValidationError(
                "Genre can only contain letters, spaces, hyphens, and ampersands."
            )
        return value

    def validate_description(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")
        if len(value) < 5:
            raise serializers.ValidationError("Description must be at least 5 characters long.")
        return value

    def validate_pdf_file(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files (.pdf) are allowed for pdf_file.")
        return value

    def validate_cover_image(self, value):
        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError(
                "Cover image must have a valid extension (.jpg, .jpeg, .png, .webp)."
            )
        return value


class ReadingListBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="book.title", read_only=True)
    author = serializers.CharField(source="book.author", read_only=True)
    cover_image = serializers.ImageField(source="book.cover_image", read_only=True)

    class Meta:
        model = ReadingListBook

        fields = [
            "id",
            "book",
            "title",
            "author",
            "cover_image",
            "position",
        ]

class ReadingListSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = ReadingList

        fields = [
            "id",
            "name",
            "books",
            "created_at",
            "book_count"
        ]

    def get_books(self, obj):
        active_books = obj.reading_list_books.filter(book__is_deleted=False).order_by("position")
        return ReadingListBookSerializer(active_books, many=True).data

    def get_book_count(self, obj):
        return obj.reading_list_books.filter(book__is_deleted=False).count()

class AddBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

class ReorderBookSerializer(serializers.Serializer):
    position = serializers.IntegerField(min_value=1)
