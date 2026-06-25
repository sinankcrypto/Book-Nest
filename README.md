# 📚 BookNest

BookNest is a full-stack book management platform built with **Django REST Framework** and **React**. Users can upload books, browse a shared digital library, create reading lists, and organize their reading experience.

## 🚀 Features

### User Management
- User registration with email OTP verification
- Secure login and logout
- JWT authentication using HTTP-only cookies
- Profile management

### Book Management
- Upload books with PDF files
- Upload book cover images
- Browse all uploaded books
- View detailed book information
- Search books by title, author, or genre
- Paginated book listing

### Reading Lists
- Create reading lists
- View reading lists
- Delete reading lists
- Add books to reading lists
- Remove books from reading lists
- Track the number of books in each reading list

### Security & Validation
- JWT Authentication
- Protected API endpoints
- Input validation using Django REST Framework serializers
- Proper error handling and informative responses

---

## 🛠 Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- Cloudinary
- Django CORS Headers

### Frontend
- React
- Vite
- React Router
- Axios
- Tailwind CSS
- React Hot Toast

### Deployment
- Frontend: Vercel
- Backend: Render
- Database: PostgreSQL
- Media Storage: Cloudinary

---

## 📂 Project Structure

### Backend

```txt
backend/
├── accounts/
├── books/
├── config/
├── manage.py
├── requirements.txt
└── ...
```

### Frontend

```txt
frontend/
├── src/
│   ├── api/
│   ├── components/
│   ├── context/
│   ├── layouts/
│   ├── pages/
│   ├── services/
│   └── routes/
├── package.json
└── ...
```

---

## 📖 API Overview

### Authentication

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/verify-otp/` | Verify email OTP |
| POST | `/api/auth/resend-otp/` | Resend OTP |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/profile/` | Get user profile |

---

### Books

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/api/books/` | List books |
| POST | `/api/books/` | Upload book |
| GET | `/api/books/{id}/` | Book details |
| DELETE | `/api/books/{id}/` | Delete book |

---

### Reading Lists

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/api/reading-lists/` | List reading lists |
| POST | `/api/reading-lists/` | Create reading list |
| GET | `/api/reading-lists/{id}/` | Reading list details |
| DELETE | `/api/reading-lists/{id}/` | Delete reading list |
| POST | `/api/reading-lists/{id}/books/` | Add book to list |
| DELETE | `/api/reading-lists/{id}/books/{book_id}/` | Remove book from list |

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd BookNest
```

---

## Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=booknest
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Backend Server

```bash
python manage.py runserver
```

---

## Frontend Setup

### Install Dependencies

```bash
npm install
```

### Configure Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

### Start Frontend

```bash
npm run dev
```

---

## ☁️ Deployment

### Frontend
- Hosted on Vercel

### Backend
- Hosted on Render

### Database
- PostgreSQL

### Media Files
- Cloudinary

---

## 🔒 Authentication Flow

```txt
Register
   ↓
OTP Verification
   ↓
Login
   ↓
JWT Cookies Issued
   ↓
Protected Routes Accessible
```

---

## 📸 Screens

### Home
- Featured books section
- Welcome banner

### Books
- Search books
- Paginated listing

### Upload Book
- Upload PDF
- Upload cover image

### Book Detail
- View book details
- Read PDF
- Add to reading list

### Reading Lists
- Create reading lists
- Manage books within lists

---

## Future Improvements

- Reading list reordering (drag and drop)
- Edit reading list names
- User profile editing
- Advanced filtering by genre and author
- Book recommendations
- Dark mode
- Book ratings and reviews

---

## Author

**Sinan Muhammed**

Built as a full-stack Django + React book management application.