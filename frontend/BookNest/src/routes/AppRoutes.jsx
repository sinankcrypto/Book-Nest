import {
  Routes,
  Route,
} from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import VerifyOTP from "../pages/auth/VerifyOTP";
import Home from "../pages/Home"
import Books from "../pages/books/Books";


import ProtectedRoute from "./ProtectedRoute";
import MainLayout from "../layouts/MainLayout";

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
    </Routes>
  );
};

export default AppRoutes;