async function updateSetting(key, value) {
    try {
        const response = await fetch('/api/update_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                [key]: value
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Paramètre mis à jour', 'success');
            
            // Appliquer les changements immédiatement
            if (key === 'theme') {
                applyTheme(value);
            }
        }
    } catch (error) {
        showNotification('Erreur de mise à jour', 'error');
    }
}

function changeTheme(theme) {
    updateSetting('theme', theme);
}

function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
}

function saveAllSettings() {
    const language = document.getElementById('languageSelect').value;
    const currency = document.getElementById('currencySelect').value;
    const notifications = document.getElementById('notificationsToggle').checked;
    
    updateSetting('language', language);
    updateSetting('currency', currency);
    updateSetting('notifications', notifications);
    
    showNotification('Tous les paramètres ont été sauvegardés', 'success');
}

function resetSettings() {
    if (confirm('Êtes-vous sûr de vouloir réinitialiser tous les paramètres ?')) {
        // Réinitialiser aux valeurs par défaut
        updateSetting('theme', 'light');
        updateSetting('language', 'fr');
        updateSetting('currency', 'XOF');
        updateSetting('notifications', true);
        
        // Recharger la page après un délai
        setTimeout(() => {
            location.reload();
        }, 1000);
    }
}

// Appliquer le thème au chargement
document.addEventListener('DOMContentLoaded', function() {
    if (typeof theme !== 'undefined') {
        applyTheme(theme);
    }
});