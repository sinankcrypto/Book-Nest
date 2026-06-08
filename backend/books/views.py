from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated, SAFE_METHODS
)

from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("-created_at")

    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    serializer_class = BookSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
