from django import forms
from accounts.models import CustomUser

class CustomerForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name' , 'last_name' , 'username' , 'email' , 'password']


    def __init__(self, *args, **kwargs):
        super(CustomerForm , self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    def clean(self):
        
        cleaned_data = super(CustomerForm , self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match')
        
        





