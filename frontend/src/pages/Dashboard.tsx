import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTasks } from '../api';
import type { Task } from '../types';
import StatusBadge from '../components/StatusBadge';
import { RefreshCw, Plus, ExternalLink } from 'lucide-react';

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const pageSize = 15;

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await getTasks(page, pageSize);
      setTasks(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000);
    return () => clearInterval(interval);
  }, [page]);

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
          <p className="text-sm text-gray-500 mt-1">{total} total tasks</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={fetchTasks}
            className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
          <Link
            to="/tasks/new"
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            <Plus className="w-4 h-4" />
            New Task
          </Link>
        </div>
      </div>

      {loading && tasks.length === 0 ? (
        <div className="text-center py-12 text-gray-500">Loading tasks...</div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-200">
          <p className="text-gray-500 mb-4">No tasks yet</p>
          <Link
            to="/tasks/new"
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            <Plus className="w-4 h-4" />
            Create your first task
          </Link>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Task</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Agent</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Created</th>
                  <th className="px-6 py-3"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {tasks.map((task) => (
                  <tr key={task.task_id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <Link
                        to={`/tasks/${task.task_id}`}
                        className="text-sm font-medium text-gray-900 hover:text-indigo-600 line-clamp-1"
                      >
                        {task.task}
                      </Link>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={task.status} />
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {task.current_agent || '—'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {new Date(task.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        to={`/tasks/${task.task_id}`}
                        className="text-indigo-600 hover:text-indigo-800"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {totalPages > 1 && (
            <div className="flex justify-center gap-2 mt-6">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1 text-sm border rounded disabled:opacity-50"
              >
                Prev
              </button>
              <span className="px-3 py-1 text-sm text-gray-600">
                {page} / {totalPages}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-3 py-1 text-sm border rounded disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
