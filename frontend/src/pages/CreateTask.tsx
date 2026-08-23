import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTask } from '../api';
import { Send, Loader2 } from 'lucide-react';

export default function CreateTask() {
  const [task, setTask] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!task.trim()) return;
    try {
      setSubmitting(true);
      setError('');
      const res = await createTask({ task: task.trim() });
      navigate(`/tasks/${res.task_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">New Task</h1>
      <p className="text-sm text-gray-500 mb-8">
        Describe the software engineering task you want the AI team to work on.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="task" className="block text-sm font-medium text-gray-700 mb-2">
            Task Description
          </label>
          <textarea
            id="task"
            rows={6}
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="e.g. Build a REST API for user management with CRUD operations, authentication, and tests..."
            className="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={!task.trim() || submitting}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            Submit Task
          </button>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-6 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
