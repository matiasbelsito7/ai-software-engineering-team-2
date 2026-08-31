import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProject, getTiers } from '../api';
import type { TierInfo } from '../types';
import { ArrowLeft, ArrowRight, Check, Loader2, Sparkles } from 'lucide-react';

const steps = ['Describe your app', 'Choose a plan', 'Review & create'];

export default function CreateProject() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedTier, setSelectedTier] = useState('free');
  const [tiers, setTiers] = useState<TierInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [tiersLoading, setTiersLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getTiers()
      .then(setTiers)
      .catch(() => setError('Failed to load plans'))
      .finally(() => setTiersLoading(false));
  }, []);

  const canNext = () => {
    if (step === 0) return name.trim().length > 0 && description.trim().length > 0;
    if (step === 1) return !!selectedTier;
    return true;
  };

  const handleCreate = async () => {
    setLoading(true);
    setError('');
    try {
      const project = await createProject({
        name: name.trim(),
        description: description.trim(),
        tier: selectedTier,
      });
      navigate(`/projects/${project.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create project');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to projects
      </button>

      <h1 className="text-2xl font-bold text-gray-900 mb-2">Create a new project</h1>
      <p className="text-sm text-gray-500 mb-8">
        Describe your app in plain language and let the AI team build it for you.
      </p>

      <div className="flex items-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div
              className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-medium ${
                i < step
                  ? 'bg-indigo-600 text-white'
                  : i === step
                  ? 'bg-indigo-100 text-indigo-700 ring-2 ring-indigo-600'
                  : 'bg-gray-100 text-gray-500'
              }`}
            >
              {i < step ? <Check className="w-3.5 h-3.5" /> : i + 1}
            </div>
            <span className={`text-xs ${i === step ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
              {s}
            </span>
            {i < steps.length - 1 && <div className="w-8 h-px bg-gray-300 mx-1" />}
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      )}

      {step === 0 && (
        <div className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              What's your app called?
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. My Task Manager"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              What does it do?
            </label>
            <textarea
              id="description"
              rows={6}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your app in plain language. For example: A task management app where users can create, edit, and delete tasks, set due dates, and mark tasks as complete. Include user authentication and a dashboard with task statistics."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
            />
            <p className="text-xs text-gray-400 mt-2">
              The more detail you provide, the better the result.
            </p>
          </div>
        </div>
      )}

      {step === 1 && (
        <div>
          {tiersLoading ? (
            <div className="text-center py-12 text-gray-500">Loading plans...</div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {tiers.map((tier) => (
                <button
                  key={tier.name}
                  onClick={() => setSelectedTier(tier.name)}
                  className={`text-left p-5 rounded-xl border-2 transition-all ${
                    selectedTier === tier.name
                      ? 'border-indigo-600 bg-indigo-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-gray-900">{tier.display_name}</span>
                    {selectedTier === tier.name && (
                      <div className="w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center">
                        <Check className="w-3 h-3 text-white" />
                      </div>
                    )}
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-3">
                    {tier.price_monthly === 0 ? 'Free' : `$${tier.price_monthly}`}
                    {tier.price_monthly > 0 && (
                      <span className="text-sm font-normal text-gray-500">/mo</span>
                    )}
                  </div>
                  <ul className="space-y-1.5 text-xs text-gray-600">
                    <li>{tier.tokens_per_project >= 1_000_000 ? `${tier.tokens_per_project / 1_000_000}M` : `${tier.tokens_per_project / 1_000}K`} tokens per project</li>
                    <li>{tier.max_iterations} iterations</li>
                    <li>{tier.max_projects === -1 ? 'Unlimited' : tier.max_projects} projects</li>
                    <li>{tier.retention_days} days retention</li>
                    {tier.can_download_code && <li className="text-indigo-600 font-medium">Download code</li>}
                  </ul>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {step === 2 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Project</div>
            <div className="text-sm font-medium text-gray-900 mt-1">{name}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Description</div>
            <div className="text-sm text-gray-700 mt-1">{description}</div>
          </div>
          <div>
            <div className="text-xs text-gray-500 uppercase font-medium">Plan</div>
            <div className="text-sm font-medium text-gray-900 mt-1 capitalize">
              {tiers.find((t) => t.name === selectedTier)?.display_name || selectedTier}
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between mt-8">
        <button
          onClick={() => (step === 0 ? navigate('/') : setStep(step - 1))}
          className="px-5 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          {step === 0 ? 'Cancel' : 'Back'}
        </button>
        {step < 2 ? (
          <button
            onClick={() => setStep(step + 1)}
            disabled={!canNext()}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
            <ArrowRight className="w-4 h-4" />
          </button>
        ) : (
          <button
            onClick={handleCreate}
            disabled={loading}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Sparkles className="w-4 h-4" />
            )}
            {loading ? 'Creating...' : 'Create Project'}
          </button>
        )}
      </div>
    </div>
  );
}
