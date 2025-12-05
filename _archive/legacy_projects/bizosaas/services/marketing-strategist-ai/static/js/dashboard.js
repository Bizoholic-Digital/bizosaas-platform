// BizOSaaS Marketing Strategist AI Dashboard JavaScript

/**
 * Main Dashboard Controller
 */
class MarketingStrategistDashboard {
    constructor() {
        this.apiBaseUrl = '/api/v1';
        this.wsConnection = null;
        this.charts = {};
        this.refreshInterval = null;
        
        this.init();
    }
    
    async init() {
        try {
            console.log('Initializing Marketing Strategist AI Dashboard...');
            
            // Initialize real-time updates
            this.initWebSocket();
            
            // Initialize charts
            this.initCharts();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Load initial data
            await this.loadDashboardData();
            
            // Start auto-refresh
            this.startAutoRefresh();
            
            console.log('Dashboard initialized successfully');
        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            this.showErrorMessage('Failed to initialize dashboard');
        }
    }
    
    /**
     * Initialize WebSocket connection for real-time updates
     */
    initWebSocket() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            this.wsConnection = new WebSocket(wsUrl);
            
            this.wsConnection.onopen = () => {
                console.log('WebSocket connected for real-time updates');
            };
            
            this.wsConnection.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleRealtimeUpdate(data);
            };
            
            this.wsConnection.onclose = () => {
                console.log('WebSocket connection closed');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.initWebSocket(), 5000);
            };
            
            this.wsConnection.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.warn('WebSocket not available, falling back to polling');
        }
    }
    
    /**
     * Handle real-time updates from WebSocket
     */
    handleRealtimeUpdate(data) {
        switch (data.type) {
            case 'campaign_update':
                this.updateCampaignMetrics(data.payload);
                break;
            case 'performance_alert':
                this.showPerformanceAlert(data.payload);
                break;
            case 'optimization_complete':
                this.handleOptimizationComplete(data.payload);
                break;
            default:
                console.log('Unknown real-time update type:', data.type);
        }
    }
    
    /**
     * Initialize charts and visualizations
     */
    initCharts() {
        // Performance trends chart
        this.charts.performance = this.createPerformanceChart();
        
        // Platform distribution chart
        this.charts.platform = this.createPlatformChart();
        
        // ROI analysis chart
        this.charts.roi = this.createROIChart();
        
        // Budget allocation chart
        this.charts.budget = this.createBudgetChart();
    }
    
    /**
     * Create performance trends chart
     */
    createPerformanceChart() {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'ROAS',
                    data: [],
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'CTR (%)',
                    data: [],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'ROAS'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'CTR (%)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
    
    /**
     * Create platform distribution chart
     */
    createPlatformChart() {
        const ctx = document.getElementById('platformChart');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#3B82F6',
                        '#10B981',
                        '#8B5CF6',
                        '#F59E0B',
                        '#EF4444'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${percentage}%`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Create ROI analysis chart
     */
    createROIChart() {
        const ctx = document.getElementById('roiChart');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'ROAS',
                    data: [],
                    backgroundColor: function(context) {
                        const value = context.parsed.y;
                        if (value >= 4) return '#10B981';
                        if (value >= 3) return '#3B82F6';
                        if (value >= 2) return '#F59E0B';
                        return '#EF4444';
                    },
                    borderRadius: 4,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `ROAS: ${context.parsed.y.toFixed(2)}x`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'ROAS'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Platform'
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Create budget allocation chart
     */
    createBudgetChart() {
        const ctx = document.getElementById('budgetChart');
        if (!ctx) return null;
        
        return new Chart(ctx, {
            type: 'pie',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#3B82F6',
                        '#10B981',
                        '#8B5CF6',
                        '#F59E0B',
                        '#EF4444',
                        '#6B7280'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                const value = context.parsed.toLocaleString();
                                return `${context.label}: $${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Strategy generation form
        const strategyForm = document.getElementById('strategyForm');
        if (strategyForm) {
            strategyForm.addEventListener('submit', (e) => this.handleStrategyGeneration(e));
        }
        
        // Campaign optimization buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('optimize-campaign')) {
                this.handleCampaignOptimization(e.target.dataset.campaignId);
            }
            
            if (e.target.classList.contains('pause-campaign')) {
                this.handleCampaignPause(e.target.dataset.campaignId);
            }
            
            if (e.target.classList.contains('view-insights')) {
                this.handleViewInsights(e.target.dataset.campaignId);
            }
        });
        
        // Auto-refresh controls
        const refreshButton = document.getElementById('refreshButton');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => this.loadDashboardData());
        }
        
        // Filter controls
        const filterSelect = document.getElementById('filterSelect');
        if (filterSelect) {
            filterSelect.addEventListener('change', () => this.applyFilters());
        }
    }
    
    /**
     * Load dashboard data
     */
    async loadDashboardData() {
        try {
            this.showLoadingState();
            
            // Load analytics data
            const analyticsData = await this.fetchAnalyticsData();
            this.updateAnalytics(analyticsData);
            
            // Load campaigns data
            const campaignsData = await this.fetchCampaignsData();
            this.updateCampaigns(campaignsData);
            
            // Load recent activities
            const activitiesData = await this.fetchRecentActivities();
            this.updateRecentActivities(activitiesData);
            
            // Load performance alerts
            const alertsData = await this.fetchPerformanceAlerts();
            this.updatePerformanceAlerts(alertsData);
            
            this.hideLoadingState();
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.showErrorMessage('Failed to load dashboard data');
            this.hideLoadingState();
        }
    }
    
    /**
     * Fetch analytics data from API
     */
    async fetchAnalyticsData() {
        const response = await fetch(`${this.apiBaseUrl}/analytics/dashboard?tenant_id=demo-tenant`);
        if (!response.ok) throw new Error('Failed to fetch analytics data');
        return response.json();
    }
    
    /**
     * Fetch campaigns data from API
     */
    async fetchCampaignsData() {
        const response = await fetch(`${this.apiBaseUrl}/campaigns?tenant_id=demo-tenant`);
        if (!response.ok) throw new Error('Failed to fetch campaigns data');
        return response.json();
    }
    
    /**
     * Fetch recent activities
     */
    async fetchRecentActivities() {
        const response = await fetch(`${this.apiBaseUrl}/activities/recent?tenant_id=demo-tenant`);
        if (!response.ok) throw new Error('Failed to fetch activities');
        return response.json();
    }
    
    /**
     * Fetch performance alerts
     */
    async fetchPerformanceAlerts() {
        const response = await fetch(`${this.apiBaseUrl}/alerts?tenant_id=demo-tenant`);
        if (!response.ok) throw new Error('Failed to fetch alerts');
        return response.json();
    }
    
    /**
     * Update analytics display
     */
    updateAnalytics(data) {
        if (!data.success) return;
        
        const dashboard = data.dashboard;
        
        // Update overview metrics
        this.updateElement('activeCampaigns', dashboard.overview.total_campaigns);
        this.updateElement('monthlyROAS', dashboard.overview.average_roas.toFixed(1));
        this.updateElement('totalSpend', `$${dashboard.overview.total_spend.toLocaleString()}`);
        this.updateElement('totalConversions', dashboard.overview.total_conversions);
        
        // Update charts
        this.updatePerformanceChart(dashboard.performance_trends);
        this.updatePlatformChart(dashboard.platform_breakdown);
        this.updateROIChart(dashboard.platform_breakdown);
    }
    
    /**
     * Update performance chart
     */
    updatePerformanceChart(trendsData) {
        if (!this.charts.performance || !trendsData.weekly_data) return;
        
        const chart = this.charts.performance;
        const weeklyData = trendsData.weekly_data;
        
        chart.data.labels = weeklyData.map(item => item.week);
        chart.data.datasets[0].data = weeklyData.map(item => item.roas);
        chart.data.datasets[1].data = weeklyData.map(item => (item.clicks / item.impressions * 100).toFixed(2));
        
        chart.update();
    }
    
    /**
     * Update platform chart
     */
    updatePlatformChart(platformData) {
        if (!this.charts.platform || !platformData) return;
        
        const chart = this.charts.platform;
        const platforms = Object.keys(platformData);
        const revenues = platforms.map(platform => platformData[platform].revenue);
        
        chart.data.labels = platforms.map(p => p.replace('_', ' ').toUpperCase());
        chart.data.datasets[0].data = revenues;
        
        chart.update();
    }
    
    /**
     * Update ROI chart
     */
    updateROIChart(platformData) {
        if (!this.charts.roi || !platformData) return;
        
        const chart = this.charts.roi;
        const platforms = Object.keys(platformData);
        const roas = platforms.map(platform => platformData[platform].roas);
        
        chart.data.labels = platforms.map(p => p.replace('_', ' ').toUpperCase());
        chart.data.datasets[0].data = roas;
        
        chart.update();
    }
    
    /**
     * Handle strategy generation
     */
    async handleStrategyGeneration(event) {
        event.preventDefault();
        
        try {
            const formData = new FormData(event.target);
            const strategyData = {
                tenant_id: 'demo-tenant',
                client_id: 'demo-client',
                campaign_name: formData.get('campaignName'),
                objective: formData.get('objective'),
                target_audience: {
                    interests: formData.get('interests').split(',').map(i => i.trim())
                },
                budget: parseFloat(formData.get('budget')),
                duration_days: parseInt(formData.get('duration')),
                platforms: formData.getAll('platforms'),
                campaign_type: 'search',
                kpis: ['conversions', 'roas']
            };
            
            this.showLoadingSpinner('Generating AI strategy...');
            
            const response = await fetch(`${this.apiBaseUrl}/strategy/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(strategyData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayGeneratedStrategy(result.strategy);
                this.showSuccessMessage('Strategy generated successfully!');
            } else {
                throw new Error(result.message || 'Failed to generate strategy');
            }
            
        } catch (error) {
            console.error('Strategy generation failed:', error);
            this.showErrorMessage('Failed to generate strategy: ' + error.message);
        } finally {
            this.hideLoadingSpinner();
        }
    }
    
    /**
     * Display generated strategy
     */
    displayGeneratedStrategy(strategy) {
        const strategyContainer = document.getElementById('generatedStrategy');
        if (!strategyContainer) return;
        
        strategyContainer.innerHTML = `
            <div class="strategy-overview">
                <h3>Generated Strategy: ${strategy.campaign_name}</h3>
                <div class="strategy-metrics">
                    <div class="metric">
                        <label>Estimated ROI:</label>
                        <span class="value">${strategy.estimated_roi}x</span>
                    </div>
                    <div class="metric">
                        <label>Confidence Score:</label>
                        <span class="value">${(strategy.confidence_score * 100).toFixed(0)}%</span>
                    </div>
                </div>
                <div class="strategy-details">
                    <h4>Platform Strategies:</h4>
                    ${this.renderPlatformStrategies(strategy.platform_strategies)}
                    
                    <h4>Budget Allocation:</h4>
                    ${this.renderBudgetAllocation(strategy.budget_allocation)}
                    
                    <h4>Key Recommendations:</h4>
                    <ul>
                        ${strategy.optimization_opportunities.map(opp => `<li>${opp}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
        
        strategyContainer.style.display = 'block';
    }
    
    /**
     * Render platform strategies
     */
    renderPlatformStrategies(strategies) {
        return Object.entries(strategies).map(([platform, strategy]) => `
            <div class="platform-strategy">
                <h5>${platform.replace('_', ' ').toUpperCase()}</h5>
                <p>Budget: $${strategy.recommended_budget.toLocaleString()}</p>
                <p>Focus: ${strategy.optimization_focus}</p>
            </div>
        `).join('');
    }
    
    /**
     * Render budget allocation
     */
    renderBudgetAllocation(allocation) {
        return Object.entries(allocation).map(([platform, details]) => `
            <div class="budget-item">
                <span>${platform.replace('_', ' ').toUpperCase()}:</span>
                <span>$${details.budget.toLocaleString()} (${details.percentage}%)</span>
            </div>
        `).join('');
    }
    
    /**
     * Handle campaign optimization
     */
    async handleCampaignOptimization(campaignId) {
        try {
            this.showLoadingSpinner('Optimizing campaign...');
            
            const response = await fetch(`${this.apiBaseUrl}/campaign/optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    campaign_id: campaignId,
                    optimization_type: 'performance',
                    implementation_priority: 'high'
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showSuccessMessage('Campaign optimization completed!');
                this.loadDashboardData(); // Refresh data
            } else {
                throw new Error(result.message || 'Optimization failed');
            }
            
        } catch (error) {
            console.error('Campaign optimization failed:', error);
            this.showErrorMessage('Optimization failed: ' + error.message);
        } finally {
            this.hideLoadingSpinner();
        }
    }
    
    /**
     * Show loading state
     */
    showLoadingState() {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'loadingOverlay';
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = `
            <div class="loading-spinner"></div>
            <p>Loading dashboard data...</p>
        `;
        document.body.appendChild(loadingOverlay);
    }
    
    /**
     * Hide loading state
     */
    hideLoadingState() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }
    
    /**
     * Show loading spinner with message
     */
    showLoadingSpinner(message = 'Processing...') {
        // Implementation for showing loading spinner
        console.log(message);
    }
    
    /**
     * Hide loading spinner
     */
    hideLoadingSpinner() {
        // Implementation for hiding loading spinner
    }
    
    /**
     * Show success message
     */
    showSuccessMessage(message) {
        this.showNotification(message, 'success');
    }
    
    /**
     * Show error message
     */
    showErrorMessage(message) {
        this.showNotification(message, 'error');
    }
    
    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
        
        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }
    
    /**
     * Update element content
     */
    updateElement(id, content) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = content;
        }
    }
    
    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        // Refresh data every 5 minutes
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 5 * 60 * 1000);
    }
    
    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
    
    /**
     * Cleanup on page unload
     */
    destroy() {
        this.stopAutoRefresh();
        
        if (this.wsConnection) {
            this.wsConnection.close();
        }
        
        // Cleanup charts
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.marketingDashboard = new MarketingStrategistDashboard();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.marketingDashboard) {
        window.marketingDashboard.destroy();
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MarketingStrategistDashboard;
}