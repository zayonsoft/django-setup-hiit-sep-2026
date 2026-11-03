from django.forms import ModelForm
from myapp.models import Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ["uploaded_by"]
