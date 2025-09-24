from product.models import Cart , Product , Tax

def get_cart_count(request):

    cart_count = 0

    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(custom_user = request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
        except:
            cart_count = 0

    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        
        cart_items = Cart.objects.filter(custom_user = request.user)
        for item in cart_items:
            product = Product.objects.get(pk=item.product.pk)
            subtotal += (product.price * item.quantity)

        get_tax = Tax.objects.filter(is_active=True)

        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            #tax_amount = (tax_percentage / 100) * subtotal
            tax_amount = round(( tax_percentage * subtotal ) / 100 , 2)
            tax_dict.update({tax_type: {str(tax_percentage) : tax_amount}})
            #print(tax_type , tax_percentage , tax_amount)

        # {'FBR': {'9.00':'216.00'}}

        #print(tax_dict)


        for key, inner_dict in tax_dict.items():
            for inner_key, inner_value in inner_dict.items():
                tax += inner_value

        #print(tax)

        

        grand_total = tax + subtotal

    return dict(subtotal=subtotal , tax=tax , grand_total=grand_total , tax_dict=tax_dict)

        




