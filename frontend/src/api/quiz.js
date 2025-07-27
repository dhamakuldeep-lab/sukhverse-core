import axios from 'axios';

const quizApi = axios.create({ baseURL: process.env.REACT_APP_QUIZ_API_URL });

export const getQuiz = (id) => quizApi.get(`/${id}`);
export const submitQuiz = (id, attempt) => quizApi.post(`/${id}/attempts`, attempt);