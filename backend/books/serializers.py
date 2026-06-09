from .models import Book, ReadingList, ReadingListBook
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

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
    books = ReadingListBookSerializer(source="reading_list_books", many=True, read_only=True)

    class Meta:
        model = ReadingList

        fields = [
            "id",
            "name",
            "books",
            "created_at",
        ]

class AddBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

class ReorderBookSerializer(serializers.Serializer):
    position = serializers.IntegerField(min_value=1)
