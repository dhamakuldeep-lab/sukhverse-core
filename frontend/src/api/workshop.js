import axios from 'axios';

const workshopApi = axios.create({ baseURL: process.env.REACT_APP_WORKSHOP_API_URL });

export const createWorkshop = (workshop) => workshopApi.post('', workshop);
export const getWorkshop = (id) => workshopApi.get(`/${id}`);
export const updateProgress = (progress) => workshopApi.post('/progress', progress);