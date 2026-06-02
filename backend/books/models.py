from django.db import models
from django.conf import settings

# Create your models here.

class Book(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books"
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    pdf_file = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class ReadingList(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_lists"
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(
        ReadingList,
        on_delete=models.CASCADE,
        related_name="reading_list_books"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]

        unique_together = [
            ("reading_list", "book"),
            ("reading_list", "position")
        ]

    def __str__(self):
        return (
            f"{self.reading_list.name}"
            f" - "
            f"{self.book.title}"
        )