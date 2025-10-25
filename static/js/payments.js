let selectedAmount = 0;
let selectedMethod = '';

function selectAmount(amount) {
    selectedAmount = amount;
    document.getElementById('customAmount').value = amount;
    updateSummary();
    
    // Highlight selected amount
    document.querySelectorAll('.amount-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

function selectMethod(method) {
    selectedMethod = method;
    
    // Highlight selected method
    document.querySelectorAll('.method-card').forEach(card => {
        card.classList.remove('active');
    });
    event.target.classList.add('active');
}

function updateSummary() {
    const serviceFees = selectedAmount * 0.01; // 1% de frais
    const totalAmount = selectedAmount + serviceFees;
    
    document.getElementById('selectedAmount').textContent = 
        selectedAmount.toLocaleString() + ' FCFA';
    document.getElementById('serviceFees').textContent = 
        serviceFees.toLocaleString() + ' FCFA';
    document.getElementById('totalAmount').textContent = 
        totalAmount.toLocaleString() + ' FCFA';
}

function initiatePayment() {
    const customAmount = parseInt(document.getElementById('customAmount').value);
    
    if (customAmount && customAmount > 0) {
        selectedAmount = customAmount;
    }
    
    if (!selectedAmount || selectedAmount <= 0) {
        showNotification('Veuillez sélectionner un montant', 'error');
        return;
    }
    
    if (!selectedMethod) {
        showNotification('Veuillez sélectionner une méthode de paiement', 'error');
        return;
    }
    
    // Mettre à jour le modal de confirmation
    document.getElementById('confirmAmount').textContent = 
        selectedAmount.toLocaleString() + ' FCFA';
    
    const methodNames = {
        'orange': 'Orange Money',
        'free': 'Free Money', 
        'wave': 'Wave',
        'card': 'Carte Bancaire'
    };
    
    document.getElementById('confirmMethod').textContent = methodNames[selectedMethod];
    
    // Afficher le modal
    document.getElementById('paymentModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('paymentModal').style.display = 'none';
}

async function processPayment() {
    try {
        const response = await fetch('/api/initiate_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: selectedAmount,
                payment_method: selectedMethod
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Paiement initié avec succès!', 'success');
            closeModal();
            
            // Simuler la confirmation après 3 secondes
            setTimeout(async () => {
                await confirmPayment(data.payment_data.payment_id);
            }, 3000);
            
        } else {
            showNotification('Erreur lors du paiement: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Erreur de connexion', 'error');
    }
}

async function confirmPayment(paymentId) {
    try {
        const response = await fetch('/api/confirm_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                payment_id: paymentId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`Paiement confirmé! Nouveau solde: ${data.new_balance} FCFA`, 'success');
            
            // Rediriger vers le dashboard après 2 secondes
            setTimeout(() => {
                window.location.href = `/dashboard?meter_id=${meterId}`;
            }, 2000);
            
        } else {
            showNotification('Erreur de confirmation: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Erreur de connexion', 'error');
    }
}

// Gérer l'entrée de montant personnalisé
document.getElementById('customAmount').addEventListener('input', function() {
    const amount = parseInt(this.value);
    if (amount && amount > 0) {
        selectedAmount = amount;
        updateSummary();
        
        // Désélectionner les boutons de montant rapide
        document.querySelectorAll('.amount-btn').forEach(btn => {
            btn.classList.remove('active');
        });
    }
});

// Fermer le modal en cliquant en dehors
window.onclick = function(event) {
    const modal = document.getElementById('paymentModal');
    if (event.target === modal) {
        closeModal();
    }
}