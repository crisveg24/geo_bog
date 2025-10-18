// main.js - Funciones principales del dashboard

// Cargar datos al iniciar la página
document.addEventListener('DOMContentLoaded', function() {
    loadStatistics();
    loadGeographicData();
});

// Función para cargar estadísticas
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const result = await response.json();
        
        if (result.success) {
            displayStatistics(result.data);
            createStatisticsChart(result.data);
        } else {
            showError('statistics-summary', 'Error al cargar estadísticas');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('statistics-summary', 'Error de conexión');
    }
}

// Función para mostrar estadísticas en cards
function displayStatistics(data) {
    const container = document.getElementById('statistics-summary');
    
    if (data.length === 0) {
        container.innerHTML = '<div class="stat-card"><h3>Sin datos</h3><p>No hay estadísticas disponibles</p></div>';
        return;
    }
    
    container.innerHTML = data.map(stat => `
        <div class="stat-card">
            <h3>${stat.metric_name}</h3>
            <p><strong>Promedio:</strong> ${stat.avg_value ? Math.round(stat.avg_value).toLocaleString() : 'N/A'}</p>
            <p><strong>Mínimo:</strong> ${stat.min_value ? Math.round(stat.min_value).toLocaleString() : 'N/A'}</p>
            <p><strong>Máximo:</strong> ${stat.max_value ? Math.round(stat.max_value).toLocaleString() : 'N/A'}</p>
            <p><strong>Localidades:</strong> ${stat.count}</p>
        </div>
    `).join('');
}

// Función para crear gráfico de estadísticas con Plotly
function createStatisticsChart(data) {
    if (data.length === 0) return;
    
    const trace = {
        x: data.map(d => d.metric_name),
        y: data.map(d => d.avg_value),
        type: 'bar',
        marker: {
            color: 'rgba(102, 126, 234, 0.8)',
            line: {
                color: 'rgba(102, 126, 234, 1)',
                width: 2
            }
        }
    };
    
    const layout = {
        title: 'Valores Promedio por Métrica',
        xaxis: { title: 'Métrica' },
        yaxis: { title: 'Valor Promedio' },
        plot_bgcolor: '#f9f9f9',
        paper_bgcolor: '#f9f9f9'
    };
    
    Plotly.newPlot('statistics-chart', [trace], layout, {responsive: true});
    
    // Crear gráfico de distribución
    createDistributionChart(data);
}

// Función para crear gráfico de distribución
function createDistributionChart(data) {
    if (data.length === 0) return;
    
    const trace = {
        labels: data.map(d => d.metric_name),
        values: data.map(d => d.total_value || d.avg_value * d.count),
        type: 'pie',
        marker: {
            colors: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>Total: %{value:,.0f}<br>Porcentaje: %{percent}<extra></extra>'
    };
    
    const layout = {
        title: 'Distribución de Registros por Métrica',
        plot_bgcolor: '#f9f9f9',
        paper_bgcolor: '#f9f9f9',
        showlegend: true,
        legend: {
            orientation: 'v',
            x: 1.1,
            y: 0.5
        }
    };
    
    Plotly.newPlot('distribution-chart', [trace], layout, {responsive: true});
}

// Función para cargar datos geográficos
async function loadGeographicData() {
    try {
        const response = await fetch('/api/geographic-data');
        const result = await response.json();
        
        if (result.success) {
            displayGeographicData(result.data);
        } else {
            showError('geographic-data', 'Error al cargar datos geográficos');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('geographic-data', 'Error de conexión');
    }
}

// Función para mostrar datos geográficos en tabla
function displayGeographicData(data) {
    const container = document.getElementById('geographic-data');
    
    if (data.length === 0) {
        container.innerHTML = '<p>No hay datos geográficos disponibles</p>';
        return;
    }
    
    const tableHTML = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Localidad</th>
                    <th>Latitud</th>
                    <th>Longitud</th>
                    <th>Información</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(item => `
                    <tr>
                        <td><strong>${item.name || 'N/A'}</strong></td>
                        <td>${item.latitude ? item.latitude.toFixed(4) : 'N/A'}</td>
                        <td>${item.longitude ? item.longitude.toFixed(4) : 'N/A'}</td>
                        <td>${item.description || 'N/A'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = tableHTML;
}

// Función para mostrar errores
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="error">${message}</div>`;
}
