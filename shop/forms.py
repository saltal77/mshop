from django import forms
from .models import Rating
from django.core.validators import MinValueValidator, MaxValueValidator

class MyFilterForm(forms.Form):
    CHOICES_SZ= (
    (' ','Все'),
    ('XS','оч.Маленький'),
    ('S','Маленький'),
    ('M','Средний'),
    ('L','Большой'),
    ('XL','оч.Большой'),
             )
    CHOICES_ST= (
    (' ','Все'),
    ('Мужские','Мужские'),
    ('Женские','Женские'),
             )
    CHOICES_SP= (
    (' ','Не задано'),
    ('Дороже','сначала дороже'),
    ('Дешевле','сначала дешевле'),
             )
    CHOICES_SN= (
    (' ','Не задано'),
    ('A','от А-Я'),
    ('Z','от Я-А'),
             )
    CHOICES_CLR= (
    (' ','Не задано'),
    ('Белый','Белый'),
    ('Бежевый','Бежевый'),
    ('Зеленый', 'Зеленый'),
             )
    sz_select = forms.ChoiceField(label='Размер', widget=forms.Select, choices=CHOICES_SZ, initial='Все')
    st_select = forms.ChoiceField(label='Тип', widget=forms.RadioSelect(attrs={'class': 'segmented', 'onchange':'this.form.submit()'}), choices=CHOICES_ST, initial=' ')
    sp_select = forms.ChoiceField(label='Цена', widget=forms.Select, choices=CHOICES_SP, initial='Не задано')
    sn_select = forms.ChoiceField(label='По алфавиту', widget=forms.Select, choices=CHOICES_SN, initial='Не задано')
    spp_select = forms.IntegerField(label='цена до', widget=forms.NumberInput(attrs={'type':'range', 'step': '50',
     'min': '0', 'max': '5000', 'value': '5000', 'oninput': 'curVal()', 'onchange':'this.form.submit()' }))
    #sc_select = forms.ChoiceField(label='Цвет', widget=forms.Select(attrs={'onchange':'this.form.submit()'}), choices=CHOICES_CLR, initial='Не задано')
    sc_select = forms.CharField(widget=forms.HiddenInput(attrs={'value': ' ', 'id': 'color'}))
    r_select = forms.BooleanField(label='По рейтингу', initial=False, required=False)
    price_min = forms.IntegerField(label='от',
    widget=forms.TextInput(attrs={ 'maxlength': '6', 'pattern': '\d+', 'placeholder': 'min', 'onchange':'this.form.submit()'}), required=False)
    price_max = forms.IntegerField(label='до',
    widget=forms.TextInput(attrs={'maxlength': '6', 'pattern': '\d+', 'placeholder' : 'max', 'onchange':'this.form.submit()'}), required=False)


class RatingCreateForm(forms.ModelForm):
    CHOICES_R= (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    )
   
    rating = forms.ChoiceField(label='Оценка товара', widget=forms.RadioSelect(attrs={'class': 'form-control'}), required=True, choices=CHOICES_R)
    author = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}), required=True)
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}), required=True)
    ratingcomment = forms.CharField(label='Отзыв', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}), required=True)
    
    class Meta:
        model = Rating
        fields = ['author', 'email', 'ratingcomment', 'rating']


