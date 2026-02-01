import axios from "axios";
import { toast } from "react-toastify";

// Create the axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Request Interceptor: Attach the Token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ Response Interceptor: Handle Errors & Auto-Refresh Token
api.interceptors.response.use(
  (res) => res, // If success, just return the response
  async (err) => {
    const originalRequest = err.config;

    // 1️⃣ Check if error is 401 (Unauthorized) AND we haven't retried yet
    if (
      err.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem("refresh")
    ) {
      originalRequest._retry = true; // Mark as retried to prevent infinite loops

      try {
        // 2️⃣ Try to get a new access token using the refresh token
        const refreshRes = await axios.post(
          "http://127.0.0.1:8000/api/v1/accounts/token/refresh/",
          { refresh: localStorage.getItem("refresh") },
          { headers: { "Content-Type": "application/json" } }
        );

        // 3️⃣ Save new token
        const newAccessToken = refreshRes.data.access;
        localStorage.setItem("access", newAccessToken);

        // 4️⃣ Update the header and retry the original failed request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);

      } catch (refreshErr) {
        // 5️⃣ If refresh fails (token expired completely), force logout
        console.error("Refresh failed", refreshErr);
        toast.error("Session expired. Please login again.");
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshErr);
      }
    }

    // 6️⃣ Handle other errors (like 400 Bad Request, 500 Server Error)
    if (err.response?.status !== 401) {
       toast.error(
        err.response?.data?.detail ||
        err.response?.data?.non_field_errors?.[0] ||
        "Something went wrong"
      );
    }

    return Promise.reject(err);
  }
);

export default api;