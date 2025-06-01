import axios from "axios";

const API_URL = "http://localhost:8000"; // адрес вашего FastAPI backend

export const registerUser = (data) => axios.post(`${API_URL}/auth-service/register`, data);
export const loginUser = (data) => axios.post(`${API_URL}/auth-service/login`, data);
export const getUser = (userId) => axios.get(`${API_URL}/auth-service/user`, { params: { user_id: userId } });
export const logoutUser = () => axios.post(`${API_URL}/auth-service/logout`);
export const getUserList = () => axios.get(`${API_URL}/auth-service/user-list`);
export const deleteUser = (userId) => axios.delete(`${API_URL}/auth-service/user/delete/${userId}`);
export const updateUser = (userId, data) => axios.put(`${API_URL}/auth-service/user/update/${userId}`, data);

