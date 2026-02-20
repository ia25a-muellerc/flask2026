// Bestelldaten vom Server holen
document.addEventListener('DOMContentLoaded', function() {
    let selectedPaymentMethod = '';

    // Daten vom Server holen
    fetch('/api/cart')
        .then(response => response.json())
        .then(data => {
            const quantity = data.quantity || 1;
            const total = data.total || '30.00';

            // Bestellzusammenfassung anzeigen
            document.getElementById('summaryProduct').textContent = 'Desk Dunk';
            document.getElementById('summaryQuantity').textContent = quantity;
            document.getElementById('summaryTotal').textContent = ' CHF ' + parseFloat(total).toLocaleString('de-CH', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        })
        .catch(() => {
            // Fallback
            document.getElementById('summaryQuantity').textContent = '1';
            document.getElementById('summaryTotal').textContent = ' CHF 30.00';
        });

    // Zahlungsmethode auswählen
    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('click', function() {
            const method = this.querySelector('.payment-btn').getAttribute('data-method');
            showPaymentForm(method);
        });
    });

    // Zahlungsformular anzeigen
    function showPaymentForm(method) {
        selectedPaymentMethod = method;
        const titles = {
            paypal: 'PayPal Zahlung', card: 'Kreditkarten Zahlung', applepay: 'Apple Pay Zahlung',
            googlepay: 'Google Pay Zahlung', twint: 'Twint Zahlung', invoice: 'Rechnung ausstellen'
        };
        
        document.getElementById('formTitle').textContent = titles[method] || 'Zahlungsdetails';
        document.getElementById('cardSection').style.display = method === 'card' ? 'block' : 'none';
        document.getElementById('twintSection').style.display = method === 'twint' ? 'block' : 'none';
        document.getElementById('paymentFormSection').style.display = 'block';
        document.getElementById('paymentFormSection').scrollIntoView({ behavior: 'smooth' });
        
        // Required-Attribute setzen
        ['cardName', 'cardNumber', 'expiry', 'cvv'].forEach(id => {
            document.getElementById(id).required = (method === 'card');
        });
        document.getElementById('twintPhone').required = (method === 'twint');
    }

    document.querySelectorAll('.payment-form input, .payment-form select').forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => input.classList.contains('invalid') && validateField(input));
    });

    // Einzelnes Feld validieren
    function validateField(field) {
        const errorSpan = document.getElementById(field.id + 'Error');
        if (!errorSpan) return true;
        
        field.classList.remove('invalid');
        errorSpan.textContent = '';
        
        if (field.required && !field.value.trim()) {
            field.classList.add('invalid');
            errorSpan.textContent = 'Dieses Feld ist erforderlich';
            return false;
        }
        
        const value = field.value.trim();
        if (!value) return true;
        
        // Email prüfen
        if (field.type === 'email') {
            if (!value.includes('@') || !value.includes('.')) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Bitte geben Sie eine gültige E-Mail-Adresse ein';
                return false;
            }
        }
        
        // Kartennummer prüfen
        if (field.id === 'cardNumber') {
            let numbers = value.replace(/\s/g, '');
            if (numbers.length < 13 || numbers.length > 19) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Ungültige Kartennummer';
                return false;
            }
        }
        
        // Ablaufdatum prüfen
        if (field.id === 'expiry') {
            if (!/^\d{2}\/\d{2}$/.test(value)) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Format: MM/YY';
                return false;
            }
        }
        
        // CVV prüfen
        if (field.id === 'cvv') {
            if (value.length < 3) {
                field.classList.add('invalid');
                errorSpan.textContent = 'CVV muss 3 Ziffern haben';
                return false;
            }
        }
        
        // PLZ prüfen
        if (field.id === 'zip') {
            if (value.length < 4) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Ungültige PLZ';
                return false;
            }
        }
        
        return true;
    }

    // Bestellbestätigung Modal
    const purchaseModal = document.getElementById('purchaseModal');
    const purchaseCancelBtn = document.getElementById('purchaseCancelBtn');
    const purchaseConfirmBtn = document.getElementById('purchaseConfirmBtn');
    let pendingPurchase = false;

    function openPurchaseModal() {
        if (!purchaseModal) return;
        purchaseModal.classList.add('show');
        purchaseModal.setAttribute('aria-hidden', 'false');
    }

    function closePurchaseModal() {
        if (!purchaseModal) return;
        purchaseModal.classList.remove('show');
        purchaseModal.setAttribute('aria-hidden', 'true');
        pendingPurchase = false;
    }

    if (purchaseCancelBtn) {
        purchaseCancelBtn.addEventListener('click', closePurchaseModal);
    }

    if (purchaseConfirmBtn) {
        purchaseConfirmBtn.addEventListener('click', async function() {
            if (!pendingPurchase) return;

            const paymentForm = document.getElementById('selectedPaymentForm');
            const formData = new FormData(paymentForm);
            const payload = Object.fromEntries(formData.entries());
            payload.payment_method = selectedPaymentMethod;

            try {
                const response = await fetch('/api/payment/confirm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (!response.ok || !result.success) {
                    throw new Error(result.message || 'Zahlung konnte nicht gespeichert werden');
                }

                window.location.href = '/popUpPayment';
            } catch (error) {
                closePurchaseModal();
                alert(error.message || 'Fehler beim Speichern der Zahlung');
            }
        });
    }

    if (purchaseModal) {
        purchaseModal.addEventListener('click', function(event) {
            if (event.target === purchaseModal) {
                closePurchaseModal();
            }
        });
    }

    // Formular absenden
    document.getElementById('selectedPaymentForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const requiredFields = [...this.querySelectorAll('[required]')];
        const invalidFields = requiredFields.filter(field => !validateField(field));

        if (!selectedPaymentMethod) {
            alert('Bitte wählen Sie zuerst eine Zahlungsmethode aus.');
            return;
        }

        if (invalidFields.length > 0) {
            invalidFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            invalidFields[0].focus();
            return;
        }

        pendingPurchase = true;
        openPurchaseModal();
    });
});