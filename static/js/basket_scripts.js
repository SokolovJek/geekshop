"use strict";

window.onload = function () {
    console.log('DOM ready');
    $('.basket_record').on('change', "input[type='number']", function (event) {
        let qty = event.target.value;
        let productPk = event.target.name;
        console.log(productPk, qty, event);
        $.ajax({
            url:'/basket/change_quantity/' + productPk + '/' +  qty + '/',
            success: function (data){
                console.log(data);
                if (data.status){
                    $('.basket_summary').html(data.change);
                    $('.product_cost' + productPk).html(data.change_price);
                    console.log('.product_cost' + productPk)
                    }
            }
        });
    });
}




