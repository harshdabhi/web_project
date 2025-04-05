google.charts.load('current', { packages: ['corechart'] });
google.charts.setOnLoadCallback(drawAllMachinesChart);

function drawAllMachinesChart() {
    const data = google.visualization.arrayToDataTable([
        ['Status', 'Number of Machines'],
        ['OK', 1],
        ['Warning', 1],
        ['Fault', 1]
    ]);

    const options = {
        title: 'All Machines Status Distribution',
        is3D: true,
        colors: ['#2ecc71', '#f1c40f', '#e74c3c']
    };

    const chart = new google.visualization.PieChart(document.getElementById('all-machines-piechart'));
    chart.draw(data, options);
}
