import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  withCredentials: true, // если используем cookie для токенов
  timeout: 10000,
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.message ||
      'Неизвестная ошибка при запросе'
    console.error('API Error:', message)
    return Promise.reject(error)
  }
)