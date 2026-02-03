// Warenkorb Funktionen

const pricePerItem = 30.00;

function increaseQuantity() {
    const quantityElement = document.getElementById('quantity');
    let quantity = parseInt(quantityElement.textContent);
    quantity++;
    quantityElement.textContent = quantity;
    updateTotal();
}

function decreaseQuantity() {
    const quantityElement = document.getElementById('quantity');
    let quantity = parseInt(quantityElement.textContent);
    if (quantity > 1) {
        quantity--;
        quantityElement.textContent = quantity;
        updateTotal();
    }
}

function updateTotal() {
    const quantityElement = document.getElementById('quantity');
    const quantity = parseInt(quantityElement.textContent);
    const total = (pricePerItem * quantity).toFixed(2);
    document.getElementById('total').textContent = total + ' €';
}

// Checkout-Button
document.addEventListener('DOMContentLoaded', function() {
    const checkoutBtn = document.querySelector('.checkout');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            const quantity = parseInt(document.getElementById('quantity').textContent);
            const totalText = document.getElementById('total').textContent;
            const total = totalText.replace(' €', '').replace(',', '.');
            
            // Zur Zahlungsseite mit Betrag und Menge umleiten
            window.location.href = `/payment?total=${total}&quantity=${quantity}&product=Desk%20Dunk`;
        });
    }
});
