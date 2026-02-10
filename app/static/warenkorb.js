// Einfacher Warenkorb mit Session-Cookies

const PRICE = 30.00;

async function increaseQuantity() {
    const quantity = parseInt(document.getElementById('quantity').textContent) + 1;
    await updateCart(quantity);
}

async function decreaseQuantity() {
    const quantity = parseInt(document.getElementById('quantity').textContent);
    if (quantity > 1) {
        await updateCart(quantity - 1);
    }
}

async function updateCart(quantity) {
    const response = await fetch('/api/cart/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity })
    });
    
    const data = await response.json();
    document.getElementById('quantity').textContent = data.quantity;
    document.getElementById('total').textContent = ' CHF ' + data.total;
}

async function loadCart() {
    const response = await fetch('/api/cart');
    if (!response.ok) {
        return;
    }
    const data = await response.json();
    document.getElementById('quantity').textContent = data.quantity;
    document.getElementById('total').textContent = ' CHF ' + data.total;
}

// Checkout
document.addEventListener('DOMContentLoaded', function() {
    loadCart();
    document.querySelector('.checkout').addEventListener('click', function() {
        const quantity = document.getElementById('quantity').textContent;
        const total = document.getElementById('total').textContent.replace(' CHF ', '');
        window.location.href = `/payment?total=${total}&quantity=${quantity}&product=Desk%20Dunk`;
    });
});


