import axios from "axios";

let BACKEND_HOST = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost";
let PROD = process.env.NEXT_PUBLIC_PROD;

let base_url = BACKEND_HOST;
console.log("Production mode", PROD);
console.log("backend:base_url", base_url);

const apiClient = axios.create({
  baseURL: base_url,
  timeout: 5000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default apiClient;
