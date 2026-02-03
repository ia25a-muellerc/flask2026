 const pricePerItem = 30.00;
        let quantity = 1;

        function updateTotal() {
            const total = (pricePerItem * quantity).toFixed(2);
            document.getElementById('total').textContent = total + ' €';
        }

        function increaseQuantity() {
            quantity++;
            document.getElementById('quantity').textContent = quantity;
            updateTotal();
        }

        function decreaseQuantity() {
            if (quantity > 1) {
                quantity--;
                document.getElementById('quantity').textContent = quantity;
                updateTotal();
            }
        }