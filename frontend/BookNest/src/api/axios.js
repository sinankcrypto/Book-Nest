import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL,
  withCredentials: true,
});

const skipRefreshUrls = [
  "/auth/login/",
  "/auth/register/",
  "/auth/profile/",
  "/auth/refresh/",
  "/auth/verify-otp/",
  "/auth/resend-otp/",
];

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest =
      error.config;

    if (
      skipRefreshUrls.some(url =>
        originalRequest.url?.includes(url)
      )
    ) {
      return Promise.reject(error);
    }

    if (
      error.response?.status ===
        401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/refresh/`,
          {},
          {
            withCredentials: true,
          }
        );

        return api(
          originalRequest
        );
      } catch (err) {
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default api;