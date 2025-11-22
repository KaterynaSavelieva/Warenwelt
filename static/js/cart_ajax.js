async function addToCart(productId) {
    try {
        let response = await fetch(`/add-to-cart/${productId}`, {
            method: "POST",
        });

        if (!response.ok) {
            console.log("Error adding to cart");
            return;
        }

        // optionally update cart total on page
        const data = await response.json();
        if (data.cart_total !== undefined) {
            const el = document.getElementById("cart-total");
            if (el) el.textContent = data.cart_total.toFixed(2) + " €";
        }

    } catch (err) {
        console.log("AJAX error:", err);
    }
}
