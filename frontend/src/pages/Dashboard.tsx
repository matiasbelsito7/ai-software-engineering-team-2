import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProjects, getProjectStats } from '../api';
import type { Project, ProjectStats } from '../types';
import StatusBadge from '../components/StatusBadge';
import { RefreshCw, Plus, ExternalLink, FolderOpen } from 'lucide-react';

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [stats, setStats] = useState<ProjectStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const limit = 15;

  const fetchData = async (isInitial = false) => {
    try {
      if (isInitial) setLoading(true);
      const [projectRes, statsRes] = await Promise.all([
        getProjects(offset, limit),
        getProjectStats(),
      ]);
      setProjects(projectRes.projects);
      setTotal(projectRes.total);
      setStats(statsRes);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    } finally {
      if (isInitial) setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(true);
    const interval = setInterval(() => fetchData(), 5000);
    return () => clearInterval(interval);
  }, [offset]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Projects</h1>
          <p className="text-sm text-gray-500 mt-1">{total} total projects</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => fetchData()}
            className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
          <Link
            to="/projects/new"
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            <Plus className="w-4 h-4" />
            New Project
          </Link>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="text-sm text-gray-500">Projects</div>
            <div className="text-2xl font-bold text-gray-900">{stats.total_projects}</div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="text-sm text-gray-500">Tokens Used</div>
            <div className="text-2xl font-bold text-gray-900">
              {stats.total_tokens_used > 0 ? `${(stats.total_tokens_used / 1000).toFixed(0)}K` : '0'}
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="text-sm text-gray-500">Tier</div>
            <div className="text-2xl font-bold text-indigo-600 capitalize">{stats.current_tier}</div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-4">
            <div className="text-sm text-gray-500">Remaining</div>
            <div className="text-2xl font-bold text-gray-900">
              {stats.projects_remaining === null ? '∞' : stats.projects_remaining}
            </div>
          </div>
        </div>
      )}

      {loading && projects.length === 0 ? (
        <div className="text-center py-12 text-gray-500">Loading projects...</div>
      ) : projects.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-200">
          <FolderOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 mb-4">No projects yet</p>
          <Link
            to="/projects/new"
            className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700"
          >
            <Plus className="w-4 h-4" />
            Create your first project
          </Link>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Project</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Tier</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Tokens</th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase">Created</th>
                  <th className="px-6 py-3"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {projects.map((project) => (
                  <tr key={project.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <Link
                        to={`/projects/${project.id}`}
                        className="text-sm font-medium text-gray-900 hover:text-indigo-600 line-clamp-1"
                      >
                        {project.name}
                      </Link>
                      <p className="text-xs text-gray-500 line-clamp-1 mt-0.5">{project.description}</p>
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={project.status} />
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 capitalize">{project.tier}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {project.tokens_used > 0 ? `${(project.tokens_used / 1000).toFixed(0)}K` : '0'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {new Date(project.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        to={`/projects/${project.id}`}
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
                onClick={() => setOffset((o) => Math.max(0, o - limit))}
                disabled={offset === 0}
                className="px-3 py-1 text-sm border rounded disabled:opacity-50"
              >
                Prev
              </button>
              <span className="px-3 py-1 text-sm text-gray-600">
                {Math.floor(offset / limit) + 1} / {totalPages}
              </span>
              <button
                onClick={() => setOffset((o) => Math.min((totalPages - 1) * limit, o + limit))}
                disabled={offset + limit >= total}
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
