document.addEventListener('DOMContentLoaded', function() {
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
                },
                responsive: true,
                maintainAspectRatio: false,
            }

        });
    }

    document.getElementById('shareButton').addEventListener('click', function() {
        shareChart();
    });

    function shareChart() {
        var canvas = document.getElementById('myChart');
        canvas.toBlob(function(blob) {
            var formData = new FormData();
            formData.append('graphImage', blob);
    
            fetch('/api/save-graph', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Rediriger vers la nouvelle page avec le graphique
                    window.location.href = "/graph/graph.png";
                } else {
                    console.error('Erreur lors de la sauvegarde du graphique.');
                }
            })
            .catch(error => console.error('Erreur lors de la communication avec le serveur:', error));
        });
    }
});