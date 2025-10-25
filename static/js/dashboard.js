// Initialisation des graphiques
document.addEventListener('DOMContentLoaded', function() {
    if (typeof hourlyData !== 'undefined') {
        renderCharts();
        startRealTimeUpdates();
        
        // Initialiser la simulation
        setTimeout(() => {
            simulateRecharge();
        }, 1000);
    }
});

function renderCharts() {
    renderHourlyChart();
    renderDailyChart();
    renderMonthlyChart();
}

function renderHourlyChart() {
    const timestamps = hourlyData.map(data => {
        const date = new Date(data.timestamp);
        return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    });
    
    const consumption = hourlyData.map(data => data.consumption_kwh);
    
    const trace = {
        x: timestamps,
        y: consumption,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Consommation (kWh)',
        line: {
            color: '#2563eb',
            width: 3,
            shape: 'spline'
        },
        marker: {
            color: '#2563eb',
            size: 6
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(37, 99, 235, 0.1)'
    };
    
    const layout = {
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent',
        font: {
            family: 'Inter, sans-serif'
        },
        xaxis: {
            title: 'Heure de la journée',
            gridcolor: '#e2e8f0',
            tickangle: -45
        },
        yaxis: {
            title: 'Consommation (kWh)',
            gridcolor: '#e2e8f0'
        },
        margin: { t: 0 },
        hovermode: 'closest'
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot('hourlyChart', [trace], layout, config);
}

function renderDailyChart() {
    const dates = dailyData.map(data => {
        const date = new Date(data.date);
        return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' });
    });
    
    const consumption = dailyData.map(data => data.consumption_kwh);
    
    const trace = {
        x: dates,
        y: consumption,
        type: 'bar',
        name: 'Consommation Quotidienne',
        marker: {
            color: consumption.map(value => 
                value > 30 ? '#10b981' : '#f59e0b'
            )
        }
    };
    
    const layout = {
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent',
        font: {
            family: 'Inter, sans-serif'
        },
        xaxis: {
            title: 'Date',
            gridcolor: '#e2e8f0'
        },
        yaxis: {
            title: 'kWh',
            gridcolor: '#e2e8f0'
        },
        margin: { t: 0 },
        showlegend: false
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot('dailyChart', [trace], layout, config);
}

function renderMonthlyChart() {
    const months = monthlyData.map(data => {
        const [year, month] = data.month.split('-');
        return new Date(year, month - 1).toLocaleDateString('fr-FR', { month: 'short', year: '2-digit' });
    });
    
    const costs = monthlyData.map(data => data.cost);
    
    const trace = {
        x: months,
        y: costs,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Coût (FCFA)',
        line: {
            color: '#8b5cf6',
            width: 3,
            shape: 'spline'
        },
        marker: {
            color: '#8b5cf6',
            size: 6
        }
    };
    
    const layout = {
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent',
        font: {
            family: 'Inter, sans-serif'
        },
        xaxis: {
            title: 'Mois',
            gridcolor: '#e2e8f0',
            tickangle: -45
        },
        yaxis: {
            title: 'FCFA',
            gridcolor: '#e2e8f0'
        },
        margin: { t: 0 }
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot('monthlyChart', [trace], layout, config);
}

// Simulation de recharge
function setAmount(amount) {
    document.getElementById('rechargeAmount').value = amount;
    simulateRecharge();
}

function simulateRecharge() {
    const rechargeAmount = parseInt(document.getElementById('rechargeAmount').value);
    const avgDailyCost = metrics.avg_daily_cost;
    const currentBalance = metrics.current_balance;
    
    if (rechargeAmount && rechargeAmount >= 1000) {
        const totalBalance = currentBalance + rechargeAmount;
        const simulatedDays = totalBalance / avgDailyCost;
        
        document.getElementById('simulatedDays').textContent = 
            Math.round(simulatedDays) + ' jours';
        document.getElementById('totalBalance').textContent = 
            Math.round(totalBalance).toLocaleString() + ' FCFA';
        
        // Mettre à jour le graphique de projection
        updateProjectionChart(totalBalance, simulatedDays);
    }
}

function updateProjectionChart(totalBalance, simulatedDays) {
    const dailyCost = metrics.avg_daily_cost;
    const daysData = [];
    const balanceData = [];
    
    // Générer des données pour 30 jours
    for (let day = 0; day <= 30; day++) {
        daysData.push(`J${day}`);
        const balance = Math.max(0, totalBalance - (day * dailyCost));
        balanceData.push(balance);
    }
    
    const trace = {
        x: daysData,
        y: balanceData,
        type: 'scatter',
        mode: 'lines',
        name: 'Solde projeté',
        line: {
            color: '#2563eb',
            width: 3,
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(37, 99, 235, 0.1)'
    };
    
    // Ligne critique à 1000 FCFA
    const criticalLine = {
        x: daysData,
        y: Array(daysData.length).fill(1000),
        type: 'scatter',
        mode: 'lines',
        name: 'Seuil critique',
        line: {
            color: '#ef4444',
            width: 2,
            dash: 'dash'
        }
    };
    
    const layout = {
        plot_bgcolor: 'transparent',
        paper_bgcolor: 'transparent',
        font: {
            family: 'Inter, sans-serif'
        },
        xaxis: {
            title: 'Jours',
            gridcolor: '#e2e8f0',
            showgrid: true
        },
        yaxis: {
            title: 'Solde (FCFA)',
            gridcolor: '#e2e8f0'
        },
        margin: { t: 30, r: 30, b: 50, l: 50 },
        showlegend: false,
        annotations: [
            {
                x: Math.min(simulatedDays, 30),
                y: 0,
                text: `≈ ${Math.round(simulatedDays)} jours`,
                showarrow: true,
                arrowhead: 2,
                ax: 0,
                ay: -40,
                bgcolor: '#2563eb',
                bordercolor: '#2563eb',
                borderwidth: 2,
                borderpad: 4,
                font: {
                    color: 'white',
                    size: 12
                }
            }
        ]
    };
    
    Plotly.newPlot('projectionChart', [trace, criticalLine], layout, {
        responsive: true,
        displayModeBar: false
    });
}

function startRealTimeUpdates() {
    // Simuler des mises à jour en temps réel toutes les 30 secondes
    setInterval(() => {
        updateRealTimeData();
    }, 30000);
}

async function updateRealTimeData() {
    try {
        const response = await fetch('/api/update_consumption', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                meter_id: meterId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Recharger la page pour voir les nouvelles données
            location.reload();
        }
    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error);
    }
}

function updateChart(chartType) {
    switch(chartType) {
        case 'hourly':
            renderHourlyChart();
            break;
        case 'daily':
            renderDailyChart();
            break;
        case 'monthly':
            renderMonthlyChart();
            break;
    }
    
    // Afficher une notification
    showNotification('Graphique actualisé avec succès', 'success');
}

function showNotification(message, type = 'info') {
    // Créer une notification toast
    const toast = document.createElement('div');
    toast.className = `toast-notification ${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    // Ajouter l'animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
        style.remove();
    }, 3000);
}

// Mettre à jour la prédiction en temps réel
async function updateConsumptionPrediction() {
    try {
        const response = await fetch(`/api/consumption/${meterId}`);
        const data = await response.json();
        
        // Mettre à jour l'affichage si nécessaire
        const daysElement = document.querySelector('.days-count .number');
        if (daysElement) {
            // Vous pourriez mettre à jour les valeurs ici
            // en fonction des nouvelles données
        }
    } catch (error) {
        console.error('Erreur mise à jour prédiction:', error);
    }
}

// Gérer l'entrée de montant personnalisé
document.getElementById('rechargeAmount')?.addEventListener('input', function() {
    const amount = parseInt(this.value);
    if (amount && amount > 0) {
        // Désélectionner les boutons de montant rapide
        document.querySelectorAll('.quick-amount').forEach(btn => {
            btn.classList.remove('active');
        });
    }
});

// Activer/désactiver les boutons de montant rapide
document.querySelectorAll('.quick-amount').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.quick-amount').forEach(b => {
            b.classList.remove('active');
        });
        this.classList.add('active');
    });
});