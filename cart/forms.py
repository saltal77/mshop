from django import forms
#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
class CartAddProductForm(forms.Form):
    #quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='Количество')
    #quantity = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength': '2', 'pattern': '\d+' }),label='Количество', min_value=1, max_value=20, initial=1)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'maxlength': '2'}), label='Количество', min_value=1, max_value=20, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)