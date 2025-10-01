from datetime import datetime
import simplejson as json
import ast


def generate_order_number(pk):
    
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S') #2025/01/10
    order_number = current_datetime + str(pk)
    return order_number


def order_total_by_seller(order , seller_id):

    subtotal = 0
    tax = 0
    tax_dict = {}
    total_data = json.loads(order.total_data)
    data = total_data.get(str(seller_id))


    for key , value in data.items():
        subtotal += float(key)
        value_dict = ast.literal_eval(value)
        tax_dict.update(value_dict)

        # {'FBR': {'9.00': '119.88'}, 'WHT': {'7.00': '93.24'}}
            
        for tax_type, tax_info in value_dict.items():
            #print(tax_info)
            for percentage , amount in tax_info.items():
                tax += float(amount)
    grand_total = float(subtotal) + float(tax)
    context = {
        'subtotal':subtotal,
        'tax_dict':tax_dict,
        'grand_total':grand_total,
    }
    return context






