from django import forms
from product.models import Product
from seller.validators import allow_only_images_validators


class ProductForm(forms.ModelForm):

    image = forms.FileField(widget=forms.FileInput(attrs={'class':"form-control no-border"}) , validators=[allow_only_images_validators])
    
    class Meta:
        model = Product
        fields = ['category' , 'product_title' , 'description' , 'price' , 'image' , 'is_available']


    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'is_available':
                field.widget.attrs['class'] = 'form-control'







