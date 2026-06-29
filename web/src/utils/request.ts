import axios from "axios";

export const DEFAULT_REQUEST_TIMEOUT = 30000;
export const LONG_REQUEST_TIMEOUT = 180000;

const request = axios.create({
  baseURL: "http://localhost:8000",
  timeout: DEFAULT_REQUEST_TIMEOUT,
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