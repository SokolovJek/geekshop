$(document).ready(function(){

    
    let total_form = parseInt($('#id_orderitems-TOTAL_FORMS').val())
    let total_cost = parseInt($('.order_total_cost').text());
    let total_quantity = parseInt($('.order_total_quantity').text());
    let all_quantity_arr = [];
    let all_summary_arr = [];
    let event_target,item_index,delta_quantity,item_current_quantity
    let input_checkbox = 1


    $('.formset_row').formset({
    addText: 'добавить продукт',
    deleteText: 'удалить',
    prefix: 'orderitems',
    removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
    console.log('dddd')
    var target_name= row[0].querySelector('input[type="number"]').name;
    orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
    total_quantity = total_quantity - all_quantity_arr[orderitem_num];
    total_cost = total_cost - (all_summary_arr[orderitem_num] * all_quantity_arr[orderitem_num])
    $('.order_total_cost').text(total_cost)
    $('.order_total_quantity').text(total_quantity)
    }


    
    for(i=0; i < total_form; i++){
        all_quantity_arr[i] = parseInt($('#id_orderitems-' + i + '-quantity').val())

        if(!parseInt($('.orderitems-' + i + '-price').text())){
            all_summary_arr[i] = 0
        }else{
            all_summary_arr[i] = parseInt($('.orderitems-' + i + '-price').text())
        }
        
    }

    $('.formset_row').click(function(){
        console.log('ddddddd')
        event_target = event.target.id
        item_index = parseInt(event_target.replace('id_orderitems-','').replace('-quantity'))

        //  МОЙ ВАРИАНТ ПРОВЕРКИ CHECKBOX
        // if(event.target.type == 'checkbox'){
        //     if($('#id_orderitems-' + item_index + '-DELETE').is(':checked')){
        //     total_quantity = total_quantity - all_quantity_arr[item_index];
        //     total_cost = total_cost - (all_summary_arr[item_index] * all_quantity_arr[item_index])
        //     input_checkbox = 0
        //     }else{
        //         total_quantity = total_quantity + all_quantity_arr[item_index];
        //         total_cost = total_cost + (all_summary_arr[item_index] * all_quantity_arr[item_index])
        //         input_checkbox = 1
        //     }
        // }else{


        

        delta_quantity = all_quantity_arr[item_index] - parseInt($('#id_orderitems-'+ item_index +'-quantity').val())
        
        item_current_quantity = parseInt($('#id_orderitems-'+ item_index +'-quantity').val())

        total_quantity = total_quantity - delta_quantity;
        total_cost = (total_cost - (all_summary_arr[item_index] * all_quantity_arr[item_index])) + (all_summary_arr[item_index] * item_current_quantity)

        all_quantity_arr[item_index] = item_current_quantity
        

        
    
    $('.order_total_cost').text(total_cost)
    $('.order_total_quantity').text(total_quantity)



    })


});
