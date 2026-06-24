import {
  Routes,
  Route,
} from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import VerifyOTP from "../pages/auth/VerifyOTP";
import Home from "../pages/Home"
import Books from "../pages/books/Books";
import UploadBook from "../pages/books/UploadBook";
import BookDetail from "../pages/books/BookDetail";
import ReadingLists from "../pages/readingLists/ReadingLists";
import ReadingListDetail from "../pages/readingLists/ReadingListDetail";

import ProtectedRoute from "./ProtectedRoute";
import MainLayout from "../layouts/MainLayout";
import { ImageOff } from "lucide-react";

const AppRoutes = () => {
  return (
    <Routes>
      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      <Route
        path="/verify-otp"
        element={<VerifyOTP />}
      />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Home />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/books"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Books />
            </MainLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/upload-book"
        element={
          <ProtectedRoute>
            <UploadBook />
          </ProtectedRoute>
        }
      />
      <Route
        path="/books/:id"
        element={
          <ProtectedRoute>
            <BookDetail />
          </ProtectedRoute>
        }
      />
      <Route
        path="/reading-lists"
        element={
          <ProtectedRoute>
            <ReadingLists />
          </ProtectedRoute>
        }
      />

      <Route
        path="/reading-lists/:id"
        element={
          <ProtectedRoute>
            <ReadingListDetail />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default AppRoutes;