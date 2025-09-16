from django import forms
from accounts.models import CustomUser
from seller.models import Seller
from django.core import validators
from seller.validators import allow_only_images_validators



class SellerForm(forms.ModelForm):

    seller_license = forms.FileField(widget=forms.FileInput(attrs={"class":"form-control no-border"}) , validators=[allow_only_images_validators])

    class Meta:
        model = Seller
        fields = ['seller_name' , 'seller_license']

    seller_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    
    def __init__(self, *args, **kwargs):
        super(SellerForm , self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control no-border'




