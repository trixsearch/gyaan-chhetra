import axios from "axios";
// import { toast } from "react-toastify"; // Optional: Uncomment if you want error toasts back

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

// ✅ Response Interceptor: Auto-Refresh Token (Simplified Version)
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;

    // If error is 401 and we haven't retried yet
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;

      try {
        const refresh = localStorage.getItem("refresh");
        
        // 1. Call the refresh endpoint
        const res = await axios.post(
          "http://127.0.0.1:8000/api/v1/accounts/token/refresh/",
          { refresh }
        );

        // 2. Save the new token
        localStorage.setItem("access", res.data.access);

        // 3. Update header and retry original request
        original.headers.Authorization = `Bearer ${res.data.access}`;
        return api(original);

      } catch (error) {
        // 4. If refresh fails, clear storage and redirect to login
        localStorage.clear();
        window.location.href = "/login";
      }
    }

    return Promise.reject(err);
  }
);

export default api;