from django.forms import Form, ImageField



class TempImageForm(Form):
    image = ImageField()