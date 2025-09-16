from django.core.exceptions import ValidationError
import os


def allow_only_images_validators(value):
    ext = os.path.splitext(value.name)[1] # license-imgage.jpg

    valid_extensions = ['.png' , '.jpg' , '.jpeg']

    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension allowed extensions: ' +str(valid_extensions))
    






