function initSize() {
    $('#size_error_text').text('');
    $('#size_input').val('');
    $('#cancel_size').hide();
    $('#size_select').show();
    $('#new_size').show();
    $('#size_input').hide();
    $('#size_select').attr('required', true);
    $('#size_input').attr('required', false);

    $('#new_size').click(() => {
        $('#new_size').hide();
        $('#cancel_size').show();
        $('#size_select').hide();
        $('#size_input').show();
        $('#size_input').attr('required', true);
        $('#size_select').attr('required', false);
    });

    $('#cancel_size').click(() => {
        initSize();
    });
}

// function saveSize(csrftoken, url) {
//     var size = $('#size_input').val();
//     if (size != '') {
//         $.ajax({
//             headers: {
//                 "X-CSRFTOKEN": csrftoken
//             },
//             url: url,
//             method: 'POST',
//             data: {
//                 'size': size
//             },
//             dataType: 'json',
//             success: function (response) {
//                 var size = response.size;
//                 $('#size_select').append(`<option value="${size.id}">${size.size}</option>`);
//                 initSize();
//                 $('#size_success_text').text('Size added successfully');
//                 $('#size_error_text').text('');
//             },
//             error: function (response) {
//                 var error = response["responseJSON"]["error"];
//                 $('#size_error_text').text(error);
//                 $('#size_success_text').text('');
//             }
//         });
//     }
//
// }

function initColor() {
    $('#color_error_text').text('');
    $('#color_input').val('');
    $('#cancel_color').hide();
    $('#color_input').hide();
    $('#color_select').show();
    $('#new_color').show();
    $('#color_select').attr('required', true);
    $('#color_input').attr('required', false);

    $('#new_color').click(() => {
        $('#new_color').hide();
        $('#cancel_color').show();
        $('#color_select').hide();
        $('#color_input').show();
        $('#color_input').attr('required', true);
        $('#color_select').attr('required', false);
    });

    $('#cancel_color').click(() => {
        initColor();
    });
}

function initCategory() {
    $('#category_error_text').text('');
    $('#category_input').val('');
    $('#cancel_category').hide();
    $('#category_input').hide();
    $('#category_select').show();
    $('#new_category').show();
    $('#category_input').attr('required', false);
    $('#category_select').attr('required', true);

    $('#new_category').click(() => {
        $('#new_category').hide();
        $('#cancel_category').show();
        $('#category_select').hide();
        $('#category_input').show();
        $('#category_input').attr('required', true);
        $('#category_select').attr('required', false);
    });

    $('#cancel_category').click(() => {
        initCategory();
    });
}

function initProduct() {
    $('#product_error_text').text('');
    $('#product_input').val('');
    $('#cancel_product').hide();
    $('#product_input').hide();
    $('#product_select').show();
    $('#new_product').show();
    $('#product_input').attr('required', false);
    $('#product_select').attr('required', true);
    $('#product_description').hide();
    $('#product_description').val('');

    $('#new_product').click(() => {
        $('#new_product').hide();
        $('#cancel_product').show();
        $('#product_select').hide();
        $('#product_input').show();
        $('#product_input').attr('required', true);
        $('#product_select').attr('required', false);
        $('#product_description').show();
    });

    $('#cancel_product').click(() => {
        initProduct();
    });
}

function checkFieldError() {
    if ($('#name_error').length) {
        var nameError = JSON.parse($('#name_error').text());
        $('#name_error_text').text(nameError);
        $('#id_name').addClass('error_border');

    } else {
        nameError = '';
        $('#id_name').removeClass('error_border');
    }

    if ($('#mobile_no_error').length) {
        var mobileError = JSON.parse($('#mobile_no_error').text());
        $('#mobile_no_error_text').text(mobileError);
        $('#id_mobile_no').addClass('error_border');
    } else {
        mobileError = '';
        $('#mobileError').removeClass('error_border');
    }

    if ($('#address_error').length) {
        var addressError = JSON.parse($('#address_error').text());
        $('#address_error_text').text(addressError);
        $('#id_address').addClass('error_border');
    } else {
        addressError = '';
        $('#id_address').removeClass('error_border');

    }
}

$(document).ready(function () {
    window.staticUrl = "{{ STATIC_URL }}"
    $('#product_list').DataTable({
        'lengthChange': false,
        'pageLength': 25,
        "language": {
            "search": "<span>Search</span>",
        },
    });
    $('#product_list_filter input[type=search]').addClass('form-control');
    $('#product_list_filter > label').css({'margin-right': '10px', 'text-align': 'left'});
    $('#product_list_filter > label > span').css('margin-left', '8px');

    initSize();
    initColor();
    initCategory();
    initProduct();
    checkFieldError();

});