from django.db import models
from django.core.urlresolvers import reverse
from django_comments.moderation import CommentModerator, moderator
from django.db.models.signals import post_save
from django_comments.models import Comment
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

# Модель размер продукта
class Size(models.Model):
    PROD_SIZES = (
        ('XS', 'очень Маленький'),
        ('S', 'Маленький'),
        ('M', 'Средний'),
        ('L', 'Большой'),
        ('XL', 'очень Большой'),
        ('N', 'Не Имеет')
    )
    sz = models.CharField(db_index=True, unique=True, max_length=2, choices=PROD_SIZES,  verbose_name="Размер")

    class Meta:
        ordering = ['sz']
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.sz


# Модель Тип продукта ## ошибка названия Type!!!
class Type(models.Model): 
    name = models.CharField(max_length=200, db_index=True, verbose_name="Тип")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name

# Модель Цвет
class Color(models.Model):
    name = models.CharField(max_length=200, db_index=True , verbose_name="Цвет", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name

# Модель Производитель
class Firm(models.Model):
    name = models.CharField(max_length=200, db_index=True , verbose_name="Производитель", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name  
              

# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True , verbose_name="Категория")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# Модель продукта
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='types', verbose_name="Категория (-Тип)")
    type = models.ForeignKey(Type, related_name='products', verbose_name="Тип (-Категория)") ## ошибка названия type!!!
    size = models.ForeignKey(Size, related_name='sizes', verbose_name="Размер")
    color = models.ForeignKey(Color, related_name='colors', verbose_name="Цвет", null=True)
    firm = models.ForeignKey(Firm, related_name='firms', verbose_name="Производитель", null=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Занесен")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    enable_comments = models.BooleanField(default=True, verbose_name="Разрешить комментарий")
    recommended = models.BooleanField(default=False, verbose_name='Рекоммендуемый')

    # ## методы save и delete переопределенные для избежания образоваия мусорных/безхозных фото ##
    ## ((( фотки мусорные остаются, перестала работать на сохранение форма рейтингов ((( ##
    # def save(self, *args, **kwargs):
    #     try:
    #         this_record = Product.objects.get(pk=self.pk)
    #         if this_record.image != self.image:
    #             this_record.image.delete(save=False)
    #     except:
    #         pass
    #     super(Product, self).save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     self.image.delete(save=False)
    #     super(Product, self).delete(*args, **kwargs)
    # ################################################

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.id, self.slug])

    def get_stock_status(self):
        return True if self.stock > 0 else False

    def str_category(self):
        return str(self.category)

    def has_size(self):
        # возвращает строковое представление размера для сравнения по условию в шаблоне  (тк поле внешнее и возвращается просто число)
        return str(self.size)

    def has_type(self):
        # возвращает строковое представление Тип (М/Ж) для сравнения по условию в шаблоне (тк поле внешнее и возвращается просто число)
        return str(self.type)


    def get_ratings(self):
        # собираем все рейтинги через связь related_name='rate' в таблице Rating из Product
        # собираем именно значения rating и переводим в список
        # выводим среднее арифметическое
        #r = list(self.rate.filter(flag=True).values_list('rating'))
        r = list(self.rate.filter(flag=True).values_list('rating'))
        c = len(r)
        m = 0
        for i in r:
            m += i[0]
        return round(m/c)

    def allow_comments(self):
        return self.rate.filter(flag=True).count()

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

# Модель Рейтинг
class Rating(models.Model):
    rating = models.PositiveIntegerField(verbose_name='рейтинг', default=0)
    product = models.ForeignKey(Product, related_name='rate', verbose_name="Товар", null=True)
    author = models.CharField(max_length=50, db_index=True , verbose_name="Автор", unique=True, null=True)
    email = models.EmailField(verbose_name='Почта',max_length=80, null=True)
    ratingcomment = models.TextField(verbose_name='Отзыв', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Оставлен")
    flag = models.BooleanField(verbose_name='Отобразить на сайте', default=False)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return str(self.rating)

    def display(self):
        return self.flag


# Автомодератор для комментариев
class ProductModerator(CommentModerator):
    email_notification = False
    enable_field = 'enable_comments'
    auto_moderate_field = 'created'
    moderate_after = 0

moderator.register(Product, ProductModerator)


def sender_mail(theme, text):
    send_mail(theme, text, settings.SERVER_EMAIL, [settings.STUFF_EMAIL], fail_silently=False)
    
# Отправка письма по событию post_save()
def notify_of_comment(sender, instance, **kwargs):
    theme = 'Оставлен новый комментарий о товаре'
    link = 'localhost:8000' + instance.get_content_object_url()
    text = 'от: %s. \nОтзыв: %s. \nссылка на товар: %s \nНапоминание: необходимо разрешить показывать' \
                    ' этот отзыв на сайте или удалить...' % (instance.user_name.title(), instance.comment.capitalize(), link)
    #text += instance.get_as_text()
    sender_mail(theme, text)

post_save.connect(notify_of_comment, sender=Comment)