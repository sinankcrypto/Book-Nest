from .models import Book
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

