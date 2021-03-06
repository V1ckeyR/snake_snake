$(document).ready(function () {
    var order = Array();
    var item = $('.item');
    var orderContent = $('#order-content');
    var orderButtons = $('#order-buttons');
    var dollarLocale = Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumSignificantDigits: 2,
        minimumFractionDigits: 2,
    });

    function drawOrderList() {
        orderButtons.html('')
        if (!order.length) {
            orderContent.html('<span>Oops, it\'s nothing here :(</span>')
        } else {
            orderContent.html('')
            var total = 0;
            for (let i in order) {
                var id = order[i]
                var cost = $(`#${id}`).children('.cost').text()
                total += parseFloat(cost.slice(1))
                orderContent.append(`
                    <div class="order-card">
                        <span>${ parseInt(i) + 1 }</span>
                        <div class="item-img"></div>
                        <div class="dotted-line"></div>
                        <span id="cost_${id}">${cost}</span>
                        <span id="close_${id}" class="close">&times;</span>
                    </div>
                `)
                $(`#close_${id}`).click( function () {
                    var id =  $(this).attr('id').split('_')[1]
                    order.splice(order.indexOf(id), 1);
                    $(`#${id}`).children('.tip_item').html('+');
                    drawOrderList();
                })
            }
            orderContent.append(`
                <div class="order-card">
                    <span>TOTAL</span>
                    <div class="dotted-line"></div>
                    <span>${ dollarLocale.format(total) }</span>
                </div>
            `)
            orderButtons.append('<button id="submit_order" type="submit">Submit</button>')
        }
    }

    $('#shopping_cart').click(function () {
        $('#order').show()
        drawOrderList()
    })

    $('#close_shopping_cart').click(function () {
        $('#order').hide();
    })

    $('.category-bar_btn').click(function () {
        $('.category-bar_btn').removeClass('active');
        $(this).addClass('active');
    })

    item.hover(function () {
            $(this).children().hide();
            $(this).css('background-image', $(this).children('.item-img').css('background-image'));
            $(this).children('.tip_item').show();
        }, function () {
            $(this).children().show();
            $(this).css('background-image', 'none');
            $(this).children('.tip_item').hide();
    })

    item.click(function () {
        var id = $(this).attr('id');
        if (order.includes(id)) {
            order.splice(order.indexOf(id), 1)
            $(this).children('.tip_item').html('+');
        } else {
            order.push($(this).attr('id'))
            $(this).children('.tip_item').html('&times');
        }
    })
})
