// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiConfig = {
  baseUrl: API_BASE_URL,
  endpoints: {
    validate: `${API_BASE_URL}/api/interview/validate`,
    start: `${API_BASE_URL}/api/interview/start`,
    evaluate: `${API_BASE_URL}/api/interview/evaluate`,
    end: (sessionId: string) => `${API_BASE_URL}/api/interview/${sessionId}`
  }
};