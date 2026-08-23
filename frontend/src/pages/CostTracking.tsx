import { useEffect, useState } from 'react';
import { getCostSummary, getCostRecords, getBudgets } from '../api';
import type { CostSummary, CostRecord, Budget } from '../types';
import { DollarSign, TrendingUp, Activity, Wallet, Loader2 } from 'lucide-react';

export default function CostTracking() {
  const [summary, setSummary] = useState<CostSummary | null>(null);
  const [records, setRecords] = useState<CostRecord[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCostSummary(), getCostRecords(1, 50), getBudgets()])
      .then(([s, r, b]) => { setSummary(s); setRecords(r.items); setBudgets(b); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

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
        <h1 className="text-2xl font-bold text-gray-900">Cost Tracking</h1>
        <p className="text-sm text-gray-500 mt-1">Monitor LLM usage and costs</p>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-50 rounded-lg">
                <DollarSign className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-xs text-gray-500">Total Cost</p>
                <p className="text-xl font-bold text-gray-900">${summary.total_cost.toFixed(4)}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-50 rounded-lg">
                <TrendingUp className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-xs text-gray-500">Input Tokens</p>
                <p className="text-xl font-bold text-gray-900">{summary.total_input_tokens.toLocaleString()}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-50 rounded-lg">
                <Activity className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="text-xs text-gray-500">Output Tokens</p>
                <p className="text-xl font-bold text-gray-900">{summary.total_output_tokens.toLocaleString()}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-orange-50 rounded-lg">
                <Wallet className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <p className="text-xs text-gray-500">Records</p>
                <p className="text-xl font-bold text-gray-900">{summary.records_count}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cost Records */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="font-semibold text-gray-900">Usage Records</h2>
          </div>
          <div className="overflow-auto max-h-96">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left px-6 py-2 text-xs font-medium text-gray-500 uppercase">Model</th>
                  <th className="text-left px-6 py-2 text-xs font-medium text-gray-500 uppercase">Provider</th>
                  <th className="text-right px-6 py-2 text-xs font-medium text-gray-500 uppercase">Input</th>
                  <th className="text-right px-6 py-2 text-xs font-medium text-gray-500 uppercase">Output</th>
                  <th className="text-right px-6 py-2 text-xs font-medium text-gray-500 uppercase">Cost</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {records.map((r) => (
                  <tr key={r.record_id} className="hover:bg-gray-50">
                    <td className="px-6 py-3 text-sm font-medium text-gray-900">{r.model}</td>
                    <td className="px-6 py-3 text-sm text-gray-500">{r.provider}</td>
                    <td className="px-6 py-3 text-sm text-gray-500 text-right">{r.input_tokens.toLocaleString()}</td>
                    <td className="px-6 py-3 text-sm text-gray-500 text-right">{r.output_tokens.toLocaleString()}</td>
                    <td className="px-6 py-3 text-sm text-gray-900 text-right font-medium">${r.cost.toFixed(4)}</td>
                  </tr>
                ))}
                {records.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-sm text-gray-400">
                      No records yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Budgets */}
        <div className="bg-white rounded-xl border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="font-semibold text-gray-900">Budgets</h2>
          </div>
          <div className="p-6 space-y-4">
            {budgets.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-4">No budgets configured</p>
            ) : (
              budgets.map((b) => {
                const pct = b.limit > 0 ? (b.used / b.limit) * 100 : 0;
                return (
                  <div key={b.budget_id}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium text-gray-900">{b.name}</span>
                      <span className="text-gray-500">${b.used.toFixed(2)} / ${b.limit.toFixed(2)}</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          pct > 90 ? 'bg-red-500' : pct > 70 ? 'bg-yellow-500' : 'bg-green-500'
                        }`}
                        style={{ width: `${Math.min(100, pct)}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-400 mt-1">{pct.toFixed(0)}% used · {b.period}</p>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
