import axios from 'axios';

const analyticsApi = axios.create({ baseURL: process.env.REACT_APP_ANALYTICS_API_URL });

export const getDashboard = (workshopId) => analyticsApi.get(`/dashboard`, { params: { workshop_id: workshopId } });
export const getAtRiskStudents = () => analyticsApi.get('/at-risk');