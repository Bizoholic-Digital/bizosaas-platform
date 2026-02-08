'use client';

import { useEffect, useState } from 'react';
import { Download, RefreshCw, X } from 'lucide-react';

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{
    outcome: 'accepted' | 'dismissed';
    platform: string;
  }>;
  prompt(): Promise<void>;
}

declare global {
  interface WindowEventMap {
    beforeinstallprompt: BeforeInstallPromptEvent;
  }
}

export default function PWAProvider({ children }: { children: React.ReactNode }) {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showInstallBanner, setShowInstallBanner] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [swRegistration, setSwRegistration] = useState<ServiceWorkerRegistration | null>(null);
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    // Check if app is already installed
    const checkIfInstalled = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const isInWebAppiOS = (window.navigator as any).standalone === true;
      setIsInstalled(isStandalone || isInWebAppiOS);
    };

    checkIfInstalled();

    // Register service worker
    const registerSW = async () => {
      if ('serviceWorker' in navigator && process.env.NEXT_PUBLIC_PWA_ENABLED === 'true') {
        try {
          const registration = await navigator.serviceWorker.register('/sw.js');
          setSwRegistration(registration);
          
          console.log('✅ Service Worker registered successfully');
          
          // Check for updates
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (newWorker) {
              newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                  setUpdateAvailable(true);
                  showNotification('App update available!', 'A new version is ready to install.');
                }
              });
            }
          });

          // Handle messages from service worker
          navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data.type === 'CACHE_UPDATED') {
              showNotification('Content updated!', 'New content is available offline.');
            }
          });

        } catch (error) {
          console.error('❌ Service Worker registration failed:', error);
        }
      }
    };

    registerSW();

    // Handle install prompt
    const handleBeforeInstallPrompt = (e: BeforeInstallPromptEvent) => {
      e.preventDefault();
      setDeferredPrompt(e);
      
      // Show install banner after a delay if not already installed
      setTimeout(() => {
        if (!isInstalled) {
          setShowInstallBanner(true);
        }
      }, 3000);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Handle app installed
    window.addEventListener('appinstalled', () => {
      setIsInstalled(true);
      setShowInstallBanner(false);
      setDeferredPrompt(null);
      showNotification('App installed!', 'CorelDove Store has been added to your home screen.');
    });

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, [isInstalled]);

  const showNotification = (title: string, message: string) => {
    // Simple notification system for CorelDove (can be enhanced with a proper toast library)
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, { body: message, icon: '/icons/icon-192x192.svg' });
    } else {
      console.log(`${title}: ${message}`);
    }
  };

  const installApp = async () => {
    if (!deferredPrompt) return;

    try {
      await deferredPrompt.prompt();
      const choiceResult = await deferredPrompt.userChoice;
      
      if (choiceResult.outcome === 'accepted') {
        console.log('✅ User accepted PWA install');
      } else {
        console.log('❌ User dismissed PWA install');
      }
    } catch (error) {
      console.error('❌ Error during PWA install:', error);
    }

    setDeferredPrompt(null);
    setShowInstallBanner(false);
  };

  const updateApp = () => {
    if (swRegistration?.waiting) {
      swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
      window.location.reload();
    }
  };

  const dismissInstallBanner = () => {
    setShowInstallBanner(false);
    localStorage.setItem('pwa-install-dismissed', Date.now().toString());
  };

  return (
    <>
      {children}
      
      {/* Install Banner */}
      {showInstallBanner && deferredPrompt && !isInstalled && (
        <div className="fixed bottom-4 left-4 right-4 z-50 md:left-auto md:right-4 md:w-96">
          <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center mb-2">
                  <Download className="w-5 h-5 text-blue-600 mr-2" />
                  <h4 className="font-semibold text-gray-900">
                    Install CorelDove App
                  </h4>
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  Shop faster with our mobile app. Access your cart offline and get instant notifications.
                </p>
                <div className="flex space-x-2">
                  <button 
                    onClick={installApp}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded text-sm font-medium"
                  >
                    Install
                  </button>
                  <button 
                    onClick={dismissInstallBanner}
                    className="border border-gray-300 hover:bg-gray-50 text-gray-700 px-3 py-1.5 rounded text-sm"
                  >
                    Not Now
                  </button>
                </div>
              </div>
              <button
                onClick={dismissInstallBanner}
                className="ml-2 p-1 hover:bg-gray-100 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Update Banner */}
      {updateAvailable && (
        <div className="fixed top-4 left-4 right-4 z-50 md:left-auto md:right-4 md:w-80">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <RefreshCw className="w-5 h-5 text-green-600 mr-2" />
              <div className="flex-1">
                <h4 className="font-medium text-green-900">
                  Update Available
                </h4>
                <p className="text-sm text-green-700">
                  Restart to get the latest features and products.
                </p>
              </div>
              <button 
                onClick={updateApp}
                className="ml-2 border border-green-300 text-green-700 hover:bg-green-50 px-3 py-1.5 rounded text-sm"
              >
                Update
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}