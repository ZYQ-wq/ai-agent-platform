import axios from "axios";

const request = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000,
});

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

request.interceptors.response.use(
  (response) => response.data,
  (error) => Promise.reject(error)
);

export default request;