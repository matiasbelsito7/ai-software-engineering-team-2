import axios from 'axios';
import type {
  Task,
  TaskCreateRequest,
  TaskCreateResponse,
  Template,
  KnowledgeEntry,
  CostRecord,
  CostSummary,
  Budget,
  HealthResponse,
  PaginatedResponse,
  ApprovalRequest,
  User,
  TokenResponse,
  Project,
  ProjectListResponse,
  ProjectStats,
  TierInfo,
} from './types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 and try refresh
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;

    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post<TokenResponse>('/api/v1/auth/refresh', {
            refresh_token: refreshToken,
          });
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('refresh_token', data.refresh_token);
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
          return api(originalRequest);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      } else {
        window.location.href = '/login';
      }
    }

    const message = err.response?.data?.detail || err.message;
    return Promise.reject(new Error(message));
  }
);

// Auth
export const register = (email: string, password: string) =>
  api.post<User>('/auth/register', { email, password }).then((r) => r.data);

export const login = (email: string, password: string) =>
  api.post<TokenResponse>('/auth/login', { email, password }).then((r) => r.data);

export const refreshToken = (refresh_token: string) =>
  api.post<TokenResponse>('/auth/refresh', { refresh_token }).then((r) => r.data);

export const getMe = () =>
  api.get<User>('/auth/me').then((r) => r.data);

// Tiers
export const getTiers = () =>
  api.get<TierInfo[]>('/projects/tiers').then((r) => r.data);

// Projects
export const createProject = (data: { name: string; description: string; tier?: string }) =>
  api.post<Project>('/projects', data).then((r) => r.data);

export const getProjects = (offset = 0, limit = 50, status?: string) =>
  api.get<ProjectListResponse>('/projects', { params: { offset, limit, status } }).then((r) => r.data);

export const getProject = (projectId: string) =>
  api.get<Project>(`/projects/${projectId}`).then((r) => r.data);

export const deleteProject = (projectId: string) =>
  api.delete(`/projects/${projectId}`);

export const getProjectStats = () =>
  api.get<ProjectStats>('/projects/stats').then((r) => r.data);

export const getProjectPreview = (projectId: string) =>
  api.get<{ html: string }>(`/projects/${projectId}/preview`).then((r) => r.data);

export const downloadProject = async (projectId: string, projectName: string) => {
  const response = await api.get(`/projects/${projectId}/download`, {
    responseType: 'blob',
  });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${projectName}.zip`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

// Admin
export const getAdminMetrics = () =>
  api.get('/admin/metrics').then((r) => r.data);

export const getAdminUsers = (offset = 0, limit = 50) =>
  api.get('/admin/users', { params: { offset, limit } }).then((r) => r.data);

// Health
export const getHealth = () => api.get<HealthResponse>('/health').then((r) => r.data);

// Tasks
export const createTask = (data: TaskCreateRequest) =>
  api.post<TaskCreateResponse>('/tasks', data).then((r) => r.data);

export const getTasks = (page = 1, page_size = 20) =>
  api.get<PaginatedResponse<Task>>('/tasks', { params: { page, page_size } }).then((r) => r.data);

export const getTask = (taskId: string) =>
  api.get<Task>(`/tasks/${taskId}`).then((r) => r.data);

export const deleteTask = (taskId: string) =>
  api.delete(`/tasks/${taskId}`);

// Templates
export const getTemplates = () =>
  api.get<Template[]>('/templates').then((r) => r.data);

export const getTemplate = (templateId: string) =>
  api.get<Template>(`/templates/${templateId}`).then((r) => r.data);

export const createTaskFromTemplate = (templateId: string, vars: Record<string, string>) =>
  api.post(`/templates/${templateId}/create-task`, vars).then((r) => r.data);

// Knowledge
export const getKnowledge = (page = 1, page_size = 20) =>
  api.get<PaginatedResponse<KnowledgeEntry>>('/knowledge', { params: { page, page_size } }).then((r) => r.data);

export const searchKnowledge = (q: string) =>
  api.get<KnowledgeEntry[]>('/knowledge/search', { params: { q } }).then((r) => r.data);

export const createKnowledgeEntry = (entry: Omit<KnowledgeEntry, 'created_at'>) =>
  api.post<KnowledgeEntry>('/knowledge', entry).then((r) => r.data);

export const deleteKnowledgeEntry = (entryId: string) =>
  api.delete(`/knowledge/${entryId}`);

// Cost Tracking
export const getCostSummary = () =>
  api.get<CostSummary>('/cost-tracking/summary').then((r) => r.data);

export const getCostRecords = (page = 1, page_size = 20) =>
  api.get<PaginatedResponse<CostRecord>>('/cost-tracking/records', { params: { page, page_size } }).then((r) => r.data);

export const getBudgets = () =>
  api.get<Budget[]>('/cost-tracking/budgets').then((r) => r.data);

export const createBudget = (budget: Omit<Budget, 'used'>) =>
  api.post<Budget>('/cost-tracking/budgets', budget).then((r) => r.data);

export const deleteBudget = (budgetId: string) =>
  api.delete(`/cost-tracking/budgets/${budgetId}`);

// WebSocket helper
export const createTaskWebSocket = (
  taskId: string,
  onMessage: (data: Record<string, unknown>) => void,
  onError?: (error: Event) => void,
  onClose?: (event: CloseEvent) => void,
) => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//${window.location.host}/ws/tasks/${taskId}`);
  ws.onmessage = (event) => {
    try {
      onMessage(JSON.parse(event.data));
    } catch {
      console.error('Failed to parse WebSocket message');
    }
  };
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    onError?.(error);
  };
  ws.onclose = (event) => {
    console.warn('WebSocket closed:', event.code, event.reason);
    onClose?.(event);
  };
  return ws;
};

// SSE helper
export const streamTask = async function* (taskId: string) {
  const response = await fetch(`/api/v1/tasks/${taskId}/stream`);
  if (!response.ok) {
    throw new Error(`Stream failed: ${response.status} ${response.statusText}`);
  }
  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  if (!reader) return;

  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          yield JSON.parse(line.slice(6));
        } catch { /* skip malformed */ }
      }
    }
  }
};

// Approvals (human-in-the-loop)
export const getPendingApprovals = (taskId: string) =>
  api.get<ApprovalRequest[]>(`/tasks/${taskId}/approvals`).then((r) => r.data);

export const resolveApproval = (taskId: string, approvalId: string, approved: boolean) =>
  api.post(`/tasks/${taskId}/approvals/${approvalId}`, { approved }).then((r) => r.data);
