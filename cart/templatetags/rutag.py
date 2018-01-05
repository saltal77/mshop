from django import template

register = template.Library()

# pluralize for russian language
# {{someval|rupluralize:"товар,товара,товаров"}}
@register.filter(is_safe = False)
#@stringfilter
#@register.filter
def rupluralize(value, arg):
    bits = arg.split(u',')
    try:
        value = str( 0 if not value or value <= 0 else value )[-1:] # patched version
        return bits[ 0 if value=='1' else (1 if value in '234' else 2) ]
    except:
        raise TemplateSyntaxError
    return ''


# def сhoice(string):
#     """
#     Добавляет к тексту строку рекомендации редактора
#     """
#     new_string = ''
#     chs = '  *** от редакции - Отличная История!'
#     new_string = string + chs
#     return new_string

# register.filter('сhoice', сhoice)
#{% load rutag %}

