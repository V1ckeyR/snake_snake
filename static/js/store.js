$(document).ready(function () {
    $('#shopping_cart').click(function () {
        $('#order').show()
    })

    $('#close').click(function () {
        $('#order').hide()
    })

    $('.category-bar_btn').click(function () {
        $('.category-bar_btn').removeClass('active')
        $(this).addClass('active')
    })

    var item = $('.item');

    item.hover(function () {
            $(this).children().hide();
            $(this).css('background-image', $(this).children('.item-img').css('background-image'));
        }, function () {
            $(this).children().show();
            $(this).css('background-image', 'none')
    })

    item.click(function () {

    })
})
