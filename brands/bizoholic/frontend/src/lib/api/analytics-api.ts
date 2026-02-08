/**
 * Formats a numeric value based on the specified type
 */
export function formatMetricValue(value: number, type: 'currency' | 'number' | 'percentage' | 'time'): string {
    if (value === undefined || value === null) return '0';

    switch (type) {
        case 'currency':
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
            }).format(value);
        case 'percentage':
            return `${value.toFixed(1)}%`;
        case 'time':
            if (value >= 3600) return `${(value / 3600).toFixed(1)}h`;
            if (value >= 60) return `${(value / 60).toFixed(1)}m`;
            return `${value.toFixed(0)}s`;
        case 'number':
        default:
            return value.toLocaleString();
    }
}

/**
 * Generates an array of colors for charts
 */
export function generateChartColors(count: number): string[] {
    const baseColors = [
        '#3B82F6', // blue-500
        '#10B981', // emerald-500
        '#F59E0B', // amber-500
        '#EF4444', // red-500
        '#8B5CF6', // purple-500
        '#EC4899', // pink-500
        '#06B6D4', // cyan-500
        '#F97316', // orange-500
    ];

    if (count <= baseColors.length) {
        return baseColors.slice(0, count);
    }

    // Generate more colors if needed
    const colors = [...baseColors];
    for (let i = baseColors.length; i < count; i++) {
        const hue = (i * 137.508) % 360; // Use golden angle for even distribution
        colors.push(`hsl(${hue}, 70%, 50%)`);
    }

    return colors;
}
