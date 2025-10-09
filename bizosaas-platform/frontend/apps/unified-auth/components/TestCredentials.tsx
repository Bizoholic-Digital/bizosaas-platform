'use client';

interface Credential {
  role: string;
  email: string;
  password: string;
  description: string;
  color: string;
  accessTo: string[];
}

const credentials: Credential[] = [
  {
    role: 'SuperAdmin',
    email: 'superadmin@bizosaas.com',
    password: 'BizoSaaS2025!Admin',
    description: 'Full platform access',
    color: 'bg-red-50 border-red-300 text-red-800 hover:bg-red-100',
    accessTo: ['SQLAdmin (8005)', 'Admin Dashboard (3009)', 'Client Portal (3001)']
  },
  {
    role: 'Admin',
    email: 'administrator@bizosaas.com',
    password: 'Bizoholic2025!Admin',
    description: 'Tenant administration',
    color: 'bg-blue-50 border-blue-300 text-blue-800 hover:bg-blue-100',
    accessTo: ['Admin Dashboard (3009)', 'Client Portal (3001)']
  },
  {
    role: 'User',
    email: 'user@bizosaas.com',
    password: 'Bizoholic2025!User',
    description: 'Client access only',
    color: 'bg-green-50 border-green-300 text-green-800 hover:bg-green-100',
    accessTo: ['Client Portal (3001)']
  }
];

export default function TestCredentials({
  onSelectCredential
}: {
  onSelectCredential: (email: string, password: string) => void;
}) {
  return (
    <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-700">
          🧪 Test Credentials
        </h3>
        <span className="text-xs text-gray-500 bg-yellow-100 px-2 py-1 rounded">
          Development Mode
        </span>
      </div>

      <div className="space-y-2">
        {credentials.map((cred) => (
          <button
            key={cred.role}
            onClick={() => onSelectCredential(cred.email, cred.password)}
            className={`w-full text-left p-3 rounded-lg border-2 transition-all ${cred.color}`}
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="font-semibold text-sm">{cred.role}</div>
                <div className="text-xs opacity-75 mt-1">{cred.description}</div>
                <div className="text-xs font-mono mt-1 bg-white/50 px-2 py-1 rounded inline-block">
                  {cred.email}
                </div>
              </div>
              <svg
                className="w-5 h-5 opacity-50"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M9 5l7 7-7 7"></path>
              </svg>
            </div>
            <div className="mt-2 flex flex-wrap gap-1">
              {cred.accessTo.map((access, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-white/70 px-2 py-0.5 rounded"
                >
                  {access}
                </span>
              ))}
            </div>
          </button>
        ))}
      </div>

      <div className="mt-3 text-xs text-gray-500 text-center">
        Click any credential to auto-fill and login
      </div>
    </div>
  );
}