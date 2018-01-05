from django import forms
class CuponApllyForm(forms.Form):
    code = forms.CharField(label='Промокод', widget=forms.TextInput(attrs={'class': 'form-control',
    	'placeholder': 'Введите код скидки...'}))
