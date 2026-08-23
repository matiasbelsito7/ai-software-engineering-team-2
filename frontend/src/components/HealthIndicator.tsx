import { useEffect, useState } from 'react';
import { getHealth } from '../api';
import { CheckCircle, XCircle } from 'lucide-react';

export default function HealthIndicator() {
  const [healthy, setHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const check = async () => {
      try {
        await getHealth();
        setHealthy(true);
      } catch {
        setHealthy(false);
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  if (healthy === null) return null;

  return (
    <div className="flex items-center gap-1.5 text-xs">
      {healthy ? (
        <>
          <CheckCircle className="w-3.5 h-3.5 text-green-500" />
          <span className="text-green-700">API Connected</span>
        </>
      ) : (
        <>
          <XCircle className="w-3.5 h-3.5 text-red-500" />
          <span className="text-red-700">API Offline</span>
        </>
      )}
    </div>
  );
}
