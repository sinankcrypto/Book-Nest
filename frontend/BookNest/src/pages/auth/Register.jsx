import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import AuthLayout from "../../layouts/AuthLayout";
import AuthInput from "../../components/auth/AuthInput";
import AuthButton from "../../components/auth/AuthButton";

import { register } from "../../services/authService";
import toast from "react-hot-toast";

const Register = () => {
  const navigate = useNavigate();

  const [formData, setFormData] =
    useState({
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    });

  const [loading, setLoading] =
    useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]:
        e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (
      formData.password !==
      formData.confirmPassword
    ) {
      toast.error("Passwords do not match")
      return;
    }

    try {
      setLoading(true);

      await register({
        username:
          formData.username,
        email: formData.email,
        password:
          formData.password,
      });

      sessionStorage.setItem(
        "pendingEmail",
        formData.email
      );
      toast.success("Sign up successfull please verify your email")

      navigate("/verify-otp");

    } catch (error) {
      console.log(error);
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
    <form
      onSubmit={handleSubmit}
      className="space-y-4"
    >
      <AuthInput
        label="Username"
        name="username"
        value={formData.username}
        onChange={handleChange}
      />

      <AuthInput
        label="Email"
        name="email"
        value={formData.email}
        onChange={handleChange}
      />

      <AuthInput
        label="Password"
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
      />

      <AuthInput
        label="Confirm Password"
        type="password"
        name="confirmPassword"
        value={
          formData.confirmPassword
        }
        onChange={handleChange}
      />

      <AuthButton
        loading={loading}
      >
        Create Account
      </AuthButton>

      <p className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <Link
          to="/login"
          className="text-yellow-600"
        >
          Login
        </Link>
      </p>
    </form>
  </AuthLayout>
);

}

export default Register;