// Analytics and Chart Management
class HealthAnalytics {
    constructor() {
        this.charts = {};
        this.apiBaseUrl = window.location.origin;
        this.init();
    }

    async init() {
        await this.loadHealthStats();
        await this.loadDataTypesChart();
        await this.loadTimelineChart();
        await this.loadHeartRateChart();
        await this.loadActivityChart();
        await this.loadHealthInsights();
        await this.loadRecentActivity();
    }

    // Load health statistics
    async loadHealthStats() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/health-stats`);
            const data = await response.json();
            
            if (response.ok) {
                this.updateHealthStats(data);
            } else {
                console.error('Failed to load health stats:', data.error);
            }
        } catch (error) {
            console.error('Error loading health stats:', error);
        }
    }

    updateHealthStats(data) {
        document.getElementById('avg-heart-rate').textContent = data.avg_heart_rate || 'N/A';
        document.getElementById('total-steps').textContent = this.formatNumber(data.total_steps) || '0';
        document.getElementById('total-calories').textContent = this.formatNumber(data.total_calories) || '0';
        document.getElementById('avg-sleep').textContent = data.avg_sleep_hours || 'N/A';
    }

    // Load data types distribution chart
    async loadDataTypesChart() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/data-types`);
            const data = await response.json();
            
            if (response.ok) {
                this.createDataTypesChart(data.data_types);
            } else {
                console.error('Failed to load data types:', data.error);
            }
        } catch (error) {
            console.error('Error loading data types:', error);
        }
    }

    createDataTypesChart(dataTypes) {
        const ctx = document.getElementById('data-types-chart').getContext('2d');
        
        if (this.charts.dataTypes) {
            this.charts.dataTypes.destroy();
        }

        this.charts.dataTypes = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: dataTypes.map(item => this.formatRecordType(item.type)),
                datasets: [{
                    data: dataTypes.map(item => item.count),
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF',
                        '#4BC0C0', '#FF6384'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Load timeline chart
    async loadTimelineChart() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/timeline`);
            const data = await response.json();
            
            if (response.ok) {
                this.createTimelineChart(data);
            } else {
                console.error('Failed to load timeline data:', data.error);
            }
        } catch (error) {
            console.error('Error loading timeline data:', error);
        }
    }

    createTimelineChart(data) {
        const ctx = document.getElementById('timeline-chart').getContext('2d');
        
        if (this.charts.timeline) {
            this.charts.timeline.destroy();
        }

        // Prepare data for the last 30 days
        const last30Days = this.getLast30Days();
        const stepsData = this.fillMissingDates(data.daily_steps, last30Days, 'steps');
        const heartRateData = this.fillMissingDates(data.daily_heart_rate, last30Days, 'heart_rate');

        this.charts.timeline = new Chart(ctx, {
            type: 'line',
            data: {
                labels: last30Days.map(date => new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
                datasets: [
                    {
                        label: 'Steps',
                        data: stepsData,
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Heart Rate (BPM)',
                        data: heartRateData,
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Steps'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Heart Rate (BPM)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });
    }

    // Load heart rate trends chart
    async loadHeartRateChart() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/heart-rate-trends`);
            const data = await response.json();
            
            if (response.ok) {
                this.createHeartRateChart(data.heart_rate_trends);
            } else {
                console.error('Failed to load heart rate trends:', data.error);
            }
        } catch (error) {
            console.error('Error loading heart rate trends:', error);
        }
    }

    createHeartRateChart(heartRateData) {
        const ctx = document.getElementById('heart-rate-chart').getContext('2d');
        
        if (this.charts.heartRate) {
            this.charts.heartRate.destroy();
        }

        this.charts.heartRate = new Chart(ctx, {
            type: 'line',
            data: {
                labels: heartRateData.map(item => new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })),
                datasets: [
                    {
                        label: 'Average Heart Rate',
                        data: heartRateData.map(item => item.avg),
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Min Heart Rate',
                        data: heartRateData.map(item => item.min),
                        borderColor: '#4BC0C0',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        borderDash: [5, 5]
                    },
                    {
                        label: 'Max Heart Rate',
                        data: heartRateData.map(item => item.max),
                        borderColor: '#FF9F40',
                        backgroundColor: 'rgba(255, 159, 64, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Heart Rate (BPM)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                }
            }
        });
    }

    // Load daily activity chart
    async loadActivityChart() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/daily-summary`);
            const data = await response.json();
            
            if (response.ok) {
                this.createActivityChart(data.daily_summary);
            } else {
                console.error('Failed to load daily summary:', data.error);
            }
        } catch (error) {
            console.error('Error loading daily summary:', error);
        }
    }

    createActivityChart(dailySummary) {
        const ctx = document.getElementById('activity-chart').getContext('2d');
        
        if (this.charts.activity) {
            this.charts.activity.destroy();
        }

        this.charts.activity = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Steps', 'Calories', 'Heart Rate', 'Distance (km)'],
                datasets: [{
                    label: 'Today\'s Activity',
                    data: [
                        dailySummary.steps,
                        dailySummary.calories,
                        dailySummary.avg_heart_rate,
                        dailySummary.distance_km
                    ],
                    backgroundColor: [
                        '#36A2EB',
                        '#FF6384',
                        '#FFCE56',
                        '#4BC0C0'
                    ],
                    borderColor: [
                        '#36A2EB',
                        '#FF6384',
                        '#FFCE56',
                        '#4BC0C0'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Activity Type'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Value'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed.y;
                                
                                if (label === 'Steps') return `Steps: ${value.toLocaleString()}`;
                                if (label === 'Calories') return `Calories: ${value.toLocaleString()}`;
                                if (label === 'Heart Rate') return `Heart Rate: ${value} BPM`;
                                if (label === 'Distance (km)') return `Distance: ${value} km`;
                                
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Load health insights and recommendations
    async loadHealthInsights() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/health-insights`);
            const data = await response.json();
            
            if (response.ok) {
                this.updateHealthInsights(data.insights);
            } else {
                console.error('Failed to load health insights:', data.error);
            }
        } catch (error) {
            console.error('Error loading health insights:', error);
        }
    }

    updateHealthInsights(insights) {
        // Update recovery score
        const scoreNumber = document.getElementById('score-number');
        const scoreLevel = document.getElementById('score-level');
        
        if (insights.recovery_score) {
            scoreNumber.textContent = insights.recovery_score.score;
            scoreLevel.textContent = insights.recovery_score.level;
            scoreLevel.className = `score-level ${insights.recovery_score.level}`;
        }

        // Update workout recommendation
        const recommendationType = document.getElementById('recommendation-type');
        const recommendationReason = document.getElementById('recommendation-reason');
        const recommendationSuggestions = document.getElementById('recommendation-suggestions');

        if (insights.workout_recommendation) {
            const rec = insights.workout_recommendation;
            
            recommendationType.textContent = rec.recommendation.replace('_', ' ');
            recommendationType.className = `recommendation-type ${rec.recommendation}`;
            
            recommendationReason.textContent = rec.reason;
            
            // Update suggestions
            recommendationSuggestions.innerHTML = `
                <h4>Suggestions</h4>
                <ul>
                    ${rec.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                </ul>
            `;
        }
    }

    // Load recent activity
    async loadRecentActivity() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/recent-activity`);
            const data = await response.json();
            
            if (response.ok) {
                this.updateRecentActivity(data.recent_activity);
            } else {
                console.error('Failed to load recent activity:', data.error);
            }
        } catch (error) {
            console.error('Error loading recent activity:', error);
        }
    }

    updateRecentActivity(activities) {
        const activityList = document.getElementById('activity-list');
        
        if (activities.length === 0) {
            activityList.innerHTML = `
                <div class="loading-activity">
                    <i class="fas fa-info-circle"></i>
                    <p>No recent activity found</p>
                </div>
            `;
            return;
        }

        activityList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="${activity.icon}"></i>
                </div>
                <div class="activity-content">
                    <h4>${activity.type}</h4>
                    <p>${activity.value} • ${activity.time} ${activity.date}</p>
                </div>
            </div>
        `).join('');
    }

    // Utility functions
    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toLocaleString();
    }

    formatRecordType(type) {
        return type.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
    }

    getLast30Days() {
        const days = [];
        for (let i = 29; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            days.push(date.toISOString().split('T')[0]);
        }
        return days;
    }

    fillMissingDates(data, allDates, valueKey) {
        const dataMap = new Map(data.map(item => [item.date, item[valueKey]]));
        return allDates.map(date => dataMap.get(date) || 0);
    }
}

// Initialize analytics when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.healthAnalytics = new HealthAnalytics();
});

