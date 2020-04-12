var grandTotal = 0.000;

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

function calculateGrandTotal() {
    var grandTotal = 0;
    var nancount = 0;
    var rowCount = 0;
    $(".sub_total").each(function () {
        var tempSubTotal = parseFloat($(this).text());
        if (!isNaN(tempSubTotal)) {
            grandTotal += tempSubTotal;
        } else {
            nancount++;
        }
        rowCount++;
    });
    if (rowCount == 0) {
        grandTotal = NaN;
    }
    return {grandTotal, nancount};
}

function disableOrEnablePaidetotalField() {
    var grandTotal = calculateGrandTotal();
    if (!isNaN(grandTotal.grandTotal)) {
        $('#grand_total').text(grandTotal.grandTotal.toFixed(3));
        if (grandTotal.nancount > 0) {
            $('#paid_total_field').attr('disabled', true);
            $('#paid_total_field').val('')
            $('#total_due').text('----');
        } else {
            $('#paid_total_field').removeAttr('disabled');
        }
        $('#paid_total_field').attr('max', grandTotal.grandTotal.toFixed(3));
    } else {
        $('#grand_total').text('----');
        $('#paid_total_field').attr('disabled', true);
        $('#paid_total_field').val('');
        $('#total_due').text('----');
    }
}

function onChangeQuantity(quantityField) {
    var $row = quantityField.closest("tr");
    var $tds = $row.find("td");
    var price = parseFloat($($tds[6]).text()).toFixed(3);
    var quantity = parseInt(quantityField.val());
    var discount = parseInt(quantityField.data('discount'));
    var minPurchase = parseInt(quantityField.data('min-purchase'));
    var subTotal = 0.000;
    var stockTotal = parseInt(quantityField.data('stock-total'));
    if (!isNaN(quantity)) {
        if (quantity >= 0 && quantity <= stockTotal) {
            quantityField.val(quantity);
            quantityField.removeClass('error_border');
        } else if (quantity > stockTotal) {
            quantity = stockTotal;
            quantityField.val(stockTotal);
        } else {
            quantity = 1;
            quantityField.val(1);
        }

        if (quantity >= minPurchase && minPurchase != 0 && discount != 0) {
            subTotal = ((quantity * price) * (1.00 - (discount / 100.000))).toFixed(3);
            $($tds[7]).find('input').attr('value', discount);
            $($tds[7]).find('span').text(discount);
        } else {
            subTotal = (quantity * price).toFixed(3);
        }
        $($tds[9]).text(subTotal);
    } else {
        quantityField.addClass('error_border');
        $($tds[9]).text('----');
    }
    disableOrEnablePaidetotalField();
}

function addInvoiceItem(productVariant, currentObject) {
    $(currentObject).addClass('avoid-clicks');
    let currId = $(currentObject).attr('id');
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#empty_form_product :input').attr('value', productVariant.variant_id);
    $('#empty_form_price_per_product :input').attr('value', productVariant.price);
    $('#empty_form_discount_percent :input').attr('value', productVariant.discount_percent);
    $('#empty_form_quantity :input').attr({
        'onchange': 'onChangeQuantity($(this))',
        'onkeyup': 'onChangeQuantity($(this))',
        'data-discount': productVariant.discount_percent,
        'data-min-purchase': productVariant.discount_min_purchase,
        'data-stock-total': productVariant.stock_total,
        'max': productVariant.stock_total
    });
    var newInvoiceItem = '<tr class="nopadding invoice_row" style="cursor: pointer" id="invoice-item-' + productVariant.variant_id + '"  data-parent-id=' + currId + ' oncontextmenu="invoiceContextMenu()">' +
        '<td>' + $('#empty_form_product').html() + '<span>' + productVariant.variant_id + '</span>' + '</td>'
        + '<td>' + productVariant.product_name + '</td>'
        + '<td>' + productVariant.category + '</td>'
        + '<td>' + productVariant.gsm + '</td>'
        + '<td>' + productVariant.size + '</td>'
        + '<td>' + productVariant.color + '</td>'
        + '<td>' + $('#empty_form_price_per_product').html() + '<span>' + productVariant.price + '</span>' + '</td>'
        + '<td>' + $('#empty_form_discount_percent').html() + '<span>' + 0 + '</span>' + '</td>'
        + '<td style="width: 10%;">' + $('#empty_form_quantity').html() + '</td>'
        + '<td class="text-right sub_total">----</td>'
        + '</tr>';
    newInvoiceItem = newInvoiceItem.replace(/__prefix__/g, form_idx);
    $('#invoice_item').append(newInvoiceItem);
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);

    invoiceContextMenu();
    disableOrEnablePaidetotalField();
}

function checkTableEmpty() {
    $(document).bind('DOMSubtreeModified', '#invoice_item', function () {
        if ($('#invoice_item').children().length <= 1) {
            $('#invoice_empty_msg').css('display', 'contents');
        } else {
            $('#invoice_empty_msg').css('display', 'none');
        }
    })
}

function paidTotalInputFieldChange() {
    $('#paid_total_field').bind('change keyup', function () {
        var paidTotal = parseFloat($('#paid_total_field').val());
        var grandTotal = calculateGrandTotal();
        if (!isNaN(paidTotal) && !isNaN(grandTotal.grandTotal)) {
            var due = grandTotal.grandTotal - paidTotal;
            if (due >= 0 && due <= grandTotal.grandTotal) {
                $('#total_due').text(due.toFixed(3));
                $('#paid_total_field').removeClass('error_border');
            } else if (due > grandTotal.grandTotal) {
                $('#paid_total_field').val(0);
                $('#total_due').text(grandTotal.grandTotal.toFixed(3));
            } else {
                $('#paid_total_field').val(grandTotal.grandTotal.toFixed(3));
                $('#total_due').text('0.000');
            }
        } else {
            $('#total_due').text('----');
            $('#paid_total_field').addClass('error_border');
        }
    });
}

function invoiceContextMenu() {
    $('.invoice_row').on('contextmenu', function (e) {
        e.preventDefault();
        $('#contextMenu').css({
            top: e.pageY + 'px',
            left: e.pageX + 'px'
        }).addClass('is-open');
        var parentId = $(this).attr('data-parent-id');
        var currId = $(this).attr('id');
        $('#remove-button').data('invoice-parent-row', parentId);
        $('#remove-button').data('invoice-item-row', currId);
    })
}

function removeInvoiceItem(currObj) {
    var parentId = $('#remove-button').data('invoice-parent-row');
    var curId = $('#remove-button').data('invoice-item-row');
    $('#' + parentId).removeClass('avoid-clicks');
    $('#' + curId).remove();
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
    var grandTotal = calculateGrandTotal();
    disableOrEnablePaidetotalField();
    if (!isNaN(grandTotal.grandTotal)) {
        $('#paid_total_field').change();
    }

}

$(document).ready(function () {
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
    $('#submitButton').on('click', function (e) {
        if(!($('#paid_total_field').val())){
            e.preventDefault();
        }
    });

    initSize();
    initColor();
    initCategory();
    initProduct();
    checkFieldError();
    checkTableEmpty();
    paidTotalInputFieldChange();
    $('#contextMenu').click(function () {
        $('#contextMenu').removeClass('is-open');
    });
    $(document).click(function () {
        $('#contextMenu').removeClass('is-open');
    });
});
