import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8001";
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  headers: {
    "Content-Type": "application/json",
  },
});

// API Service
export const api = {
  // Health check
  health: async () => {
    const response = await apiClient.get("/health");
    return response.data;
  },

  // Get data summary
  getSummary: async () => {
    const response = await apiClient.get("/summary");
    return response.data;
  },

  // Upload files
  uploadMixpanel: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post("/upload/mixpanel", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  uploadMoengage: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post("/upload/moengage", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  uploadJira: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await apiClient.post("/upload/jira", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },

  // Get metrics
  getMetrics: async () => {
    const response = await apiClient.get("/metrics");
    return response.data;
  },

  // Analyze specific metric
  analyzeMetric: async (anomalyId) => {
    const response = await apiClient.post(`/analyze/${anomalyId}`);
    return response.data;
  },

  // Get insights
  getInsights: async () => {
    const response = await apiClient.get("/insights");
    return response.data;
  },

  // Get enhanced insights
  getEnhancedInsights: async () => {
    const response = await apiClient.get("/insights/enhanced");
    return response.data;
  },

  // Trigger insights generation
  triggerInsightsGeneration: async () => {
    const response = await apiClient.post("/insights/generate");
    return response.data;
  },

  // Natural language query
  query: async (question) => {
    const response = await apiClient.post("/query", { query: question });
    return response.data;
  },

  // Trigger action
  triggerAction: async (insightId, metric, actionType) => {
    const response = await apiClient.post("/action/trigger", {
      insight_id: insightId,
      metric: metric,
      action_type: actionType,
    });
    return response.data;
  },

  // Get action logs
  getActionLogs: async () => {
    const response = await apiClient.get("/action-logs");
    return response.data;
  },

  // Reset data
  resetData: async () => {
    const response = await apiClient.delete("/reset");
    return response.data;
  },
};

export default api;
