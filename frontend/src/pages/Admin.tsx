import { useEffect, useState } from 'react';
import { getAdminMetrics, getAdminUsers } from '../api';
import {
  Users,
  FolderOpen,
  Cpu,
  Activity,
  Shield,
  RefreshCw,
} from 'lucide-react';

interface AdminMetrics {
  total_users: number;
  active_users: number;
  total_projects: number;
  projects_by_status: Record<string, number>;
  projects_by_tier: Record<string, number>;
  total_tokens_used: number;
  total_iterations: number;
}

interface AdminUser {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string | null;
}

export default function Admin() {
  const [metrics, setMetrics] = useState<AdminMetrics | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [metricsRes, usersRes] = await Promise.all([
        getAdminMetrics(),
        getAdminUsers(0, 20),
      ]);
      setMetrics(metricsRes);
      setUsers(usersRes.users);
    } catch (err) {
      console.error('Failed to fetch admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <div className="text-center py-12 text-gray-500">Loading metrics...</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Platform overview and metrics</p>
        </div>
        <button
          onClick={fetchData}
          className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {metrics && (
        <>
          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <div className="flex items-center gap-3 mb-2">
                <Users className="w-5 h-5 text-indigo-600" />
                <span className="text-sm text-gray-500">Users</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">{metrics.total_users}</div>
              <div className="text-xs text-gray-400 mt-1">{metrics.active_users} active</div>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <div className="flex items-center gap-3 mb-2">
                <FolderOpen className="w-5 h-5 text-indigo-600" />
                <span className="text-sm text-gray-500">Projects</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">{metrics.total_projects}</div>
              <div className="text-xs text-gray-400 mt-1">
                {metrics.projects_by_status.completed || 0} completed
              </div>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <div className="flex items-center gap-3 mb-2">
                <Cpu className="w-5 h-5 text-indigo-600" />
                <span className="text-sm text-gray-500">Tokens Used</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {metrics.total_tokens_used > 0
                  ? `${(metrics.total_tokens_used / 1_000_000).toFixed(2)}M`
                  : '0'}
              </div>
              <div className="text-xs text-gray-400 mt-1">
                {metrics.total_iterations} iterations
              </div>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <div className="flex items-center gap-3 mb-2">
                <Activity className="w-5 h-5 text-indigo-600" />
                <span className="text-sm text-gray-500">Status Breakdown</span>
              </div>
              <div className="space-y-1 mt-2">
                {Object.entries(metrics.projects_by_status).map(([status, count]) => (
                  <div key={status} className="flex justify-between text-xs">
                    <span className="text-gray-500 capitalize">{status}</span>
                    <span className="font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-sm font-semibold text-gray-900 mb-4">Projects by Tier</h2>
              <div className="space-y-3">
                {Object.entries(metrics.projects_by_tier).map(([tier, count]) => (
                  <div key={tier} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 capitalize">{tier}</span>
                    <div className="flex items-center gap-3">
                      <div className="w-32 bg-gray-100 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{
                            width: `${Math.min(100, (count / Math.max(metrics.total_projects, 1)) * 100)}%`,
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 w-8 text-right">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h2 className="text-sm font-semibold text-gray-900 mb-4">Recent Users</h2>
              <div className="space-y-3">
                {users.map((user) => (
                  <div key={user.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{user.email}</div>
                      <div className="text-xs text-gray-400">
                        {user.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {user.role === 'admin' && (
                        <Shield className="w-3.5 h-3.5 text-indigo-600" />
                      )}
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full ${
                          user.is_active
                            ? 'bg-green-50 text-green-700'
                            : 'bg-gray-100 text-gray-500'
                        }`}
                      >
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
