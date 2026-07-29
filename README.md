# BookNest

BookNest is a full-stack book management and reading-list application built with **Django REST Framework** and **React**.

The application allows users to create accounts, verify their email using OTP, manage their profiles, upload and manage books, and organise books into personalised reading lists.

BookNest uses **JWT authentication stored in HttpOnly cookies** and **Cloudinary** for storing book PDF files and cover images.

---

## Features

### User Management

* User registration
* Unique username and email address
* Email OTP verification
* OTP resend functionality
* User login and logout
* JWT-based authentication
* JWT access and refresh tokens stored in HttpOnly cookies
* Automatic access-token refresh
* Profile retrieval
* Authentication and authorization using Django REST Framework permissions

### Book Management

* Create and upload books
* View all available books
* Retrieve individual book details
* Update books
* Delete books
* Upload PDF files for books
* Upload optional book cover images
* Store uploaded media using Cloudinary
* Book metadata including:

  * Title
  * Author
  * Genre
  * Publication date
  * Description
  * PDF file
  * Cover image
* Search books by:

  * Title
  * Author
  * Genre
* Filter books by genre
* Order books by:

  * Creation date
  * Publication date
  * Title
* Pagination support

All authenticated users can access the available books, while book modification and deletion are restricted according to ownership permissions.

### Reading Lists

* Create personalised reading lists
* View user's reading lists
* Retrieve individual reading lists
* Update reading lists
* Delete reading lists
* Display the number of books in each reading list
* View books contained in a reading list
* Add books to reading lists
* Remove books from reading lists
* Prevent duplicate books in the same reading list
* Maintain book ordering using position values
* Reorder books within a reading list
* Automatically reorder remaining books after removing a book

### Error Handling and Validation

* Serializer-level validation
* Authentication and authorization checks
* Validation for duplicate usernames and emails
* OTP expiration and validation
* Invalid credential handling
* Duplicate book prevention in reading lists
* Invalid reading-list position handling
* Informative API error responses
* Proper HTTP status codes for successful and failed operations

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* Simple JWT
* Django REST Framework Simple JWT
* Django Filters
* Cloudinary
* WhiteNoise
* Django CORS Headers
* Resend / Django Anymail for transactional emails

### Frontend

* React
* Vite
* JavaScript
* Axios
* React Router
* Tailwind CSS

### Deployment and Services

* Render
* Vercel
* PostgreSQL
* Cloudinary
* Resend

---

## Project Structure

```text
BookNest/
│
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── user_auth/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── books/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── layouts/
    │   ├── services/
    │   └── ...
    │
    ├── package.json
    └── ...
```

---

## Authentication Flow

BookNest uses JWT authentication with tokens stored in **HttpOnly cookies**.

### Registration Flow

```text
User
  │
  │ Register
  ▼
Register API
  │
  ├── Create inactive user
  │
  ├── Generate OTP
  │
  └── Send OTP via email
  │
  ▼
User verifies OTP
  │
  ▼
Account activated
  │
  ├── Access Token → HttpOnly Cookie
  │
  └── Refresh Token → HttpOnly Cookie
```

### Login Flow

```text
User
  │
  │ Username + Password
  ▼
Login API
  │
  ├── Authenticate user
  │
  ├── Generate JWT tokens
  │
  └── Store tokens in HttpOnly cookies
  │
  ▼
Authenticated API requests
```

### Token Refresh

When the access token expires, the frontend sends a request to the refresh endpoint.

The backend reads the refresh token from the HttpOnly cookie and generates a new access token.

```text
Access Token Expired
        │
        ▼
Refresh Token Cookie
        │
        ▼
Refresh API
        │
        ▼
New Access Token
```

---

## API Documentation

BookNest provides interactive API documentation using the OpenAPI specification.

The API documentation covers:

### Authentication

* User registration
* OTP verification
* OTP resend
* Login
* Token refresh
* Logout
* Profile retrieval

### Books

* List books
* Create and upload books
* Retrieve individual books
* Update books
* Partially update books
* Delete books
* Search
* Filtering
* Ordering
* Pagination

### Reading Lists

* Create reading lists
* List reading lists
* Retrieve a reading list
* Update reading lists
* Partially update reading lists
* Delete reading lists

### Reading List Books

* List books in a reading list
* Add a book to a reading list
* Remove a book from a reading list
* Reorder books in a reading list

The API documentation also includes:

* Request schemas
* Response schemas
* Validation errors
* Authentication requirements
* HTTP status codes
* Endpoint descriptions
* Example request and response payloads

### API Documentation URL

For local development:

```text
http://localhost:8000/api/docs/
```

For the deployed API:

```text
https://api.booknest.sinanonline.in/api/docs/
```

The documentation provides an interactive interface for exploring and testing the BookNest REST API.

---

## Main API Endpoints

### Authentication

```text
POST /api/auth/register/
POST /api/auth/verify-otp/
POST /api/auth/resend-otp/
POST /api/auth/login/
POST /api/auth/refresh/
POST /api/auth/logout/
GET  /api/auth/profile/
```

### Books

```text
GET    /api/books/
POST   /api/books/

GET    /api/books/<id>/
PUT    /api/books/<id>/
PATCH  /api/books/<id>/
DELETE /api/books/<id>/
```

The book listing endpoint supports search, filtering, ordering, and pagination.

Example:

```text
GET /api/books/?search=django
GET /api/books/?genre=Programming
GET /api/books/?ordering=-created_at
GET /api/books/?page=2
```

### Reading Lists

```text
GET    /api/reading-lists/
POST   /api/reading-lists/

GET    /api/reading-lists/<id>/
PUT    /api/reading-lists/<id>/
PATCH  /api/reading-lists/<id>/
DELETE /api/reading-lists/<id>/
```

### Reading List Books

```text
GET    /api/reading-lists/<id>/books/
POST   /api/reading-lists/<id>/books/

PATCH  /api/reading-lists/<id>/books/<book_id>/reorder/
DELETE /api/reading-lists/<id>/books/<book_id>/
```

---

## Media Storage

BookNest uses **Cloudinary** for media storage.

The following files are uploaded to Cloudinary:

* Book PDF files
* Book cover images

The Django backend stores the corresponding Cloudinary file references through the configured Cloudinary storage backend.

This prevents the application server from being responsible for storing uploaded media files.

---

## Database

BookNest uses **PostgreSQL** as its primary database.

The main data relationships include:

```text
User
 │
 ├── owns Books
 │
 └── owns Reading Lists
          │
          └── contains Books
                │
                └── ReadingListBook
```

The `ReadingListBook` model acts as the relationship between reading lists and books and stores the position of each book within a reading list.

A unique constraint ensures that two books cannot occupy the same position in the same reading list.

---

## Reading List Ordering

Books in a reading list are stored with a `position` value.

For example:

```text
Position 1 → Book A
Position 2 → Book B
Position 3 → Book C
```

When a book is removed, the remaining books are automatically reordered to maintain sequential positions.

Users can also explicitly reorder a book within a reading list.

The reorder operation is handled atomically to ensure that the unique position constraint is maintained during the update.

---

## Environment Variables

The backend uses environment variables for sensitive configuration.

Typical variables include:

```text
SECRET_KEY
DEBUG
ALLOWED_HOSTS

DATABASE_URL

CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET

RESEND_API_KEY

CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS
```

The exact environment variables may vary depending on the deployment environment.

Sensitive values should never be committed to the repository.

---

## Local Development

### Clone the repository

```bash
git clone <repository-url>
cd BookNest
```

### Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables.

Run migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://localhost:8000/
```

API documentation:

```text
http://localhost:8000/api/docs/
```

---

### Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The React application will be available at the URL provided by Vite, typically:

```text
http://localhost:5173/
```

---

## Deployment

The BookNest application can be deployed using separate services for the frontend and backend.

### Backend

The Django REST API can be deployed on Render with:

* Django
* Gunicorn
* PostgreSQL
* WhiteNoise
* Cloudinary
* Resend

### Frontend

The React/Vite frontend can be deployed on Vercel.

The frontend communicates with the deployed Django REST API through the configured API base URL.

Example:

```text
Frontend:
https://booknest.sinanonline.in

Backend API:
https://api.booknest.sinanonline.in

API Documentation:
https://api.booknest.sinanonline.in/api/docs/
```

---

## API Documentation Access

Once the backend is running, the interactive API documentation can be accessed at:

```text
/api/docs/
```

### Local

```text
http://localhost:8000/api/docs/
```

### Production

```text
https://api.booknest.sinanonline.in/api/docs/
```

---

## Future Improvements

Potential future improvements include:

* Book recommendations
* User profile editing
* Advanced book filtering
* Book reviews and ratings
* Favourite books
* Reading progress tracking
* Social sharing
* Improved reading-list drag-and-drop ordering
* Role-based administration
* Automated API tests
* CI/CD pipeline
* Rate limiting for authentication endpoints

---

## License

This project is intended for educational and portfolio purposes.
