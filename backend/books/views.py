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

# Create your views here.

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()

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

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class ReadingListListCreateView(generics.ListCreateAPIView):
    serializer_class = ReadingListSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReadingList.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
class ReadingListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReadingListSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return ReadingList.objects.filter(owner=self.request.user)
    
class ReadingListBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reading_list = get_object_or_404(ReadingList, pk=pk, owner=request.user)

        books = ReadingListBook.objects.filter(reading_list=reading_list).order_by("position")

        serializer = ReadingListBookSerializer(books, many=True)

        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = AddBookSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        reading_list = get_object_or_404(ReadingList, pk=pk, owner=request.user)
        book = get_object_or_404(Book, pk=serializer.validated_data["book_id"])

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