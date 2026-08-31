import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  LayoutDashboard,
  PlusCircle,
  FileText,
  BookOpen,
  DollarSign,
  Activity,
  LogOut,
} from 'lucide-react';

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/projects/new', label: 'New Project', icon: PlusCircle },
  { to: '/templates', label: 'Templates', icon: FileText },
  { to: '/knowledge', label: 'Knowledge', icon: BookOpen },
  { to: '/costs', label: 'Costs', icon: DollarSign },
];

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen flex bg-gray-50">
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <Activity className="w-6 h-6 text-indigo-600" />
            <span className="font-bold text-lg text-gray-900">AI Team</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Software Engineering</p>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-200 space-y-3">
          {user && (
            <div className="text-xs text-gray-600 truncate" title={user.email}>
              {user.email}
            </div>
          )}
          <button
            onClick={logout}
            className="flex items-center gap-2 text-xs text-gray-500 hover:text-red-600 transition-colors w-full"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign out
          </button>
          <div className="text-xs text-gray-400">v0.1.0</div>
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
