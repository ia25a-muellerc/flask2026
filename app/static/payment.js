// Bestelldaten aus URL-Parametern
const urlParams = new URLSearchParams(window.location.search);
const total = urlParams.get('total') || '30.00';
const quantity = urlParams.get('quantity') || '1';
const product = urlParams.get('product') || 'Desk Dunk';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('summaryProduct').textContent = decodeURIComponent(product);
    document.getElementById('summaryQuantity').textContent = quantity;
    document.getElementById('summaryTotal').textContent = '€' + parseFloat(total).toLocaleString('de-CH', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    
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
        });
    });
});