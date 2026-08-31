export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface Task {
  task_id: string;
  task: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
  result?: Record<string, unknown>;
  error?: string;
  current_agent?: string;
  progress?: AgentProgress[];
}

export interface AgentProgress {
  agent: string;
  status: 'running' | 'completed' | 'failed';
  message?: string;
  timestamp: string;
}

export interface ApprovalRequest {
  approval_id: string;
  task_id: string;
  command: string;
  agent: string | null;
  description: string | null;
  status: string;
}

export interface TaskCreateRequest {
  task: string;
}

export interface TaskCreateResponse {
  task_id: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface Template {
  template_id: string;
  name: string;
  description: string;
  category: string;
  task_prompt: string;
  variables?: string[];
}

export interface KnowledgeEntry {
  entry_id: string;
  title: string;
  content: string;
  knowledge_type: string;
  tags: string[];
  created_at?: string;
}

export interface CostSummary {
  total_input_tokens: number;
  total_output_tokens: number;
  total_cost: number;
  records_count: number;
}

export interface CostRecord {
  record_id: string;
  provider: string;
  model: string;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  created_at: string;
}

export interface Budget {
  budget_id: string;
  name: string;
  limit: number;
  used: number;
  period: string;
}

export interface HealthResponse {
  status: string;
  version: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface SSEEvent {
  event: string;
  data: Record<string, unknown>;
}

// Auth types
export interface User {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Tier types
export interface TierInfo {
  name: string;
  display_name: string;
  price_monthly: number;
  tokens_per_project: number;
  max_iterations: number;
  max_projects: number;
  retention_days: number;
  can_download_code: boolean;
}

// Project types
export type ProjectStatus = 'pending' | 'generating' | 'completed' | 'failed' | 'cancelled';

export interface Project {
  id: string;
  name: string;
  description: string;
  tier: string;
  tokens_used: number;
  iterations_used: number;
  status: ProjectStatus;
  files_path: string | null;
  created_at: string;
  updated_at: string;
  expires_at: string;
}

export interface ProjectListResponse {
  projects: Project[];
  total: number;
  offset: number;
  limit: number;
}

export interface ProjectStats {
  total_projects: number;
  projects_by_status: Record<string, number>;
  total_tokens_used: number;
  current_tier: string;
  projects_remaining: number | null;
}
