/**
 * Real-time Chart Components
 * Interactive charts with live data updates and smooth animations
 */

'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { TrendingUp, TrendingDown, BarChart3, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChartDataPoint {
  timestamp: number;
  value: number;
  label?: string;
  [key: string]: any;
}

interface RealtimeChartProps {
  data: ChartDataPoint[];
  type: 'line' | 'area' | 'bar' | 'pie';
  height?: number;
  color?: string;
  title?: string;
  showGrid?: boolean;
  animate?: boolean;
  maxDataPoints?: number;
  yAxisLabel?: string;
  xAxisLabel?: string;
  formatValue?: (value: number) => string;
  formatTooltip?: (value: number, label: string) => [string, string];
  isRealtime?: boolean;
  updateInterval?: number;
}

const defaultColors = {
  primary: '#3B82F6',
  secondary: '#10B981',
  accent: '#8B5CF6',
  warning: '#F59E0B',
  danger: '#EF4444'
};

export function RealtimeChart({
  data,
  type,
  height = 300,
  color = defaultColors.primary,
  title,
  showGrid = true,
  animate = true,
  maxDataPoints = 50,
  yAxisLabel,
  xAxisLabel,
  formatValue = (value) => value.toString(),
  formatTooltip,
  isRealtime = true,
  updateInterval = 1000
}: RealtimeChartProps) {
  const [chartData, setChartData] = useState<ChartDataPoint[]>(data);
  const [isUpdating, setIsUpdating] = useState(false);

  // Manage data updates
  useEffect(() => {
    setIsUpdating(true);
    
    // Limit data points for performance
    const limitedData = data.slice(-maxDataPoints);
    
    // Add timestamp formatting
    const formattedData = limitedData.map(point => ({
      ...point,
      formattedTime: new Date(point.timestamp).toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }));

    setChartData(formattedData);
    
    // Reset updating state after animation
    setTimeout(() => setIsUpdating(false), 300);
  }, [data, maxDataPoints]);

  // Calculate trend
  const trend = useMemo(() => {
    if (chartData.length < 2) return null;
    
    const latest = chartData[chartData.length - 1].value;
    const previous = chartData[chartData.length - 2].value;
    const change = ((latest - previous) / previous) * 100;
    
    return {
      direction: change > 0 ? 'up' : change < 0 ? 'down' : 'neutral',
      percentage: Math.abs(change)
    };
  }, [chartData]);

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const value = payload[0].value;
      const formattedValue = formatValue(value);
      
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm text-gray-600">{`Time: ${label}`}</p>
          <p className="text-sm font-semibold text-gray-900">
            {formatTooltip ? formatTooltip(value, label)[0] : formattedValue}
          </p>
          {isRealtime && (
            <div className="flex items-center mt-1">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2" />
              <span className="text-xs text-green-600">Live</span>
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  const renderChart = () => {
    const commonProps = {
      data: chartData,
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };

    const animationProps = animate ? {
      animationBegin: 0,
      animationDuration: 300,
      animationEasing: 'ease-out'
    } : {};

    switch (type) {
      case 'line':
        return (
          <LineChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
            <XAxis 
              dataKey="formattedTime" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
              tickFormatter={formatValue}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="value"
              stroke={color}
              strokeWidth={2}
              dot={{ fill: color, strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, fill: color }}
              {...animationProps}
            />
          </LineChart>
        );

      case 'area':
        return (
          <AreaChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
            <XAxis 
              dataKey="formattedTime" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
              tickFormatter={formatValue}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="value"
              stroke={color}
              fill={`${color}20`}
              strokeWidth={2}
              {...animationProps}
            />
          </AreaChart>
        );

      case 'bar':
        return (
          <BarChart {...commonProps}>
            {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />}
            <XAxis 
              dataKey="formattedTime" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
              tickFormatter={formatValue}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar
              dataKey="value"
              fill={color}
              radius={[2, 2, 0, 0]}
              {...animationProps}
            />
          </BarChart>
        );

      case 'pie':
        const pieColors = [color, `${color}CC`, `${color}99`, `${color}66`, `${color}33`];
        return (
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              {...animationProps}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        );

      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      {/* Chart Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          {title && (
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          )}
          
          {isRealtime && (
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs text-green-600 font-medium">Live</span>
            </div>
          )}
        </div>

        {/* Trend Indicator */}
        {trend && (
          <div className="flex items-center space-x-2">
            {trend.direction === 'up' && (
              <TrendingUp className="h-4 w-4 text-green-500" />
            )}
            {trend.direction === 'down' && (
              <TrendingDown className="h-4 w-4 text-red-500" />
            )}
            {trend.direction === 'neutral' && (
              <Activity className="h-4 w-4 text-gray-400" />
            )}
            <span className={cn(
              "text-sm font-medium",
              trend.direction === 'up' && "text-green-600",
              trend.direction === 'down' && "text-red-600",
              trend.direction === 'neutral' && "text-gray-500"
            )}>
              {trend.percentage.toFixed(1)}%
            </span>
          </div>
        )}
      </div>

      {/* Chart Container */}
      <div className={cn(
        "transition-all duration-300",
        isUpdating && "opacity-90 scale-[0.99]"
      )} style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>

      {/* Chart Footer */}
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-4 text-xs text-gray-500">
          <span>Data Points: {chartData.length}</span>
          {maxDataPoints && (
            <span>Max: {maxDataPoints}</span>
          )}
        </div>
        
        <div className="text-xs text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

// Multi-series chart component
interface MultiSeriesChartProps {
  data: ChartDataPoint[];
  series: Array<{
    key: string;
    name: string;
    color: string;
    type?: 'line' | 'area' | 'bar';
  }>;
  height?: number;
  title?: string;
  showLegend?: boolean;
}

export function RealtimeMultiSeriesChart({
  data,
  series,
  height = 300,
  title,
  showLegend = true
}: MultiSeriesChartProps) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}
      
      {showLegend && (
        <div className="flex items-center space-x-4 mb-4">
          {series.map((s) => (
            <div key={s.key} className="flex items-center space-x-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: s.color }}
              />
              <span className="text-sm text-gray-600">{s.name}</span>
            </div>
          ))}
        </div>
      )}

      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="formattedTime" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 12, fill: '#6B7280' }}
            />
            <Tooltip />
            {series.map((s) => (
              <Line
                key={s.key}
                type="monotone"
                dataKey={s.key}
                stroke={s.color}
                strokeWidth={2}
                dot={{ fill: s.color, strokeWidth: 2, r: 3 }}
                activeDot={{ r: 5, fill: s.color }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default RealtimeChart;