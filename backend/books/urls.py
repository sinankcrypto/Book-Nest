from django.urls import path
from .views import (
    BookListCreateView, BookDetailView, ReadingListListCreateView, ReadingListDetailView,
    ReadingListBookDeleteView, ReadingListBooksView
)

urlpatterns = [
    path("", BookListCreateView.as_view()),
    path("<int:pk>/", BookDetailView.as_view()),
    path("reading-lists/", ReadingListListCreateView.as_view(), name="reading-list-list"),
    path("reading-lists/<int:pk>/", ReadingListDetailView.as_view(), name="reading-list-detail"),
    path("reading-lists/<int:pk>/books/", ReadingListBooksView.as_view(),name="reading-list-books"),
    path(
        "reading-lists/<int:pk>/books/<int:book_id>/",
        ReadingListBookDeleteView.as_view(),
        name="reading-list-book-delete"
    ),

]
