document.addEventListener('DOMContentLoaded', function () {
    const data = [
        {
            x: ['OK', 'Warning', 'Fault'],
            y: [1, 1, 1], // Match the count from assigned machines
            type: 'bar',
            marker: {
                color: ['#2ecc71', '#f1c40f', '#e74c3c']
            }
        }
    ];

    const layout = {
        title: 'Assigned Machines Status Overview',
        xaxis: {
            title: 'Status'
        },
        yaxis: {
            title: 'Number of Machines'
        }
    };

    Plotly.newPlot('assigned-machines-chart', data, layout);
});
