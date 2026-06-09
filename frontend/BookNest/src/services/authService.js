import api from "../api/axios";

export const login = async (data) => {
	const response = await api.post("/auth/login/", data);
	return response.data
} ;

export const register = async (data) => {
	const response = await api.post("/auth/register/", data);
	return response.data
};

export const VerifyOTP = async (data) => {
	const response = await api.post("/auth/verify-otp", data);
	return response.data;
};

export const resendOTP = async (data) => {
  const response = await api.post("/auth/resend-otp/", data);

  return response.data;
};

export const logout = async () => {
  const response = await api.post("/auth/logout/");

  return response.data;
};

export const getProfile = async () => {
  const response = await api.get("/auth/profile/");

  return response.data;
};