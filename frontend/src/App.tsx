import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CreateTask from './pages/CreateTask';
import TaskDetail from './pages/TaskDetail';
import Templates from './pages/Templates';
import Knowledge from './pages/Knowledge';
import CostTracking from './pages/CostTracking';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tasks/new" element={<CreateTask />} />
          <Route path="/tasks/:taskId" element={<TaskDetail />} />
          <Route path="/templates" element={<Templates />} />
          <Route path="/knowledge" element={<Knowledge />} />
          <Route path="/costs" element={<CostTracking />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
