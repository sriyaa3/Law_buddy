import axios from 'axios';

const API_BASE_URL = 'http://localhost:8006/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatApi = {
  sendMessage: (message, chatId) => 
    api.post('/chat/message', { message, chat_id: chatId }),
  
  getChatHistory: (chatId) => 
    api.get(`/chat/history/${chatId}`),
};

// Document API
export const documentApi = {
  uploadDocument: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  processDocument: (documentId) => 
    api.get(`/documents/process/${documentId}`),
};

// Document Generation API
export const documentGenerationApi = {
  getTemplates: () => 
    api.get('/document-generation/templates'),
  
  generateDocument: (documentRequest) => 
    api.post('/document-generation/generate', documentRequest),
  
  downloadDocument: (filename) => 
    api.get(`/document-generation/download/${filename}`),
};

// User API
export const userApi = {
  createUser: (userData) => 
    api.post('/users/', userData),
  
  getUser: (userId) => 
    api.get(`/users/${userId}`),
};

// MSME API
export const msmeApi = {
  createBusinessProfile: (profileData) => 
    api.post('/msme/profile', profileData),
  
  getBusinessProfile: (userId) => 
    api.get(`/msme/profile/${userId}`),
  
  updateBusinessProfile: (userId, profileData) => 
    api.put(`/msme/profile/${userId}`, profileData),
  
  getRecommendations: (userId, type) => 
    api.get(`/msme/recommendations/${userId}?type=${type}`),
  
  createWorkflow: (userId, templateName) => 
    api.post('/msme/workflows', { user_id: userId, template_name: templateName }),
  
  getWorkflows: (userId) => 
    api.get(`/msme/workflows/${userId}`),
  
  startWorkflowStep: (workflowId, stepIndex) => 
    api.post(`/msme/workflows/${workflowId}/steps/${stepIndex}/start`),
  
  completeWorkflowStep: (workflowId, stepIndex) => 
    api.post(`/msme/workflows/${workflowId}/steps/${stepIndex}/complete`),
};

export default api;