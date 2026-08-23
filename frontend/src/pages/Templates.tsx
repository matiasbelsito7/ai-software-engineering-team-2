import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTemplates, createTaskFromTemplate } from '../api';
import type { Template } from '../types';
import { FileText, Play, Loader2 } from 'lucide-react';

export default function Templates() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [using, setUsing] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    getTemplates()
      .then(setTemplates)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleUseTemplate = async (template: Template) => {
    try {
      setUsing(template.template_id);
      const res = await createTaskFromTemplate(template.template_id, {});
      navigate(`/tasks/${res.task_id}`);
    } catch (err) {
      console.error('Failed to use template:', err);
      setUsing(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-6 h-6 animate-spin text-indigo-600" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Templates</h1>
        <p className="text-sm text-gray-500 mt-1">Pre-built task templates for common workflows</p>
      </div>

      {templates.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-xl border border-gray-200">
          <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">No templates available</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => (
            <div
              key={template.template_id}
              className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="font-semibold text-gray-900">{template.name}</h3>
                <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">
                  {template.category}
                </span>
              </div>
              <p className="text-sm text-gray-500 mb-4 line-clamp-3">{template.description}</p>
              {template.variables && template.variables.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs text-gray-400 mb-1">Variables:</p>
                  <div className="flex flex-wrap gap-1">
                    {template.variables.map((v) => (
                      <span key={v} className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-xs rounded">
                        {v}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              <button
                onClick={() => handleUseTemplate(template)}
                disabled={using === template.template_id}
                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
              >
                {using === template.template_id ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
                Use Template
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
