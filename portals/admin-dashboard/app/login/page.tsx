'use client';

import React from 'react';

export default function AdminLoginPage() {
  return (
    <div className="p-20 flex flex-col items-center justify-center bg-white min-h-screen">
      <h1 className="text-4xl font-bold text-red-600 border-4 border-red-600 p-10">
        LOGIN PAGE IS RENDERING TEST
      </h1>
      <p className="mt-4 text-black text-xl">
        If you see this, the page is working.
      </p>
      <div className="mt-8">
        {/* We will re-add clerk here once we confirm this shows up */}
        [CLERK COMPONENT REMOVED FOR TEST]
      </div>
    </div>
  );
}