import axios from "axios";

const API = axios.create({
  baseURL: "https://ai-resume-analyzer-backend-5sk7.onrender.com",
});

export default API;