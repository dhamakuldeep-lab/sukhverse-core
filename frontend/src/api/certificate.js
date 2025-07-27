import axios from 'axios';

const certificateApi = axios.create({ baseURL: process.env.REACT_APP_CERTIFICATE_API_URL });

export const listCertificatesForUser = (userId) => certificateApi.get(`/user/${userId}`);