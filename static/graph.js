fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        const selectedData = data.data.slice(-6);

        createChart(selectedData);
    })
    .catch(error => console.error('Erreur lors de la récupération des données:', error));

function createChart(data) {

    var labels = data.map(entry => entry.id);
    var temperature = data.map(entry => entry.temperature);
    var humidity = data.map(entry => entry.humidity);

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Température (°C)',
                    data: temperature,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Humidité (%)',
                    data: humidity,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
