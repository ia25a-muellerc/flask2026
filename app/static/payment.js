// Bestelldaten aus URL-Parametern
const urlParams = new URLSearchParams(window.location.search);
const total = urlParams.get('total') || '30.00';
const quantity = urlParams.get('quantity') || '1';
const product = urlParams.get('product') || 'Desk Dunk';

document.addEventListener('DOMContentLoaded', function() {
    // Bestellzusammenfassung anzeigen
    document.getElementById('summaryProduct').textContent = decodeURIComponent(product);
    document.getElementById('summaryQuantity').textContent = quantity;
    
    const totalValue = parseFloat(total) || 30.00;
    document.getElementById('summaryTotal').textContent = ' CHF ' + totalValue.toLocaleString('de-CH', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    
    // Zahlungsmethode auswählen
    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('click', function() {
            const method = this.querySelector('.payment-btn').getAttribute('data-method');
            showPaymentForm(method);
        });
    });

    // Zahlungsformular anzeigen
    function showPaymentForm(method) {
        const titles = {
            paypal: 'PayPal Zahlung', card: 'Kreditkarte Zahlung', applepay: 'Apple Pay Zahlung',
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

    // Echtzeit-Validierung bei Eingabe
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
            errorSpan.textContent = 'This field is required';
            return false;
        }
        
        const value = field.value.trim();
        if (!value) return true;
        
        // Email prüfen
        if (field.type === 'email') {
            if (!value.includes('@') || !value.includes('.')) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Please enter a valid email address';
                return false;
            }
        }
        
        // Kartennummer prüfen
        if (field.id === 'cardNumber') {
            let numbers = value.replace(/\s/g, '');
            if (numbers.length < 13 || numbers.length > 19) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Invalid card number';
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
                errorSpan.textContent = 'CVV must have 3 digits';
                return false;
            }
        }
        
        // PLZ prüfen
        if (field.id === 'zip') {
            if (value.length < 4) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Invalid PLZ';
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
        purchaseConfirmBtn.addEventListener('click', function() {
            if (!pendingPurchase) return;
            window.location.href = '/popUpPayment';
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

        if (invalidFields.length > 0) {
            invalidFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            invalidFields[0].focus();
            return;
        }

        pendingPurchase = true;
        openPurchaseModal();
    });
});