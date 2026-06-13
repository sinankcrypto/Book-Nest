import { useState } from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";

import toast from "react-hot-toast";

import AuthLayout from "../../layouts/AuthLayout";
import AuthButton from "../../components/auth/AuthButton";
import { verifyOTP, resendOTP } from "../../services/authService";

import { useAuth } from "../../context/AuthContext";

const VerifyOTP = () => {
  const navigate = useNavigate();

  const location = useLocation();

  const { loadUser } = useAuth();

  const email = sessionStorage.getItem("pendingEmail");

  const [otp, setOtp] = useState("");

  const [loading, setLoading] = useState(false);

  const [resending, setResending] = useState(false);

  const handleVerify = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await verifyOTP({
        email,
        otp,
      });

      await loadUser();

      toast.success(
        "Account verified successfully"
      );

      navigate("/");
    } catch (error) {
      toast.error(
        error?.response?.data
          ?.detail ||
          "OTP verification failed"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    try {
      setResending(true);

      await resendOTP({
        email,
      });

      toast.success(
        "OTP resent successfully"
      );
    } catch (error) {
      toast.error(
        error?.response?.data
          ?.detail ||
          "Failed to resend OTP"
      );
    } finally {
      setResending(false);
    }
  };

  if (!email) {
    navigate("/register");
    return null;
  }

  return (
    <AuthLayout>
      <form
        onSubmit={handleVerify}
        className="space-y-6"
      >
        <div>
          <h2 className="text-xl font-semibold text-center">
            Verify Email
          </h2>

          <p className="text-sm text-gray-500 text-center mt-2">
            Enter the 6-digit code
            sent to
          </p>

          <p className="text-sm text-center font-medium mt-1">
            {email}
          </p>
        </div>

        <input
          type="text"
          maxLength={6}
          value={otp}
          onChange={(e) =>
            setOtp(
              e.target.value
            )
          }
          placeholder="Enter OTP"
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-center text-xl tracking-widest outline-none focus:ring-2 focus:ring-yellow-400"
        />

        <AuthButton
          loading={loading}
          type="submit"
        >
          Verify OTP
        </AuthButton>

        <div className="text-center">
          <button
            type="button"
            onClick={
              handleResend
            }
            disabled={
              resending
            }
            className="text-yellow-600 hover:text-yellow-700"
          >
            {resending
              ? "Resending..."
              : "Resend OTP"}
          </button>
        </div>
      </form>
    </AuthLayout>
  );
};

export default VerifyOTP;