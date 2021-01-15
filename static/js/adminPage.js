"use strict";

const editField = $('.edit-inventory');
const editOptions = $('.edit-options');

// Save button appears whenever user clicks on a field to edit
editField.on('click', (event) => {
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
    $(event.target).hide();
} )

function editListing(data) {
    $.post('/api/update-image', data, (response) => {
        const updateRow = $(`tr[data-image-id=${response.id}]`);
        updateRow.children('td.image-name').attr('value', response.name);
        updateRow.children('td.image-price').attr('value', response.price);
    });
}

