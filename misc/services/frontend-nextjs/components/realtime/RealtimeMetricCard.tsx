/**
 * Real-time Metric Card Component
 * Displays individual metrics with live updates and animations
 */

'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RealtimeMetricCardProps {
  title: string;
  value: number | string;
  previousValue?: number;
  change?: number;
  changeType?: 'percentage' | 'absolute';
  icon?: React.ReactNode;
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red' | 'yellow';
  format?: 'number' | 'currency' | 'percentage';
  isLoading?: boolean;
  lastUpdated?: number;
  precision?: number;
  showTrend?: boolean;
  animateChanges?: boolean;
  subtitle?: string;
}

const colorMap = {
  blue: 'text-blue-600 bg-blue-50 border-blue-200',
  green: 'text-green-600 bg-green-50 border-green-200',
  purple: 'text-purple-600 bg-purple-50 border-purple-200',
  orange: 'text-orange-600 bg-orange-50 border-orange-200',
  red: 'text-red-600 bg-red-50 border-red-200',
  yellow: 'text-yellow-600 bg-yellow-50 border-yellow-200'
};

const iconColorMap = {
  blue: 'text-blue-600',
  green: 'text-green-600',
  purple: 'text-purple-600',
  orange: 'text-orange-600',
  red: 'text-red-600',
  yellow: 'text-yellow-600'
};

export function RealtimeMetricCard({
  title,
  value,
  previousValue,
  change,
  changeType = 'percentage',
  icon,
  color = 'blue',
  format = 'number',
  isLoading = false,
  lastUpdated,
  precision = 1,
  showTrend = true,
  animateChanges = true,
  subtitle
}: RealtimeMetricCardProps) {
  const [animatedValue, setAnimatedValue] = useState<number>(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [shouldPulse, setShouldPulse] = useState(false);

  // Calculate trend direction
  const trendDirection = useMemo(() => {
    if (change === undefined || change === 0) return 'neutral';
    return change > 0 ? 'up' : 'down';
  }, [change]);

  // Format the display value
  const formatValue = (val: number | string, type: string = format) => {
    if (typeof val === 'string') return val;
    
    switch (type) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(val);
      case 'percentage':
        return `${val.toFixed(precision)}%`;
      case 'number':
      default:
        if (val >= 1000000) {
          return `${(val / 1000000).toFixed(precision)}M`;
        } else if (val >= 1000) {
          return `${(val / 1000).toFixed(precision)}K`;
        }
        return val.toString();
    }
  };

  // Animate value changes
  useEffect(() => {
    if (typeof value === 'number' && animateChanges) {
      const targetValue = value;
      const startValue = animatedValue;
      const difference = targetValue - startValue;
      
      if (Math.abs(difference) > 0) {
        setIsAnimating(true);
        setShouldPulse(true);
        
        const duration = 1000; // 1 second animation
        const steps = 60; // 60 FPS
        const stepValue = difference / steps;
        let currentStep = 0;

        const animationInterval = setInterval(() => {
          currentStep++;
          const newValue = startValue + (stepValue * currentStep);
          
          if (currentStep >= steps) {
            setAnimatedValue(targetValue);
            setIsAnimating(false);
            clearInterval(animationInterval);
          } else {
            setAnimatedValue(newValue);
          }
        }, duration / steps);

        // Remove pulse effect after animation
        setTimeout(() => setShouldPulse(false), duration + 500);

        return () => clearInterval(animationInterval);
      }
    } else if (typeof value === 'number') {
      setAnimatedValue(value);
    }
  }, [value, animateChanges]);

  // Set initial value
  useEffect(() => {
    if (typeof value === 'number' && animatedValue === 0 && value > 0) {
      setAnimatedValue(value);
    }
  }, [value]);

  const displayValue = typeof value === 'number' ? animatedValue : value;
  const timeSinceUpdate = lastUpdated ? Math.floor((Date.now() - lastUpdated) / 1000) : null;

  return (
    <div className={cn(
      "bg-white p-6 rounded-lg shadow border transition-all duration-300",
      shouldPulse && "ring-2 ring-blue-200 shadow-lg",
      "hover:shadow-md"
    )}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">{title}</h3>
            {isLoading && (
              <Loader2 className="h-4 w-4 text-gray-400 animate-spin" />
            )}
          </div>
          
          <div className="flex items-baseline space-x-2">
            <span className={cn(
              "text-2xl font-bold text-gray-900 transition-all duration-300",
              isAnimating && "scale-110"
            )}>
              {formatValue(displayValue)}
            </span>
            
            {showTrend && change !== undefined && (
              <div className="flex items-center space-x-1">
                {trendDirection === 'up' && (
                  <TrendingUp className="h-4 w-4 text-green-500" />
                )}
                {trendDirection === 'down' && (
                  <TrendingDown className="h-4 w-4 text-red-500" />
                )}
                {trendDirection === 'neutral' && (
                  <Minus className="h-4 w-4 text-gray-400" />
                )}
                <span className={cn(
                  "text-sm font-medium",
                  trendDirection === 'up' && "text-green-600",
                  trendDirection === 'down' && "text-red-600",
                  trendDirection === 'neutral' && "text-gray-500"
                )}>
                  {changeType === 'percentage' ? 
                    `${change > 0 ? '+' : ''}${change.toFixed(precision)}%` :
                    `${change > 0 ? '+' : ''}${formatValue(change)}`
                  }
                </span>
              </div>
            )}
          </div>

          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}

          {/* Real-time indicator */}
          <div className="flex items-center justify-between mt-3">
            <div className="flex items-center space-x-2">
              <div className={cn(
                "w-2 h-2 rounded-full",
                lastUpdated && (Date.now() - lastUpdated) < 30000 ? 
                  "bg-green-500 animate-pulse" : 
                  "bg-gray-300"
              )} />
              <span className="text-xs text-gray-500">
                {timeSinceUpdate !== null ? (
                  timeSinceUpdate < 60 ? 
                    `Updated ${timeSinceUpdate}s ago` :
                    `Updated ${Math.floor(timeSinceUpdate / 60)}m ago`
                ) : (
                  'No recent updates'
                )}
              </span>
            </div>
          </div>
        </div>

        {icon && (
          <div className={cn(
            "flex items-center justify-center w-12 h-12 rounded-lg border",
            colorMap[color]
          )}>
            <div className={iconColorMap[color]}>
              {icon}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Component for displaying multiple metrics in a grid
interface RealtimeMetricsGridProps {
  metrics: Array<Omit<RealtimeMetricCardProps, 'isLoading'> & { id: string }>;
  columns?: 1 | 2 | 3 | 4 | 5;
  isLoading?: boolean;
  className?: string;
}

export function RealtimeMetricsGrid({ 
  metrics, 
  columns = 4, 
  isLoading = false,
  className 
}: RealtimeMetricsGridProps) {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
    5: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-5'
  };

  return (
    <div className={cn(
      "grid gap-6",
      gridCols[columns],
      className
    )}>
      {metrics.map((metric) => (
        <RealtimeMetricCard
          key={metric.id}
          {...metric}
          isLoading={isLoading}
        />
      ))}
    </div>
  );
}

export default RealtimeMetricCard;