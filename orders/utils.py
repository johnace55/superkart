from datetime import datetime


def generate_order_number(pk):
    
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S') #2025/01/10
    order_number = current_datetime + str(pk)
    return order_number






