document.addEventListener('DOMContentLoaded', () => {
    // === GRÁFICO DE CRÉDITOS ===
    if (typeof dadosGrafico !== 'undefined') {
        const ctx = document.getElementById('graficoCreditos');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dadosGrafico.labels,
                datasets: [{
                    label: 'Créditos Recebidos (kWh)',
                    data: dadosGrafico.valores,
                    borderWidth: 1,
                    backgroundColor: 'rgba(25, 135, 84, 0.6)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'kWh' }
                    },
                    x: {
                        title: { display: true, text: 'Data' }
                    }
                }
            }
        });
    }

    // === GERAR PDF ===
    document.getElementById('btnPDF')?.addEventListener('click', async () => {
        const element = document.querySelector('.report-container');
        const opt = {
            margin: 0.5,
            filename: 'relatorio_beneficiario.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
        };

        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js";
        script.onload = () => html2pdf().from(element).set(opt).save();
        document.body.appendChild(script);
    });
});
