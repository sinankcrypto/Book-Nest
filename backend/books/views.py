from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, SAFE_METHODS
)
from rest_framework.filters import (
    SearchFilter, OrderingFilter
)

from .models import (
    Book, ReadingList, ReadingListBook
)
from .serializers import (
    BookSerializer, ReadingListBookSerializer, ReadingListSerializer,
    AddBookSerializer, ReorderBookSerializer
)
from .permissions import IsOwnerOrReadOnly
from .utils import reorder_positons

from drf_spectacular.utils import extend_schema_view

from django.utils import timezone
from django.db import transaction

from .docs import (
    book_list_schema,
    book_create_schema,
    book_retrieve_schema,
    book_update_schema,
    book_partial_update_schema,
    book_delete_schema,
    reading_list_list_schema,
    reading_list_create_schema,
    reading_list_retrieve_schema,
    reading_list_update_schema,
    reading_list_partial_update_schema,
    reading_list_delete_schema,
    reading_list_books_list_schema,
    reading_list_book_add_schema,
    reading_list_book_delete_schema,
    reading_list_book_reorder_schema
)

# Create your views here.

@extend_schema_view(
    get=book_list_schema,
    post=book_create_schema,
)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.filter(is_deleted=False)

    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "title",
        "author",
        "genre",
    ]

    filterset_fields = [
        "genre",
    ]

    ordering_fields = [
        "created_at",
        "publication_date",
        "title",
    ]

    ordering = [
        "-created_at"
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema_view(
    get=book_retrieve_schema,
    put=book_update_schema,
    patch=book_partial_update_schema,
    delete=book_delete_schema,
)
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.filter(is_deleted=False)

    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["is_deleted", "deleted_at"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Book deleted successfully."},
            status=status.HTTP_200_OK
        )

@extend_schema_view(
    get=reading_list_list_schema,
    post=reading_list_create_schema,
)
class ReadingListListCreateView(generics.ListCreateAPIView):
    serializer_class = ReadingListSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

@extend_schema_view(
    get=reading_list_retrieve_schema,
    put=reading_list_update_schema,
    patch=reading_list_partial_update_schema,
    delete=reading_list_delete_schema,
)    
class ReadingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReadingListSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return ReadingList.objects.filter(owner=self.request.user)

@extend_schema_view(
    get=reading_list_books_list_schema,
    post=reading_list_book_add_schema,
)   
class ReadingListBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reading_list = get_object_or_404(ReadingList, pk=pk, owner=request.user)

        books = ReadingListBook.objects.filter(
            reading_list=reading_list,
            book__is_deleted=False
        ).order_by("position")

        serializer = ReadingListBookSerializer(books, many=True)

        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = AddBookSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        reading_list = get_object_or_404(ReadingList, pk=pk, owner=request.user)
        book = get_object_or_404(
            Book,
            pk=serializer.validated_data["book_id"],
            is_deleted=False
        )

        if ReadingListBook.objects.filter(reading_list=reading_list, book=book).exists():
            return Response(
                {"detail": "Book already exists in reading list."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        last_position = ReadingListBook.objects.filter(reading_list=reading_list).count()

        relation = ReadingListBook.objects.create(
            reading_list=reading_list,
            book=book,
            position=last_position + 1
        )

        return Response(ReadingListBookSerializer(relation).data, status=status.HTTP_201_CREATED)

@extend_schema_view(
    delete=reading_list_book_delete_schema,
)
class ReadingListBookDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, book_id):
        relation = get_object_or_404(
            ReadingListBook,
            reading_list__id=pk,
            reading_list__owner=request.user,
            book_id=book_id
        )

        reading_list = relation.reading_list

        relation.delete()

        reorder_positons(reading_list)

        return Response(
            {
                "detail": "Book removed from reading list."
            },
            status=status.HTTP_200_OK
        )

@extend_schema_view(
    patch=reading_list_book_reorder_schema,
)
class ReadingListBookReorderView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, book_id):
        serializer = ReorderBookSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        relation = get_object_or_404(
            ReadingListBook,
            reading_list__id=pk,
            reading_list__owner=request.user,
            book_id=book_id
        )

        reading_list = relation.reading_list

        books = list(
            ReadingListBook.objects
            .filter(reading_list=reading_list)
            .order_by("position")
        )

        new_position = serializer.validated_data["position"]

        if new_position > len(books):
            return Response(
                {
                    "detail": (
                        "Position is outside the "
                        "reading list range."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Remove the book from its current position
        books.remove(relation)

        # Insert it at the new position
        books.insert(
            new_position - 1,
            relation
        )

        with transaction.atomic():
            #offset to avoid conflict during update due to unique constraint on book and position
            max_position = max(
                book.position
                for book in books
            )

            temp_offset = (
                max_position
                + len(books)
                + 1
            )

            # Phase 1: temporary positions
            for index, book in enumerate(
                books,
                start=1
            ):
                book.position = (
                    temp_offset + index
                )

            ReadingListBook.objects.bulk_update(
                books,
                ["position"]
            )

            # Phase 2: final positions
            for index, book in enumerate(
                books,
                start=1
            ):
                book.position = index

            ReadingListBook.objects.bulk_update(
                books,
                ["position"]
            )

        return Response(
            ReadingListBookSerializer(
                relation
            ).data,
            status=status.HTTP_200_OK
        )
    