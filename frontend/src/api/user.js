import axios from 'axios';

const userApi = axios.create({ baseURL: process.env.REACT_APP_USER_API_URL });

export const getProfile = (userId) => userApi.get(`/${userId}`);
export const upsertProfile = (profile) => userApi.post('/profile', profile);
export const assignRole = (userId, roleId, assignedBy) => userApi.post(`/${userId}/roles`, { role_id: roleId, assigned_by: assignedBy });