"use strict";

const addToCartButton = $('button.add-to-cart');

// When user clicks Add to Cart, item is sent to server to store in cart.
// Add to Cart button disappears and Remove from Cart button appears.
addToCartButton.on('click', (event) => {
    const imageID = $(event.target).parent().parent().attr('data-image-id')
    const imageName = $(event.target).parent().siblings('.store-image-name').html();
    const imagePrice = $(event.target).parent().siblings('.store-image-price').html();
    const data = {
        'id': imageID,
        'name': imageName,
        'price': imagePrice
    }
    addToCart(data);
    // Add to Cart button is hidden because item can't be added more than once
    $(event.target).toggle();
    // Remove from Cart button appears
    $(event.target).parent().children('button.remove-from-cart').toggle();
})

function addToCart(data) {
    $.post('/api/add-to-cart', data, (response) => {
        const cartSize = response.cart_size;
        updateCartCount(cartSize);
    })
}

function updateCartCount(num) {
    $('#view-cart-link').html(`View Cart (${num})`);
}