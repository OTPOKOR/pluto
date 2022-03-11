from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms
from product.models import Description_Middle

class FormFromSomeModel(forms.ModelForm):
    class Meta:
        model = Description_Middle
        fields = ['foreign_product','description']
        widgets = {
            'description': SummernoteWidget()
        }