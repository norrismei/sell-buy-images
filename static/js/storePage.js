"use strict";

const addToCartButton = $('button.add-to-cart');
const removeFromCartButton = $('button.remove-from-cart');

// When user clicks Add to Cart, item is sent to server to store in cart.
// Add to Cart button disappears and Remove from Cart button appears.
addToCartButton.on('click', (event) => {
    const data = getImageData(event);
    addToCart(data);
    // Add to Cart button is hidden because item can't be added more than once
    $(event.target).toggle();
    // Remove from Cart button appears
    $(event.target).parent().children('button.remove-from-cart').toggle();
})

// When user clicks on Remove from Cart is sent to server to delete from cart.
// Remove from Cart button disappears and Add to Cart button appears.
removeFromCartButton.on('click', (event) => {
    const imageID = $(event.target).parent().parent().attr('data-image-id')
    removeFromCart(imageID);
    $(event.target).toggle();
    $(event.target).parent().children('button.add-to-cart').toggle();
})

function getImageData(event) {
    const imageID = $(event.target).parent().parent().attr('data-image-id')
    const imageName = $(event.target).parent().siblings('.store-image-name').html();
    const imagePrice = $(event.target).parent().siblings('.store-image-price').html();
    const imageURL = $(event.target).parent().siblings('.store-image-url').children().attr('src');
    const data = {
        'id': imageID,
        'name': imageName,
        'price': imagePrice,
        'url': imageURL
    }
    return data;
}

function addToCart(data) {
    $.post('/api/add-to-cart', data, (response) => {
        const cartSize = response.cart_size;
        updateCartCount(cartSize);
    })
}

function removeFromCart(imageID) {
    $.post('/api/remove-from-cart', {"image_id": imageID}, (response) => {
        const cartSize = response.cart_size;
        updateCartCount(cartSize);
    })
}

function updateCartCount(num) {
    $('#view-cart-link').html(`View Cart (${num})`);
}