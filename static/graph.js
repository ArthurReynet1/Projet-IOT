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
                    // Lien permanent vers le graphique sauvegardé
                    var permanentLink = data.permanentLink;
    
                    // URL de votre site
                    var siteURL = window.location.href;
    
                    // Lien combiné
                    var combinedLink = siteURL + permanentLink;
    
                    // Ouvrir une nouvelle fenêtre pop-up avec le lien
                    var popupWindow = window.open(combinedLink, '_blank');
    
                    // Si la pop-up est bloquée, informer l'utilisateur
                    if (!popupWindow || popupWindow.closed || typeof popupWindow.closed === 'undefined') {
                        window.alert('Veuillez autoriser les pop-ups pour copier le lien.');
                    }
    
                    // Copier le lien combiné dans le presse-papiers
                    navigator.clipboard.writeText(combinedLink)
                        .then(() => {
                            // Afficher le message en tant que fenêtre pop-up
                            window.alert('Lien copié !');
    
                            console.log('Lien combiné copié dans le presse-papiers:', combinedLink);
                        })
                        .catch(err => {
                            console.error('Erreur lors de la copie dans le presse-papiers:', err);
                        });
                } else {
                    console.error('Erreur lors de la sauvegarde du graphique.');
                }
            })
            .catch(error => console.error('Erreur lors de la communication avec le serveur:', error));
        });
    }
});