import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Bizo Hub - System Recovery',
};

const CACHE_KILLER = `
(function() {
  console.log('[Bizo Hub] Cache Killer Initializing...');
  
  // 1. Force Unregister Service Workers
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function(regs) {
      for (var reg of regs) {
        reg.unregister().then(function() { console.log('[Bizo Hub] SW Unregistered'); });
      }
    });
  }

  // 2. Clear all Caches
  if ('caches' in window) {
    caches.keys().then(function(names) {
      for (var name of names) caches.delete(name);
    });
  }

  // 3. Clear Storage
  localStorage.clear();
  sessionStorage.clear();

  // 4. Clear Cookies (Aggressive)
  var cookies = document.cookie.split(";");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf("=");
    var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=" + window.location.hostname;
  }

  console.log('[Bizo Hub] Recovery Sequence Complete.');
})();
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <script dangerouslySetInnerHTML={{ __html: CACHE_KILLER }} />
      </head>
      <body className="antialiased" data-build-version="RECOVERY_001">
        {children}
      </body>
    </html>
  );
}
