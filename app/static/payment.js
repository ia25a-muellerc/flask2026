// Bestelldaten aus URL-Parametern
const urlParams = new URLSearchParams(window.location.search);
const total = urlParams.get('total') || '30.00';
const quantity = urlParams.get('quantity') || '1';
const product = urlParams.get('product') || 'Desk Dunk';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('summaryProduct').textContent = decodeURIComponent(product);
    document.getElementById('summaryQuantity').textContent = quantity;
    document.getElementById('summaryTotal').textContent = ' CHF ' + parseFloat(total).toLocaleString('de-CH', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    
    // Payment-Container Klicks (ganzer Container klickbar)
    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('click', function() {
            const button = this.querySelector('.payment-btn');
            const method = button.getAttribute('data-method');
            const formSection = document.getElementById('paymentFormSection');
            const cardSection = document.getElementById('cardSection');
            const twintSection = document.getElementById('twintSection');
            const formTitle = document.getElementById('formTitle');
            
            const titles = {
                paypal: 'PayPal Zahlung',
                card: 'Kreditkarte Zahlung',
                applepay: 'Apple Pay Zahlung',
                googlepay: 'Google Pay Zahlung',
                twint: 'Twint Zahlung',
                invoice: 'Rechnung ausstellen'
            };
            
            formTitle.textContent = titles[method] || 'Zahlungsdetails';
            
            // Spezifische Formularteile anzeigen/verstecken
            cardSection.style.display = method === 'card' ? 'block' : 'none';
            twintSection.style.display = method === 'twint' ? 'block' : 'none';
            
            formSection.style.display = 'block';
            formSection.scrollIntoView({ behavior: 'smooth' });
            
            // Update required fields based on payment method
            updateRequiredFields(method);
        });
    });

    // Update required fields based on payment method
    function updateRequiredFields(method) {
        const cardFields = ['cardName', 'cardNumber', 'expiry', 'cvv'];
        const twintFields = ['twintPhone'];
        
        // Remove required from all conditional fields
        cardFields.forEach(id => {
            const field = document.getElementById(id);
            field.removeAttribute('required');
        });
        twintFields.forEach(id => {
            const field = document.getElementById(id);
            field.removeAttribute('required');
        });
        
        // Add required based on method
        if (method === 'card') {
            cardFields.forEach(id => {
                document.getElementById(id).setAttribute('required', 'required');
            });
        } else if (method === 'twint') {
            twintFields.forEach(id => {
                document.getElementById(id).setAttribute('required', 'required');
            });
        }
    }

    // Real-time validation
    const inputs = document.querySelectorAll('.payment-form input, .payment-form select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                validateField(this);
            }
        });
    });

    function validateField(field) {
        const errorSpan = document.getElementById(field.id + 'Error');
        if (!errorSpan) return;
        
        field.classList.remove('invalid');
        errorSpan.textContent = '';
        
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('invalid');
            errorSpan.textContent = 'Dieses Feld ist erforderlich';
            return false;
        }
        
        // Email validation
        if (field.type === 'email' && field.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Bitte geben Sie eine gültige E-Mail-Adresse ein';
                return false;
            }
        }
        
        // Card number validation
        if (field.id === 'cardNumber' && field.value.trim()) {
            const cleaned = field.value.replace(/\s/g, '');
            if (cleaned.length < 13 || cleaned.length > 19) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Ungültige Kartennummer';
                return false;
            }
        }
        
        // Expiry date validation
        if (field.id === 'expiry' && field.value.trim()) {
            const expiryRegex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
            if (!expiryRegex.test(field.value)) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Format: MM/YY';
                return false;
            }
        }
        
        // CVV validation
        if (field.id === 'cvv' && field.value.trim()) {
            if (field.value.length < 3) {
                field.classList.add('invalid');
                errorSpan.textContent = 'CVV muss 3 Ziffern haben';
                return false;
            }
        }
        
        // ZIP code validation
        if (field.id === 'zip' && field.value.trim()) {
            if (field.value.length < 4) {
                field.classList.add('invalid');
                errorSpan.textContent = 'Ungültige PLZ';
                return false;
            }
        }
        
        return true;
    }

    // Form submission
    const paymentForm = document.getElementById('selectedPaymentForm');
    paymentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        let firstInvalidField = null;
        
        // Validate all required fields
        const requiredFields = this.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!validateField(field)) {
                isValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });
        
        if (!isValid && firstInvalidField) {
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalidField.focus();
            return false;
        }
        
        // If validation passes, submit the form
        alert('Zahlung erfolgreich! Vielen Dank für Ihre Bestellung.');
        window.location.href = '/';
    });
});