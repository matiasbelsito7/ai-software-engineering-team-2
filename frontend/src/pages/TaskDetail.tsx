import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTask, deleteTask, createTaskWebSocket, getPendingApprovals, resolveApproval } from '../api';
import type { Task, AgentProgress, ApprovalRequest } from '../types';
import StatusBadge from '../components/StatusBadge';
import {
  ArrowLeft,
  Trash2,
  Clock,
  Bot,
  AlertCircle,
  CheckCircle2,
  Loader2,
  Shield,
  ShieldCheck,
  ShieldX,
  Terminal,
} from 'lucide-react';

const agentColors: Record<string, string> = {
  Planner: 'bg-purple-100 text-purple-800 border-purple-200',
  Architect: 'bg-blue-100 text-blue-800 border-blue-200',
  Backend: 'bg-green-100 text-green-800 border-green-200',
  Frontend: 'bg-orange-100 text-orange-800 border-orange-200',
  Reviewer: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  QA: 'bg-red-100 text-red-800 border-red-200',
  Documentation: 'bg-teal-100 text-teal-800 border-teal-200',
  DevOps: 'bg-indigo-100 text-indigo-800 border-indigo-200',
  Git: 'bg-gray-100 text-gray-800 border-gray-200',
};

export default function TaskDetail() {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState<AgentProgress[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [resolvingId, setResolvingId] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const fetchTask = async () => {
    if (!taskId) return;
    try {
      const data = await getTask(taskId);
      setTask(data);
      if (data.progress) setProgress(data.progress);
    } catch (err) {
      console.error('Failed to fetch task:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchApprovals = async () => {
    if (!taskId) return;
    try {
      const data = await getPendingApprovals(taskId);
      setApprovals(data);
    } catch (err) {
      console.error('Failed to fetch approvals:', err);
    }
  };

  useEffect(() => {
    fetchTask();
    fetchApprovals();
    if (!taskId) return;

    wsRef.current = createTaskWebSocket(taskId, (data) => {
      const event = data.event as string;
      if (event === 'agent_progress') {
        const agentData = data.data as Record<string, unknown>;
        setProgress((prev) => [
          ...prev,
          {
            agent: agentData.agent as string,
            status: agentData.status as 'running' | 'completed' | 'failed',
            message: agentData.message as string,
            timestamp: new Date().toISOString(),
          },
        ]);
      }
      if (event === 'approval_request') {
        fetchApprovals();
      }
      if (event === 'approval_response') {
        fetchApprovals();
      }
      if (event === 'task_complete' || event === 'error') {
        fetchTask();
      }
    });

    return () => wsRef.current?.close();
  }, [taskId]);

  const handleDelete = async () => {
    if (!taskId || !confirm('Delete this task?')) return;
    try {
      await deleteTask(taskId);
      navigate('/');
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const handleApproval = async (approvalId: string, approved: boolean) => {
    if (!taskId) return;
    try {
      setResolvingId(approvalId);
      await resolveApproval(taskId, approvalId, approved);
      fetchApprovals();
    } catch (err) {
      console.error('Failed to resolve approval:', err);
    } finally {
      setResolvingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-6 h-6 animate-spin text-indigo-600" />
      </div>
    );
  }

  if (!task) {
    return (
      <div className="text-center py-20">
        <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-500">Task not found</p>
        <button onClick={() => navigate('/')} className="mt-4 text-indigo-600 text-sm">
          Back to Dashboard
        </button>
      </div>
    );
  }

  const runningAgents = progress.filter((p) => p.status === 'running');
  const completedAgents = progress.filter((p) => p.status === 'completed');
  const allAgents = ['Planner', 'Architect', 'Backend', 'Frontend', 'Reviewer', 'QA', 'Documentation', 'DevOps', 'Git'];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center gap-4 mb-8">
        <button
          onClick={() => navigate('/')}
          className="p-2 hover:bg-gray-100 rounded-lg"
        >
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div className="flex-1">
          <h1 className="text-xl font-bold text-gray-900 line-clamp-2">{task.task}</h1>
          <div className="flex items-center gap-3 mt-2">
            <StatusBadge status={task.status} />
            <span className="text-xs text-gray-500">
              <Clock className="w-3.5 h-3.5 inline mr-1" />
              {new Date(task.created_at).toLocaleString()}
            </span>
          </div>
        </div>
        <button
          onClick={handleDelete}
          className="p-2 hover:bg-red-50 rounded-lg text-red-600"
          title="Delete task"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>

      {/* Pending Approvals */}
      {approvals.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="w-5 h-5 text-amber-600" />
            <h2 className="text-sm font-semibold text-amber-900">
              Pending Approvals ({approvals.length})
            </h2>
          </div>
          <div className="space-y-3">
            {approvals.map((approval) => (
              <div
                key={approval.approval_id}
                className="bg-white rounded-lg border border-amber-200 p-4"
              >
                <div className="flex items-start gap-3">
                  <Terminal className="w-5 h-5 text-gray-500 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 mb-1">
                      {approval.description || 'Command requires approval'}
                    </p>
                    <div className="bg-gray-50 rounded-md p-2 mb-3">
                      <code className="text-xs text-gray-700 break-all">
                        {approval.command}
                      </code>
                    </div>
                    {approval.agent && (
                      <p className="text-xs text-gray-500 mb-3">
                        Requested by: <span className="font-medium">{approval.agent}</span> agent
                      </p>
                    )}
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleApproval(approval.approval_id, true)}
                        disabled={resolvingId === approval.approval_id}
                        className="inline-flex items-center gap-1.5 px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
                      >
                        {resolvingId === approval.approval_id ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ) : (
                          <ShieldCheck className="w-3.5 h-3.5" />
                        )}
                        Approve
                      </button>
                      <button
                        onClick={() => handleApproval(approval.approval_id, false)}
                        disabled={resolvingId === approval.approval_id}
                        className="inline-flex items-center gap-1.5 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 disabled:opacity-50"
                      >
                        {resolvingId === approval.approval_id ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ) : (
                          <ShieldX className="w-3.5 h-3.5" />
                        )}
                        Reject
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Agent Workflow Pipeline */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <h2 className="text-sm font-semibold text-gray-900 mb-4">Agent Pipeline</h2>
        <div className="flex flex-wrap gap-2">
          {allAgents.map((agent, i) => {
            const isRunning = runningAgents.some((r) => r.agent === agent);
            const isCompleted = completedAgents.some((c) => c.agent === agent);
            const style = agentColors[agent] || 'bg-gray-100 text-gray-800 border-gray-200';

            return (
              <div key={agent} className="flex items-center gap-2">
                <div
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border ${
                    isRunning
                      ? 'bg-indigo-100 text-indigo-800 border-indigo-300 animate-pulse'
                      : isCompleted
                      ? style
                      : 'bg-gray-50 text-gray-400 border-gray-200'
                  }`}
                >
                  {isCompleted && <CheckCircle2 className="w-3 h-3 inline mr-1" />}
                  {isRunning && <Loader2 className="w-3 h-3 inline mr-1 animate-spin" />}
                  {agent}
                </div>
                {i < allAgents.length - 1 && (
                  <span className="text-gray-300">→</span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Progress Timeline */}
      {progress.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h2 className="text-sm font-semibold text-gray-900 mb-4">Progress</h2>
          <div className="space-y-3">
            {progress.map((p, i) => (
              <div key={i} className="flex items-start gap-3">
                <div className="mt-1">
                  {p.status === 'completed' ? (
                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                  ) : p.status === 'running' ? (
                    <Bot className="w-4 h-4 text-indigo-500 animate-pulse" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-red-500" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-900">{p.agent}</span>
                    <StatusBadge status={p.status === 'running' ? 'running' : p.status === 'completed' ? 'completed' : 'failed'} />
                  </div>
                  {p.message && (
                    <p className="text-xs text-gray-500 mt-1">{p.message}</p>
                  )}
                </div>
                <span className="text-xs text-gray-400">
                  {new Date(p.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Task Result */}
      {task.result && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-sm font-semibold text-gray-900 mb-4">Result</h2>
          <pre className="bg-gray-50 rounded-lg p-4 text-xs text-gray-700 overflow-auto max-h-96">
            {JSON.stringify(task.result, null, 2)}
          </pre>
        </div>
      )}

      {task.error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-red-900 mb-2">Error</h2>
          <p className="text-sm text-red-700">{task.error}</p>
        </div>
      )}
    </div>
  );
}
