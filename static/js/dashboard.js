document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('dashboard-container');
    if (!container) return;

    try {
        // Parse the data from data attributes
        const data = {
            users: parseInt(container.dataset.users) || 0,
            devices: parseInt(container.dataset.devices) || 0,
            success: parseInt(container.dataset.success) || 0,
            failed: parseInt(container.dataset.failed) || 0,
            events: JSON.parse(container.dataset.events || '[]')
        };

        console.log('Dashboard data:', data); // Debug log

        // Initialize Highcharts Dashboard
        Highcharts.setOptions({
            chart: {
                style: {
                    fontFamily: 'Roboto, sans-serif'
                }
            }
        });

        // Create the dashboard
        const board = Dashboards.board(container, {
            gui: {
                layouts: [{
                    rows: [{
                        cells: [{
                            id: 'kpi-users'
                        }, {
                            id: 'kpi-devices'
                        }]
                    }, {
                        cells: [{
                            id: 'success-chart'
                        }, {
                            id: 'failed-chart'
                        }]
                    }, {
                        cells: [{
                            id: 'events-table'
                        }]
                    }]
                }]
            },
            components: [{
                cell: 'kpi-users',
                type: 'KPI',
                title: 'Total Users',
                value: data.users
            }, {
                cell: 'kpi-devices',
                type: 'KPI',
                title: 'Total Devices',
                value: data.devices
            }, {
                cell: 'success-chart',
                type: 'Highcharts',
                chartOptions: {
                    chart: { 
                        type: 'column',
                        height: '250px'
                    },
                    title: { text: 'Success Events' },
                    series: [{
                        name: 'Success',
                        data: [data.success],
                        color: '#28a745'
                    }]
                }
            }, {
                cell: 'failed-chart',
                type: 'Highcharts',
                chartOptions: {
                    chart: { 
                        type: 'column',
                        height: '250px'
                    },
                    title: { text: 'Failed Events' },
                    series: [{
                        name: 'Failed',
                        data: [data.failed],
                        color: '#dc3545'
                    }]
                }
            }, {
                cell: 'events-table',
                type: 'Highcharts',
                chartOptions: {
                    chart: {
                        type: 'table',
                        height: '250px'
                    },
                    title: { text: 'Event History' },
                    series: [{
                        name: 'Events',
                        data: data.events.map(event => [
                            event.event_time,
                            event.device_name,
                            event.username,
                            event.status
                        ])
                    }],
                    xAxis: {
                        categories: ['Event Time', 'Device', 'User', 'Status']
                    }
                }
            }]
        });

    } catch (error) {
        console.error('Error initializing dashboard:', error);
        console.error('Data attributes:', {
            users: container.dataset.users,
            devices: container.dataset.devices,
            success: container.dataset.success,
            failed: container.dataset.failed,
            events: container.dataset.events
        });
        container.innerHTML = '<div class="alert alert-danger">Error loading dashboard. Check console for details.</div>';
    }
});
