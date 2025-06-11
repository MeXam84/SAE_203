<?php
try {
    $db = new PDO('sqlite:serignan.db');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $db->query("SELECT temp, humidite, vent, date_heure FROM meteo ORDER BY date_heure ASC");
    $temperatures = [];
    $humidites = [];
    $vent = [];
    $dates = [];

    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $temperatures[] = $row['temp'];
        $humidites[] = $row['humidite'];
        $vent[] = $row['vent'];
        $dates[] = date('d/m H:i', strtotime($row['date_heure']));
    }

    $temp_json = json_encode($temperatures);
    $humid_json = json_encode($humidites);
    $wind_json = json_encode($vent);
    $dates_json = json_encode($dates);

} catch (Exception $e) {
    die('Erreur : ' . $e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Météo Sérignan-du-Comtat</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Évolution de la météo à Sérignan-du-Comtat</h1>
    <canvas id="weatherChart" width="600" height="300"></canvas>
    <button id="downloadBtn">Télécharger le graphique en image</button>

    <script>
        const labels = <?php echo $dates_json; ?>;
        const temperatureData = <?php echo $temp_json; ?>;
        const humidityData = <?php echo $humid_json; ?>;
        const windData = <?php echo $wind_json; ?>;

        const ctx = document.getElementById('weatherChart').getContext('2d');
        const weatherChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Température (°C)',
                        data: temperatureData,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        yAxisID: 'yTemp',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Humidité (%)',
                        data: humidityData,
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        yAxisID: 'yHumid',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Vent (m/s)',
                        data: windData,
                        borderColor: 'rgb(59, 59, 59)',
                        backgroundColor: 'rgba(59, 59, 59, 0.1)',
                        yAxisID: 'yWind',
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.formattedValue;
                                return `${label} : ${value}`;
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    yTemp: {
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Température (°C)'
                        }
                    },
                    yHumid: {
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Humidité (%)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    yWind: {
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Vent (m/s)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date et Heure'
                        }
                    }
                }
            }
        });

        document.getElementById('downloadBtn').addEventListener('click', function () {
            const link = document.createElement('a');
            link.download = 'meteo_serignan.png';
            link.href = weatherChart.toBase64Image();
            link.click();
        });
    </script>
</body>
</html>
