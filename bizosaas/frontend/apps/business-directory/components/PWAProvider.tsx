'use client';

import { useEffect, useState } from 'react';
import { Button } from '@bizoholic-digital/ui-components';
import { toast } from 'sonner';
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
                  toast.info('App update available!', {
                    description: 'A new version is ready to install.',
                    action: {
                      label: 'Update',
                      onClick: () => updateApp(),
                    },
                  });
                }
              });
            }
          });

          // Handle messages from service worker
          navigator.serviceWorker.addEventListener('message', (event) => {
            if (event.data.type === 'CACHE_UPDATED') {
              toast.success('Content updated!', {
                description: 'New content is available offline.',
              });
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
      toast.success('App installed!', {
        description: 'Bizoholic Marketing has been added to your home screen.',
      });
    });

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, [isInstalled]);

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
          <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center mb-2">
                  <Download className="w-5 h-5 text-blue-600 mr-2" />
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    Install Bizoholic App
                  </h4>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                  Get faster access and offline features by installing our app.
                </p>
                <div className="flex space-x-2">
                  <Button 
                    onClick={installApp}
                    size="sm"
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    Install
                  </Button>
                  <Button 
                    onClick={dismissInstallBanner}
                    variant="outline"
                    size="sm"
                  >
                    Not Now
                  </Button>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={dismissInstallBanner}
                className="ml-2 p-1"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Update Banner */}
      {updateAvailable && (
        <div className="fixed top-4 left-4 right-4 z-50 md:left-auto md:right-4 md:w-80">
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <div className="flex items-center">
              <RefreshCw className="w-5 h-5 text-green-600 mr-2" />
              <div className="flex-1">
                <h4 className="font-medium text-green-900 dark:text-green-100">
                  Update Available
                </h4>
                <p className="text-sm text-green-700 dark:text-green-300">
                  Restart to get the latest features.
                </p>
              </div>
              <Button 
                onClick={updateApp}
                size="sm"
                variant="outline"
                className="ml-2 border-green-300 text-green-700 hover:bg-green-50"
              >
                Update
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}