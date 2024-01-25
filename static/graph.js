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
        var shareButton = document.getElementById('shareButton');
        var canvas = document.getElementById('myChart');
    
        // Désactivez le bouton pendant le traitement
        shareButton.disabled = true;
    
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
    
                    // Copier le lien combiné dans le presse-papiers
                    navigator.clipboard.writeText(combinedLink)
                        .then(() => {
                            // Changement de style du bouton
                            shareButton.style.backgroundColor = '#d3d3d3'; // Gris clair
                            shareButton.style.color = '#333'; // Gris foncé
                            shareButton.innerText = 'Lien copié';
    
                            console.log('Lien copié dans le presse-papiers:', combinedLink);
    
                            // Réactivez le bouton après 3 secondes (3000 millisecondes)
                            setTimeout(function() {
                                shareButton.disabled = false;
                                shareButton.style.backgroundColor = ''; // Réinitialisez la couleur de fond
                                shareButton.style.color = ''; // Réinitialisez la couleur du texte
                                shareButton.innerText = 'Partager le graphique'; // Réinitialisez le texte du bouton
                            }, 2000);
                        })
                        .catch(err => {
                            console.error('Erreur lors de la copie dans le presse-papiers:', err);
                            // Réactivez le bouton immédiatement en cas d'erreur
                            shareButton.disabled = false;
                        });
                } else {
                    console.error('Erreur lors de la sauvegarde du graphique.');
                    // Réactivez le bouton immédiatement en cas d'erreur
                    shareButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Erreur lors de la communication avec le serveur:', error);
                // Réactivez le bouton immédiatement en cas d'erreur
                shareButton.disabled = false;
            });
        });
    }
    
});