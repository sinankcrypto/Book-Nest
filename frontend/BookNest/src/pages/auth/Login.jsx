import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import toast from "react-hot-toast";

import AuthLayout from "../../layouts/AuthLayout";
import AuthInput from "../../components/auth/authInput";
import AuthButton from "../../components/auth/authButton";

import { login } from "../../services/authService";
import { useAuth } from "../../context/AuthContext";

const Login = () => {
  const navigate = useNavigate();
  const { loadUser } = useAuth();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await login(formData);
      await loadUser();

      toast.success("Logged in successfully");

      navigate("/", { replace: true });
    } catch (error) {
      const errors = error?.response?.data;

      if (errors) {
        const firstField = Object.keys(errors)[0];
        const firstError = errors[firstField]?.[0];

        toast.error(firstError || "Registration failed");
      } else {
        toast.error("An error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Welcome Back
        </h2>

        <p className="mt-2 text-gray-500">
          Sign in to continue your reading journey
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >
        <AuthInput
          label="Username"
          name="username"
          placeholder="Enter your username"
          value={formData.username}
          onChange={handleChange}
          disabled={loading}
          autoComplete="username"
        />

        <AuthInput
          label="Password"
          type="password"
          name="password"
          placeholder="Enter your password"
          value={formData.password}
          onChange={handleChange}
          disabled={loading}
          autoComplete="current-password"
        />

        <AuthButton
          loading={loading}
          type="submit"
        >
          Login
        </AuthButton>

        <p className="text-center text-sm text-gray-600">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="
              font-semibold
              text-amber-600
              hover:text-amber-700
              transition-colors
            "
          >
            Create one
          </Link>
        </p>
      </form>
    </AuthLayout>
  );
};

export default Login;