'use client';

import { useState, useEffect, useRef, ReactNode } from 'react';
import { RefreshCw } from 'lucide-react';

interface PullToRefreshProps {
  onRefresh: () => Promise<void>;
  children: ReactNode;
  threshold?: number;
  resistance?: number;
  refreshingText?: string;
  pullText?: string;
  releaseText?: string;
}

export default function PullToRefresh({
  onRefresh,
  children,
  threshold = 80,
  resistance = 2.5,
  refreshingText = 'Refreshing...',
  pullText = 'Pull to refresh',
  releaseText = 'Release to refresh',
}: PullToRefreshProps) {
  const [pullDistance, setPullDistance] = useState(0);
  const [isPulling, setIsPulling] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [canRefresh, setCanRefresh] = useState(false);
  
  const containerRef = useRef<HTMLDivElement>(null);
  const startY = useRef(0);
  const currentY = useRef(0);
  const isDragging = useRef(false);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    let rafId: number;

    const handleTouchStart = (e: TouchEvent) => {
      if (container.scrollTop === 0) {
        startY.current = e.touches[0].clientY;
        isDragging.current = true;
        setIsPulling(true);
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!isDragging.current || isRefreshing) return;

      currentY.current = e.touches[0].clientY;
      const deltaY = currentY.current - startY.current;

      if (deltaY > 0 && container.scrollTop === 0) {
        e.preventDefault();
        
        const distance = Math.max(0, deltaY / resistance);
        
        rafId = requestAnimationFrame(() => {
          setPullDistance(distance);
          setCanRefresh(distance >= threshold);
        });
      }
    };

    const handleTouchEnd = async () => {
      if (!isDragging.current) return;

      isDragging.current = false;
      setIsPulling(false);

      if (canRefresh && !isRefreshing) {
        setIsRefreshing(true);
        setPullDistance(threshold);
        
        try {
          await onRefresh();
        } catch (error) {
          console.error('Refresh failed:', error);
        } finally {
          setIsRefreshing(false);
          setPullDistance(0);
          setCanRefresh(false);
        }
      } else {
        // Animate back to 0
        let currentDistance = pullDistance;
        const animate = () => {
          currentDistance *= 0.8;
          if (currentDistance < 1) {
            setPullDistance(0);
            setCanRefresh(false);
            return;
          }
          setPullDistance(currentDistance);
          requestAnimationFrame(animate);
        };
        animate();
      }
    };

    const handleScroll = () => {
      if (container.scrollTop > 0) {
        setIsPulling(false);
        setPullDistance(0);
        setCanRefresh(false);
        isDragging.current = false;
      }
    };

    // Add event listeners
    container.addEventListener('touchstart', handleTouchStart, { passive: false });
    container.addEventListener('touchmove', handleTouchMove, { passive: false });
    container.addEventListener('touchend', handleTouchEnd);
    container.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      container.removeEventListener('touchstart', handleTouchStart);
      container.removeEventListener('touchmove', handleTouchMove);
      container.removeEventListener('touchend', handleTouchEnd);
      container.removeEventListener('scroll', handleScroll);
      
      if (rafId) {
        cancelAnimationFrame(rafId);
      }
    };
  }, [canRefresh, isRefreshing, pullDistance, threshold, resistance, onRefresh]);

  const getStatusText = () => {
    if (isRefreshing) return refreshingText;
    if (canRefresh) return releaseText;
    return pullText;
  };

  const getOpacity = () => {
    if (isRefreshing) return 1;
    return Math.min(pullDistance / threshold, 1);
  };

  const getRotation = () => {
    if (isRefreshing) return 'animate-spin';
    return '';
  };

  return (
    <div 
      ref={containerRef}
      className="relative h-full overflow-auto"
      style={{
        transform: `translateY(${Math.min(pullDistance, threshold)}px)`,
        transition: isDragging.current ? 'none' : 'transform 0.3s ease-out',
      }}
    >
      {/* Pull to refresh indicator */}
      <div 
        className="absolute top-0 left-0 right-0 flex items-center justify-center bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 z-50"
        style={{
          height: `${Math.min(pullDistance, threshold)}px`,
          transform: `translateY(-${Math.min(pullDistance, threshold)}px)`,
          opacity: getOpacity(),
          transition: isDragging.current ? 'none' : 'opacity 0.3s ease-out',
        }}
      >
        <div className="flex flex-col items-center justify-center space-y-2">
          <RefreshCw 
            className={`w-6 h-6 ${getRotation()}`}
            style={{
              transform: `rotate(${pullDistance * 2}deg)`,
            }}
          />
          <span className="text-sm font-medium">
            {getStatusText()}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}