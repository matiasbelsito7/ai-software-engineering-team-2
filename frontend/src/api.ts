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
} from './types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.detail || err.message;
    return Promise.reject(new Error(message));
  }
);

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
export const createTaskWebSocket = (taskId: string, onMessage: (data: Record<string, unknown>) => void) => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//${window.location.host}/ws/tasks/${taskId}`);
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  return ws;
};

// SSE helper
export const streamTask = async function* (taskId: string) {
  const response = await fetch(`/api/v1/tasks/${taskId}/stream`);
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
