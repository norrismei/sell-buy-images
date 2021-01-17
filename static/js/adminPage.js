"use strict";

const editField = $('.edit-inventory');
const editOptions = $('.edit-options');

// Save button appears whenever user clicks on a field to edit
editField.on('click select', (event) => {
    $(event.target).parent().siblings('.edit-options').children('.save').show();
})

// When user hits save, sends image values to update database
editOptions.on('click', 'button.save', (event) => {
    const imageID = $(event.target).parent().parent().attr('data-image-id');
    const imageName = $(event.target).parent().siblings('.image-name').children().val();
    const imagePrice = $(event.target).parent().siblings('.image-price').children().val();
    const data = {
        'id': imageID,
        'name': imageName,
        'price': imagePrice
    };
    editListing(data);
    // Once listing is updated, save button is hidden until triggered again
    $(event.target).hide();
} )

function editListing(data) {
    $.post('/api/update-image', data, (response) => {
        const updateRow = $(`tr[data-image-id=${response.id}]`);
        updateRow.children('td.image-name').children().attr('value', response.name);
        updateRow.children('td.image-price').html(`<input type="text" class="edit-inventory" value="${response.price.toFixed(2)}">`);
    });
}

// When user hits remove, sends image ID to update image status in database to REMOVED
editOptions.on('click', 'button.remove', (event) => {
    const imageID = $(event.target).parent().parent().attr('data-image-id');
    removeListing(imageID);
})

function removeListing(id) {
    $.post('/api/hide-image', {"id": id}, (response) => {
        const removeRow = $(`tr[data-image-id=${response.id}]`);
        removeRow.remove();
    })
}
