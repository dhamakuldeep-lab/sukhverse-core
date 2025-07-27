import axios from 'axios';

const authApi = axios.create({ baseURL: process.env.REACT_APP_AUTH_API_URL });

export const register = (email, password) => authApi.post('/register', { email, password });
export const login = (email, password) => authApi.post('/login', { username: email, password }, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });