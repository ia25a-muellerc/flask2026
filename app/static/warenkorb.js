// Einfacher Warenkorb mit Session-Cookies

const pricePerItem = 30.00;
let noticeTimer = null;

function showNotification(message) {
    const notice = document.getElementById('cart-notice');
    if (!notice) return;

    notice.textContent = message;
    notice.classList.add('show');

    if (noticeTimer) {
        clearTimeout(noticeTimer);
    }

    noticeTimer = setTimeout(() => {
        notice.classList.remove('show');
    }, 2200);
}

function consumePendingNotice() {
    const notice = localStorage.getItem('cart_notice');
    if (!notice) return;

    if (notice === 'added') {
        showNotification('Added to cart');
    } else if (notice === 'removed') {
        showNotification('Removed from cart');
    }

    localStorage.removeItem('cart_notice');
}

function getCartItems() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

function saveCartItems(items) {
    localStorage.setItem('cart', JSON.stringify(items));
}

function addToCart() {
    const items = getCartItems();
    items.push({
        name: 'Desk Dunk',
        price: pricePerItem
    });
    saveCartItems(items);
    showNotification('Added to cart');
    renderCart();
}

function increaseQuantity() {
    const items = getCartItems();
    if (items.length > 0) {
        items.push({
            name: 'Desk Dunk',
            price: pricePerItem
        });
        saveCartItems(items);
        showNotification('Added to cart');
        renderCart();
    }
}

function decreaseQuantity() {
    const items = getCartItems();
    if (items.length > 0) {
        items.pop();
        saveCartItems(items);
        showNotification('Removed from cart');
        renderCart();
    }
}

function renderCart() {
    console.log('renderCart aufgerufen');
    const items = getCartItems();
    console.log('Items im Warenkorb:', items);

    const cartItemsDiv = document.getElementById('cart-items');
    const emptyMessage = document.getElementById('empty-message');
    const totalSection = document.getElementById('total-section');
    const checkoutBtn = document.getElementById('checkout-btn');

    if (!cartItemsDiv || !emptyMessage || !totalSection || !checkoutBtn) {
        console.error('Ein oder mehrere DOM-Elemente nicht gefunden');
        return;
    }

    cartItemsDiv.innerHTML = '';

    if (items.length === 0) {
        // Warenkorb ist leer
        emptyMessage.style.display = 'block';
        totalSection.style.display = 'none';
        checkoutBtn.style.display = 'none';
        console.log('Warenkorb ist leer');
    } else {
        emptyMessage.style.display = 'none';
        totalSection.style.display = 'flex';
        checkoutBtn.style.display = 'block';
        console.log('Warenkorb hat', items.length, 'Produkte');

        // Nur ein Item anzeigen mit Menge
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';
        itemDiv.innerHTML = `
            <div class="item-info">
                <span class="item-name">Desk Dunk</span>
                <span class="item-price">CHF ${pricePerItem.toFixed(2)}</span>
            </div>
            <div class="quantity-control">
                <button class="qty-btn" onclick="decreaseQuantity()">-</button>
                <span class="quantity" id="quantity">${items.length}</span>
                <button class="qty-btn" onclick="increaseQuantity()">+</button>
            </div>
        `;
        cartItemsDiv.appendChild(itemDiv);

        // Total berechnen
        const total = items.reduce((sum, item) => sum + item.price, 0);
        document.getElementById('total').textContent = ` CHF ${total.toFixed(2)}`;
    }
}

// Checkout-Button und initiales Rendern
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded Event ausgelöst');
    renderCart();
    consumePendingNotice();

    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            const items = getCartItems();
            const total = items.reduce((sum, item) => sum + item.price, 0).toFixed(2);
            const quantity = items.length;

            // Zur Zahlungsseite mit Betrag und Menge umleiten
            window.location.href = `/payment?total=${total}&quantity=${quantity}&product=Desk%20Dunk`;
        });
    }
});

// Auch renderCart aufrufen wenn Script lädt (Fallback falls DOMContentLoaded zu früh ist)
if (document.readyState === 'loading') {
    // DOM wird noch geladen
    document.addEventListener('DOMContentLoaded', renderCart);
} else {
    // DOM ist bereits geladen
    renderCart();
    consumePendingNotice();
}

// Global addToCart für externe Buttons verfügbar machen
window.addToCart = addToCart;
