from django import forms 
from orders.models import Order , Payment , OrderedProduct
from accounts.models import CustomUser

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name' , 'last_name' , 'phone' , 'email' , 'address' , 'country' , 'state' , 'city' , 'pin_code']

    def __init__(self, *args, **kwargs):
        super(OrderForm , self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control no-border'




