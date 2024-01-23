fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        const lastSixLabels = data.labels.slice(-6);
        const lastSixTemperature = data.temperature.slice(-6);
        const lastSixHumidity = data.humidity.slice(-6);
        createChart(lastSixLabels, lastSixTemperature, lastSixHumidity);
    })
    .catch(error => console.error('Erreur lors de la récupération des données:', error));

function createChart(labels, temperature, humidity) {
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
