from django.contrib import admin
from .models import Book, ReadingList, ReadingListBook

# Register your models here.

admin.site.register(Book)

admin.site.register(ReadingList)
admin.site.register(ReadingListBook)