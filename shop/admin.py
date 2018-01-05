from django.contrib import admin
from .models import Category, Product, Type, Size, Color, Rating, Firm



class FirmAdmin(admin.ModelAdmin):
    list_display = ['name' ]
    list_filter = ['name']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['created', 'product', 'rating', 'author', 'flag']
    list_filter = ['product', 'created', 'rating']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name',]
# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
# Модель Размер
class SizeAdmin(admin.ModelAdmin):
    list_display = ['sz',]
# Модель Тип
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'size', 'type', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'name', 'size', 'type', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}



admin.site.register(Firm, FirmAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Product, ProductAdmin)