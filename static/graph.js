fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        const selectedData = data.data.slice(-6);

        createChart(selectedData);
    })
    .catch(error => console.error('Erreur lors de la récupération des données:', error));

function createChart(data) {

    var labels = data.map(entry => entry[1]);
    var temperature = data.map(entry => entry[2]);
    var humidity = data.map(entry => entry[3]);

    // Map the data array to an array of objects with x and y properties
    var chartData = data.map(entry => ({ x: entry[3], y: entry[2] }));

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'scatter', // Use a scatter plot to display the relationship between temperature and humidity
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Température par rapport à l\'humidité',
                    data: chartData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    pointRadius: 5,
                }
            ]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Humidité (%)'
                    },
                    min: 0,
                    max: 100
                },
                y: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Température (°C)'
                    },
                    min: -20,
                    max: 50
                }
            }
        }
    });
}
