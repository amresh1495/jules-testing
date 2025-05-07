import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Assuming backend runs on port 8000

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

// Function to get all questions
export const getQuestions = () => {
  return apiClient.get('/questions/');
};

// Function to add a new question
export const addQuestion = (questionData) => {
  // Backend expects next_revision_date and current_interval_days
  // Provide default values or adjust based on backend model requirements
  const dataToSend = {
    question_text: questionData.question_text,
    solution: questionData.solution,
    next_revision_date: new Date().toISOString(), // Default to now
    current_interval_days: 0 // Default to 0
  };
  return apiClient.post('/questions/', dataToSend);
};

// Function to get a single question
export const getQuestionById = (id) => {
    return apiClient.get(`/questions/${id}`);
};

// Function to update a question's schedule
export const updateQuestionSchedule = (id, intervalDays) => {
    console.log(`Updating schedule for question ${id} with interval ${intervalDays} days`);
    return apiClient.put(`/questions/${id}`, { current_interval_days: intervalDays });
};
