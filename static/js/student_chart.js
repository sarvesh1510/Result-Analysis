// student_chart.js

document.addEventListener("DOMContentLoaded", function () {
    // Make sure data exists
    if (!window.chartLabels || !window.chartData) return;

    const canvas = document.getElementById("marksChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    // Create a soft gradient for all bars
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(79, 70, 229, 0.9)');   // Dark purple
    gradient.addColorStop(1, 'rgba(147, 197, 253, 0.8)'); // Light blue

    const backgroundColors = window.chartData.map(() => gradient);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: window.chartLabels,
            datasets: [
                {
                    label: "Marks (%)",
                    data: window.chartData,
                    backgroundColor: backgroundColors,
                    borderColor: "rgba(255, 255, 255, 0.8)",
                    borderWidth: 2,
                    borderRadius: 15,
                    barThickness: 40,
                    hoverBackgroundColor: gradient // same as normal, hover won't grow
                }
            ]
        },
        options: {
            responsive: true,
            hover: {
                mode: null // disables all hover effects
            },
            plugins: {
                legend: {
                    labels: {
                        font: { size: 16, weight: '700' },
                        color: '#333'
                    }
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleFont: { size: 18, weight: '700' },
                    bodyFont: { size: 16 },
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.7)',
                    borderWidth: 2,
                    padding: 12,
                    caretSize: 8,
                    callbacks: {
                        label: ctx => ctx.dataset.label + ": " + ctx.raw + "%"
                    }
                },
                datalabels: {
                    display: true,
                    color: '#fff',
                    font: { weight: 'bold', size: 14 },
                    formatter: value => value + "%"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { stepSize: 10, color: '#333', font: { size: 14, weight: '600' } },
                    grid: { color: 'rgba(0,0,0,0.1)', borderDash: [5,5] }
                },
                x: {
                    ticks: { color: '#333', font: { size: 14, weight: '600' } },
                    grid: { display: false }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutBounce'
            }
        },
        plugins: [ChartDataLabels]
    });
});