$(document).ready(function () {
    $('.item').hover(function () {
            $(this).children().hide();
            $(this).css('background-image', $(this).children('.item-img').css('background-image'));
        }, function () {
            $(this).children().show();
            $(this).css('background-image', 'none')
    });
})
