import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProject, getProjectPreview, downloadProject } from '../api';
import type { Project } from '../types';
import StatusBadge from '../components/StatusBadge';
import { ArrowLeft, Download, RefreshCw, Eye, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function ProjectDetail() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [project, setProject] = useState<Project | null>(null);
  const [previewHtml, setPreviewHtml] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'preview' | 'details'>('preview');
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (!projectId) return;
    setLoading(true);
    getProject(projectId)
      .then(setProject)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [projectId]);

  useEffect(() => {
    if (!projectId || !project || project.status !== 'completed') return;
    setPreviewLoading(true);
    getProjectPreview(projectId)
      .then((res) => setPreviewHtml(res.html))
      .catch(() => setPreviewHtml(null))
      .finally(() => setPreviewLoading(false));
  }, [projectId, project]);

  useEffect(() => {
    if (previewHtml && iframeRef.current) {
      const doc = iframeRef.current.contentDocument;
      if (doc) {
        doc.open();
        doc.write(previewHtml);
        doc.close();
      }
    }
  }, [previewHtml]);

  const handleDownload = async () => {
    if (!projectId || !project) return;
    setDownloading(true);
    try {
      await downloadProject(projectId, project.name);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Download failed');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12 text-gray-500">Loading project...</div>
    );
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 mb-4">Project not found</p>
        <button
          onClick={() => navigate('/')}
          className="text-indigo-600 hover:text-indigo-700 text-sm font-medium"
        >
          Back to dashboard
        </button>
      </div>
    );
  }

  const canDownload = project.status === 'completed' && project.files_path;

  return (
    <div>
      <button
        onClick={() => navigate('/')}
        className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to projects
      </button>

      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
          <p className="text-sm text-gray-500 mt-1 max-w-xl">{project.description}</p>
        </div>
        <div className="flex items-center gap-3">
          {canDownload && (
            <button
              onClick={handleDownload}
              disabled={downloading}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {downloading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              Download ZIP
            </button>
          )}
          <button
            onClick={() => {
              setLoading(true);
              getProject(project.id).then((p) => {
                setProject(p);
                setLoading(false);
              });
            }}
            className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="flex gap-4 mb-6">
        <div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
          <span className="text-xs text-gray-500">Status</span>
          <div className="mt-1">
            <StatusBadge status={project.status} />
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
          <span className="text-xs text-gray-500">Tier</span>
          <div className="mt-1 text-sm font-medium capitalize">{project.tier}</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
          <span className="text-xs text-gray-500">Tokens</span>
          <div className="mt-1 text-sm font-medium">
            {project.tokens_used > 0 ? `${(project.tokens_used / 1000).toFixed(1)}K` : '0'}
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
          <span className="text-xs text-gray-500">Iterations</span>
          <div className="mt-1 text-sm font-medium">{project.iterations_used}</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
          <span className="text-xs text-gray-500">Expires</span>
          <div className="mt-1 text-sm font-medium">
            {new Date(project.expires_at).toLocaleDateString()}
          </div>
        </div>
      </div>

      <div className="flex gap-1 border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('preview')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'preview'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <Eye className="w-4 h-4 inline mr-1.5" />
          Preview
        </button>
        <button
          onClick={() => setActiveTab('details')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'details'
              ? 'border-indigo-600 text-indigo-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Details
        </button>
      </div>

      {activeTab === 'preview' && (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          {project.status === 'generating' && (
            <div className="text-center py-16">
              <Loader2 className="w-8 h-8 text-indigo-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-500 text-sm">Generating your app...</p>
              <p className="text-gray-400 text-xs mt-1">This may take a few minutes</p>
            </div>
          )}
          {project.status === 'failed' && (
            <div className="text-center py-16">
              <p className="text-red-500 text-sm">Generation failed</p>
              <p className="text-gray-400 text-xs mt-1">Please try creating a new project</p>
            </div>
          )}
          {project.status === 'completed' && previewLoading && (
            <div className="text-center py-16">
              <Loader2 className="w-8 h-8 text-indigo-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-500 text-sm">Loading preview...</p>
            </div>
          )}
          {project.status === 'completed' && previewHtml && (
            <iframe
              ref={iframeRef}
              className="w-full h-[600px] border-0"
              title="App Preview"
            />
          )}
          {project.status === 'completed' && !previewLoading && !previewHtml && (
            <div className="text-center py-16">
              <p className="text-gray-500 text-sm">Preview not available</p>
            </div>
          )}
          {project.status === 'pending' && (
            <div className="text-center py-16">
              <p className="text-gray-500 text-sm">Project is pending</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'details' && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Project ID</div>
            <div className="text-sm font-mono text-gray-700 mt-1">{project.id}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Description</div>
            <div className="text-sm text-gray-700 mt-1">{project.description}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Created</div>
            <div className="text-sm text-gray-700 mt-1">
              {new Date(project.created_at).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Updated</div>
            <div className="text-sm text-gray-700 mt-1">
              {new Date(project.updated_at).toLocaleString()}
            </div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Expires</div>
            <div className="text-sm text-gray-700 mt-1">
              {new Date(project.expires_at).toLocaleString()}
            </div>
          </div>
          {project.files_path && (
            <div>
              <div className="text-xs text-gray-500 uppercase font-medium">Files Path</div>
              <div className="text-sm font-mono text-gray-700 mt-1">{project.files_path}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
