from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)

from .serializers import (
    BookSerializer, 
    ReadingListSerializer,
    ReadingListBookSerializer,
    ReorderBookSerializer,
    AddBookSerializer
)


# ============================================================
# BOOK LIST
# ============================================================

book_list_schema = extend_schema(
    summary="List all books",
    description=(
        "Returns a paginated list of all books available "
        "in BookNest. All authenticated users can access "
        "books created by any user.\n\n"
        "Supports searching by title, author, or genre; "
        "filtering by genre; and ordering by creation date, "
        "publication date, or title."
    ),
    parameters=[
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Search books by title, author, or genre."
            ),
            examples=[
                OpenApiExample(
                    "Search by title",
                    value="django",
                )
            ],
        ),
        OpenApiParameter(
            name="genre",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Filter books by genre."
            ),
            examples=[
                OpenApiExample(
                    "Filter by genre",
                    value="Programming",
                )
            ],
        ),
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Order results by created_at, "
                "publication_date, or title. "
                "Prefix the field with '-' for descending order."
            ),
            examples=[
                OpenApiExample(
                    "Newest first",
                    value="-created_at",
                ),
                OpenApiExample(
                    "Alphabetical order",
                    value="title",
                ),
            ],
        ),
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "The page number to retrieve."
            ),
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=BookSerializer(many=True),
            description=(
                "A paginated list of books."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
    },
    tags=["Books"],
)


# ============================================================
# BOOK CREATE
# ============================================================

book_create_schema = extend_schema(
    summary="Create a new book",
    description=(
        "Creates a new book and uploads its PDF file and "
        "optional cover image. The authenticated user becomes "
        "the owner of the book."
    ),
    request={
        "multipart/form-data": BookSerializer,
    },
    responses={
        201: OpenApiResponse(
            response=BookSerializer,
            description="Book created successfully.",
        ),
        400: OpenApiResponse(
            description=(
                "The submitted book data is invalid."
            ),
            examples=[
                OpenApiExample(
                    "Validation error",
                    value={
                        "title": [
                            "This field is required."
                        ]
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
    },
    tags=["Books"],
)


# ============================================================
# BOOK RETRIEVE
# ============================================================

book_retrieve_schema = extend_schema(
    summary="Get a book",
    description=(
        "Returns the details of a specific book. "
        "Any authenticated user can retrieve a book."
    ),
    responses={
        200: OpenApiResponse(
            response=BookSerializer,
            description="Book details.",
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description="The requested book was not found.",
            examples=[
                OpenApiExample(
                    "Book not found",
                    value={
                        "detail": "Not found."
                    },
                )
            ],
        ),
    },
    tags=["Books"],
)


# ============================================================
# BOOK UPDATE
# ============================================================

book_update_schema = extend_schema(
    summary="Update a book",
    description=(
        "Updates an existing book. Only the owner of the book "
        "can modify it. The request may include a new PDF file "
        "or cover image."
    ),
    request={
        "multipart/form-data": BookSerializer,
    },
    responses={
        200: OpenApiResponse(
            response=BookSerializer,
            description="Book updated successfully.",
        ),
        400: OpenApiResponse(
            description=(
                "The submitted book data is invalid."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user is not the owner "
                "of this book."
            ),
            examples=[
                OpenApiExample(
                    "Permission denied",
                    value={
                        "detail": (
                            "You do not have permission "
                            "to perform this action."
                        )
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            description="The requested book was not found.",
        ),
    },
    tags=["Books"],
)


# ============================================================
# BOOK PARTIAL UPDATE
# ============================================================

book_partial_update_schema = extend_schema(
    summary="Partially update a book",
    description=(
        "Partially updates an existing book. "
        "Only the owner of the book can modify it. "
        "Only the fields included in the request are updated."
    ),
    request={
        "multipart/form-data": BookSerializer,
    },
    responses={
        200: OpenApiResponse(
            response=BookSerializer,
            description="Book updated successfully.",
        ),
        400: OpenApiResponse(
            description=(
                "The submitted book data is invalid."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user is not the owner "
                "of this book."
            ),
        ),
        404: OpenApiResponse(
            description="The requested book was not found.",
        ),
    },
    tags=["Books"],
)


# ============================================================
# BOOK DELETE
# ============================================================

book_delete_schema = extend_schema(
    summary="Delete a book",
    description=(
        "Deletes an existing book. Only the owner of the "
        "book can delete it."
    ),
    request=None,
    responses={
        204: OpenApiResponse(
            description="Book deleted successfully.",
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user is not the owner "
                "of this book."
            ),
            examples=[
                OpenApiExample(
                    "Permission denied",
                    value={
                        "detail": (
                            "You do not have permission "
                            "to perform this action."
                        )
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            description="The requested book was not found.",
        ),
    },
    tags=["Books"],
)

# ============================================================
# READING LIST - LIST
# ============================================================

reading_list_list_schema = extend_schema(
    summary="List user's reading lists",
    description=(
        "Returns all reading lists belonging to the "
        "currently authenticated user. "
        "Users can only access their own reading lists."
    ),
    responses={
        200: OpenApiResponse(
            response=ReadingListSerializer(many=True),
            description=(
                "A list of the authenticated user's "
                "reading lists."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
    },
    tags=["Reading Lists"],
)


# ============================================================
# READING LIST - CREATE
# ============================================================

reading_list_create_schema = extend_schema(
    summary="Create a reading list",
    description=(
        "Creates a new reading list for the currently "
        "authenticated user. The authenticated user is "
        "automatically assigned as the owner of the "
        "reading list."
    ),
    request=ReadingListSerializer,
    responses={
        201: OpenApiResponse(
            response=ReadingListSerializer,
            description=(
                "Reading list created successfully."
            ),
        ),
        400: OpenApiResponse(
            description=(
                "The submitted reading list data is invalid."
            ),
            examples=[
                OpenApiExample(
                    "Validation error",
                    value={
                        "name": [
                            "This field is required."
                        ]
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
    },
    tags=["Reading Lists"],
)


# ============================================================
# READING LIST - RETRIEVE
# ============================================================

reading_list_retrieve_schema = extend_schema(
    summary="Get a reading list",
    description=(
        "Returns the details of a specific reading list "
        "belonging to the currently authenticated user. "
        "The response includes the books in the reading "
        "list and the total number of books."
    ),
    responses={
        200: OpenApiResponse(
            response=ReadingListSerializer,
            description=(
                "Reading list details."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist or does "
                "not belong to the authenticated user."
            ),
            examples=[
                OpenApiExample(
                    "Reading list not found",
                    value={
                        "detail": "Not found."
                    },
                )
            ],
        ),
    },
    tags=["Reading Lists"],
)


# ============================================================
# READING LIST - UPDATE
# ============================================================

reading_list_update_schema = extend_schema(
    summary="Update a reading list",
    description=(
        "Updates an existing reading list. "
        "Only the owner of the reading list can update it."
    ),
    request=ReadingListSerializer,
    responses={
        200: OpenApiResponse(
            response=ReadingListSerializer,
            description=(
                "Reading list updated successfully."
            ),
        ),
        400: OpenApiResponse(
            description=(
                "The submitted reading list data is invalid."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user does not have "
                "permission to modify this reading list."
            ),
            examples=[
                OpenApiExample(
                    "Permission denied",
                    value={
                        "detail": (
                            "You do not have permission "
                            "to perform this action."
                        )
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist or does "
                "not belong to the authenticated user."
            ),
        ),
    },
    tags=["Reading Lists"],
)


# ============================================================
# READING LIST - PARTIAL UPDATE
# ============================================================

reading_list_partial_update_schema = extend_schema(
    summary="Partially update a reading list",
    description=(
        "Partially updates an existing reading list. "
        "Only the owner of the reading list can modify it. "
        "Only the fields included in the request are updated."
    ),
    request=ReadingListSerializer,
    responses={
        200: OpenApiResponse(
            response=ReadingListSerializer,
            description=(
                "Reading list updated successfully."
            ),
        ),
        400: OpenApiResponse(
            description=(
                "The submitted reading list data is invalid."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user does not have "
                "permission to modify this reading list."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist or does "
                "not belong to the authenticated user."
            ),
        ),
    },
    tags=["Reading Lists"],
)


# ============================================================
# READING LIST - DELETE
# ============================================================

reading_list_delete_schema = extend_schema(
    summary="Delete a reading list",
    description=(
        "Deletes an existing reading list. "
        "Only the owner of the reading list can delete it."
    ),
    request=None,
    responses={
        204: OpenApiResponse(
            description=(
                "Reading list deleted successfully."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        403: OpenApiResponse(
            description=(
                "The authenticated user does not have "
                "permission to delete this reading list."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist or does "
                "not belong to the authenticated user."
            ),
        ),
    },
    tags=["Reading Lists"],
)

# ============================================================
# READING LIST BOOKS - LIST
# ============================================================

reading_list_books_list_schema = extend_schema(
    summary="List books in a reading list",
    description=(
        "Returns all books belonging to a specific reading "
        "list owned by the authenticated user. Books are "
        "returned in their current reading-list order based "
        "on their position."
    ),
    responses={
        200: OpenApiResponse(
            response=ReadingListBookSerializer(many=True),
            description=(
                "Books in the reading list, ordered by position."
            ),
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist or does "
                "not belong to the authenticated user."
            ),
            examples=[
                OpenApiExample(
                    "Reading list not found",
                    value={
                        "detail": "Not found."
                    },
                )
            ],
        ),
    },
    tags=["Reading List Books"],
)


# ============================================================
# READING LIST BOOKS - ADD
# ============================================================

reading_list_book_add_schema = extend_schema(
    summary="Add a book to a reading list",
    description=(
        "Adds an existing book to a reading list owned by "
        "the authenticated user. The book is automatically "
        "placed at the end of the reading list. "
        "A book cannot be added to the same reading list "
        "more than once."
    ),
    request=AddBookSerializer,
    responses={
        201: OpenApiResponse(
            response=ReadingListBookSerializer,
            description=(
                "Book added to the reading list successfully."
            ),
        ),
        400: OpenApiResponse(
            description=(
                "The book is already present in the reading "
                "list or the request data is invalid."
            ),
            examples=[
                OpenApiExample(
                    "Book already exists",
                    value={
                        "detail": (
                            "Book already exists in "
                            "reading list."
                        )
                    },
                ),
                OpenApiExample(
                    "Invalid request",
                    value={
                        "book_id": [
                            "This field is required."
                        ]
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list or requested book "
                "was not found."
            ),
        ),
    },
    tags=["Reading List Books"],
)


# ============================================================
# READING LIST BOOKS - DELETE
# ============================================================

reading_list_book_delete_schema = extend_schema(
    summary="Remove a book from a reading list",
    description=(
        "Removes a book from a reading list owned by the "
        "authenticated user. After removal, the positions "
        "of the remaining books are automatically reordered "
        "to maintain a continuous sequence."
    ),
    request=None,
    responses={
        200: OpenApiResponse(
            description=(
                "Book removed from the reading list "
                "successfully."
            ),
            examples=[
                OpenApiExample(
                    "Book removed",
                    value={
                        "detail": (
                            "Book removed from reading list."
                        )
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist, does not "
                "belong to the authenticated user, or the "
                "book is not in the reading list."
            ),
        ),
    },
    tags=["Reading List Books"],
)

reading_list_book_reorder_schema = extend_schema(
    summary="Reorder a book in a reading list",
    description=(
        "Moves a book to a specified position within a "
        "reading list owned by the authenticated user. "
        "The positions of other books are automatically "
        "adjusted to maintain a continuous ordering."
    ),
    request=ReorderBookSerializer,
    responses={
        200: OpenApiResponse(
            response=ReadingListBookSerializer,
            description=(
                "Book reordered successfully."
            ),
        ),
        400: OpenApiResponse(
            description=(
                "The requested position is invalid or "
                "outside the reading list range."
            ),
            examples=[
                OpenApiExample(
                    "Invalid position",
                    value={
                        "detail": (
                            "Position is outside the "
                            "reading list range."
                        )
                    },
                ),
                OpenApiExample(
                    "Invalid request",
                    value={
                        "position": [
                            "Ensure this value is "
                            "greater than or equal to 1."
                        ]
                    },
                ),
            ],
        ),
        401: OpenApiResponse(
            description=(
                "Authentication credentials are missing "
                "or invalid."
            ),
        ),
        404: OpenApiResponse(
            description=(
                "The reading list does not exist, does not "
                "belong to the authenticated user, or the "
                "book is not in the reading list."
            ),
        ),
    },
    tags=["Reading List Books"],
)
