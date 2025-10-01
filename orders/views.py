from django.shortcuts import render , redirect , HttpResponse
from product.models import Cart , Product , Category
from orders.models import Payment , Order , OrderedProduct
from django.contrib.auth.decorators import login_required
from product.context_processors import get_cart_amounts
from orders.forms import OrderForm
import simplejson as json
from orders.utils import generate_order_number , order_total_by_seller
from accounts.utils import send_notification_email
from django.http import JsonResponse
from product.models import Tax
from django.contrib.sites.shortcuts import get_current_site



# Create your views here.

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(custom_user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('all_products')
    
    sellers_ids = []
    for i in cart_items:
        if i.product.seller.id not in sellers_ids:
            sellers_ids.append(i.product.seller.id)
    
    # {"seller_id":{"subtotal":{"tax_type":{"tax_percentage":"tax_amount"}}}}

    get_tax = Tax.objects.filter(is_active=True)

    # Calculate subtotal per seller

    seller_subtotals = {}
    for i in cart_items:
        product = Product.objects.get(pk=i.product.pk)
        #print(product , product.seller.id)
        seller = product.seller.id 
        product_total = product.price * i.quantity

        if seller in seller_subtotals:
            subtotal = seller_subtotals[seller]
            subtotal += product_total
            seller_subtotals[seller] = subtotal
        else:
            seller_subtotals[seller] = product_total
    
    #print(vendor_subtotals)
    

    # Calculate tax for each seller's subtotal

    total_data = {}

    for seller_id , subtotal in seller_subtotals.items():

        tax_dict = {}

        for tax in get_tax:
            tax_type = tax.tax_type
            tax_percentage = tax.tax_percentage

            tax_amount = round((tax_percentage * subtotal) / 100 , 2)
            tax_dict.update({tax_type: {str(tax_percentage): str(tax_amount)}})
        
        total_data.update({seller_id: {str(subtotal): str(tax_dict)}})
    
    #print(total_data)


    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.custom_user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.pk)
            order.sellers.add(*sellers_ids)
            order.save()

            context = {
                'order':order,
                'cart_items':cart_items,
            }

            return render(request , 'orders/place_order.html' , context)


    return render(request , 'orders/place_order.html')

@login_required
def payments(request):

    # check if the request is ajax or not
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        
        # store the payment details in the payment model 

        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(custom_user=request.user , order_number=order_number)
        payment = Payment()
        payment.custom_user = request.user
        payment.transaction_id = transaction_id
        payment.payment_method = payment_method
        payment.amount = order.total
        payment.status = status
        payment.save()

        # update the order model

        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # move the cart items to the to ordered product model

        cart_items = Cart.objects.filter(custom_user = request.user)
        for item in cart_items:
            ordered_product = OrderedProduct()
            ordered_product.order = order
            ordered_product.payment = payment
            ordered_product.custom_user = request.user
            ordered_product.product = item.product
            ordered_product.quantity = item.quantity
            ordered_product.price = item.product.price
            ordered_product.amount = item.product.price * item.quantity # total amount
            ordered_product.save()


        # send order confirmation email to the customer

        mail_subject = 'thank you for ordering with us'
        mail_template = 'orders/order_confirmation_email.html'

        ordered_product = OrderedProduct.objects.filter(order=order)
        customer_subtotal = 0
        for item in ordered_product:
            customer_subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        
        context = {
            'user' : request.user,
            'order' : order,
            'to_email' : order.email,
            'ordered_product':ordered_product,
            'domain':get_current_site(request),
            'customer_subtotal':customer_subtotal,
            'tax_data':tax_data,
        }
        send_notification_email(mail_subject , mail_template , context)


        # send order received email to the seller

        mail_subject = 'you have received a new order'
        mail_template = 'orders/order_received_email.html'
        to_email = []
        for i in cart_items:
            if i.product.seller.custom_user.email not in to_email:
                to_email.append(i.product.seller.custom_user.email)

                ordered_product_to_seller = OrderedProduct.objects.filter(order=order , product__seller=i.product.seller)
                context = {
                    'user' : request.user,
                    'order' : order,
                    'to_email' : i.product.seller.custom_user.email,
                    'ordered_product_to_seller':ordered_product_to_seller,
                    'seller_subtotal': order_total_by_seller(order , i.product.seller.id)['subtotal'],
                    'seller_tax_data': order_total_by_seller(order , i.product.seller.id)['tax_dict'],
                    'seller_grand_total': order_total_by_seller(order , i.product.seller.id)['grand_total'],
                }
                send_notification_email(mail_subject , mail_template , context)


        # clear the cart if the payment is success
        cart_items.delete()


        # return back to ajax with the status success or failure
        response = {
            'order_number':order_number,
            'transaction_id':transaction_id,
        }
        return JsonResponse(response)



    return HttpResponse('payment view')


def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number , payment__transaction_id=transaction_id , is_ordered=True)
        ordered_product = OrderedProduct.objects.filter(order=order)

        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
        
        tax_data = json.loads(order.tax_data)



        context = {
            'order':order,
            'ordered_product':ordered_product,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request , 'orders/order_complete.html' , context)
    except:
        return redirect('home')

    






