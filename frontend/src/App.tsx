import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CreateProject from './pages/CreateProject';
import CreateTask from './pages/CreateTask';
import TaskDetail from './pages/TaskDetail';
import Templates from './pages/Templates';
import Knowledge from './pages/Knowledge';
import CostTracking from './pages/CostTracking';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/projects/new" element={<CreateProject />} />
              <Route path="/tasks/new" element={<CreateTask />} />
              <Route path="/tasks/:taskId" element={<TaskDetail />} />
              <Route path="/templates" element={<Templates />} />
              <Route path="/knowledge" element={<Knowledge />} />
              <Route path="/costs" element={<CostTracking />} />
            </Route>
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
