from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Category, Product, Rating
from cart.forms import CartAddProductForm
from rest_framework import renderers
from django.db.models import Q, Avg, Sum, Max, Min, Count
from django.conf import settings
from shop.forms import MyFilterForm, RatingCreateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage, EmptyPage
from django.core.mail import send_mail


# почтальон рейтингов и комментариев о товаре
def sender_mail(theme, text):
    send_mail(theme, text, settings.SERVER_EMAIL, [settings.STUFF_EMAIL], fail_silently=False)

# автокомплит слов для jquery
def wordslistAutocomplete(prod):
    w = []
    for k in list(prod.values('description', 'name', 'color__name', 'firm__name')):
        if k['name'].lower() not in w:
            w.append(k['name'].lower())
        if k['color__name'].lower() not in w:
            w.append(k['color__name'].lower())
        for i in k['firm__name'].split():
            if i not in w:
                w.append(i)
        for i in k['description'].split():
            w.append(i.lower().strip(',.'))
    words = list(set(w))
    return words
# уникальные цвета товаров для фильтра по цветам
def colorPicker(prod):
    colors = []
    for n in list(prod.values('color__name')):
        if n['color__name'] not in colors:
            colors.append(n['color__name'])
    return colors

# Пагинатор страниц
def pager(prod, pages, request):
    paginator = Paginator(prod, pages)
    page = request.GET.get('page')
    try:
        prod = paginator.page(page)
    except PageNotAnInteger:
        prod = paginator.page(1)
    except EmptyPage:
        prod = paginator.page(paginator.num_pages)
    return prod

# Страница с товарами
def ProductList(request):

    category = None
    categories = Category.objects.all()
    all_products = Product.objects.all()
    #products = Product.objects.filter(available=True).order_by('-created')[:20] ## Возможна разгруппировка по имени из-за сортировке по дате
    products = all_products.filter(available=True).order_by('-created')
    ###### проверить на  PostgreSQL !!!
    # products = products.distinct('name')
    ######
    ### Выбираем id  только по одному имени каждого товара из новых для главной страницы  ###
    m = {}
    for n in list(products.values('name', 'id')):
            if n['name'] not in m:
                m[n['name']] = n['id']
    products = products.filter(id__in=list(m.values()))
    ### собираем все цвета ###
    colors = colorPicker(products)
    ### Находим уникальные слова из БД для автокомплита поиска ###
    words = wordslistAutocomplete(products)
    ######
    query = request.GET.get('query')
    q = str(query).strip()
    q1 = q.lower()
    #q2 = q.capitalize()
    q2 = q.title()
    #form = MyFilterForm().as_table()
    form = MyFilterForm(initial=request.POST or request.GET or None)
    #if query and not category_slug:
    if query:
        products = all_products.filter(Q(description__icontains=q1, available=True)|
                                       Q(description__icontains=q2, available=True)|
                                       Q(name__icontains=q1, available=True)|
                                       Q(name__icontains=q2, available=True)|
                                       Q(color__name__icontains=q1, available=True)|
                                       Q(color__name__icontains=q2, available=True)|
                                       Q(firm__name__icontains=q, available=True)|
                                       Q(firm__name__icontains=q1, available=True)|
                                       Q(firm__name__icontains=q2, available=True))

        products = pager(products, 6, request)

        return render(request, 'list_shop_filter.html', {'category': category,'categories': categories,
            'products': products , 'form': form, 'words': words })

    # фильтр по характеристикам Django
    sc_select = request.GET.get('sc_select')
    sz_select = request.GET.get('sz_select')
    st_select = request.GET.get('st_select')
    sp_select = request.GET.get('sp_select')
    sn_select = request.GET.get('sn_select')
    r_select = request.GET.get('r_select')
    spp_select = request.GET.get('spp_select')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    ## было and not category_slug
    if sc_select  or sz_select  or st_select \
        or sp_select  or sn_select \
           or spp_select or r_select \
            or price_min or price_max:
        products = all_products.filter(available=True)
        cd = []

        if sz_select != ' ' and sz_select:
            products = products.filter(size__sz=sz_select)
            cd.append(sz_select)
        if sc_select != ' ' and sc_select:
            products = products.filter(color__name=sc_select)
            cd.append(sc_select)
        if st_select != ' ' and st_select:
            products = products.filter(type__name=st_select)
            cd.append(st_select)
        if sp_select != ' ' and sp_select:
            if sp_select == 'Дороже':
                products = products.order_by('-price')
            if sp_select == 'Дешевле':
                products = products.order_by('price')
            cd.append(sp_select)
        if sn_select != ' ' and sn_select:
            if sn_select == 'A':
                products = products.order_by('name')
            if sn_select == 'Z':
                products = products.order_by('-name')
            cd.append(sn_select)
        if r_select:
            products = products.annotate(score=Avg('rate__rating')).order_by('-score')
            cd.append(r_select)
        if spp_select != '5000' and spp_select:
            products = products.filter(price__lte=spp_select)
            cd.append(spp_select)
        if price_min or price_max:
            if price_max and not price_min:
                products = products.filter(price__lte=price_max)
                cd.append(price_max)
            if price_min and not price_max:
                products = products.filter(price__gte=price_min)
                cd.append(price_min)
            if price_max and price_min:
                if price_max > price_min:
                    products = products.filter(price__gte=price_min, price__lte=price_max)
                if price_max < price_min:
                    products = products.filter(price__gte=price_max, price__lte=price_min)
                if price_max == price_min:
                    products = products.filter(price=price_min)
                cd.append(price_min)
                cd.append(price_max)


        colors = colorPicker(products)
        products = pager(products, 6, request)
        return render(request, 'list_shop_filter.html', {'category': category,'categories': categories,
            'products': products , 'form': form, 'words': words , 'cd': cd, 'colors': colors})

    products = pager(products, 6, request)
    bestseller = all_products.filter(available=True, order_items__gt=1).annotate(sells=Count('order_items')).order_by('-sells')[:6]
    return render(request, 'list_shop.html', {'category': category,'categories': categories,
        'products': products , 'form': form , 'words': words, 'colors': colors, 'bestseller': bestseller})

#Страница товара
# def ProductDetail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     return render(request, 'detail.html', {'product': product})


def ProductCatItemList(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, category=category).order_by('name')
    form = MyFilterForm(initial=request.POST or request.GET or None)
    words = wordslistAutocomplete(products)
    cd = []
    colors = colorPicker(products)
    query = request.GET.get('query')
    q = str(query).strip()
    q1 = q.lower()
    q2 = q.title()
    if query:
        products = products.filter(Q(description__icontains=q1, category=category, available=True)|
                                   Q(description__icontains=q2, category=category, available=True)|
                                   Q(name__icontains=q1, category=category, available=True)|
                                   Q(name__icontains=q2, category=category, available=True)|
                                   Q(color__name__icontains=q1, category=category, available=True)|
                                   Q(color__name__icontains=q2, category=category, available=True)|
                                   Q(firm__name__icontains=q, category=category, available=True)|
                                   Q(firm__name__icontains=q1, category=category, available=True)|
                                   Q(firm__name__icontains=q2, category=category, available=True))

    # фильтр по характеристикам Django
    sc_select = request.GET.get('sc_select')
    sz_select = request.GET.get('sz_select')
    st_select = request.GET.get('st_select')
    sp_select = request.GET.get('sp_select')
    sn_select = request.GET.get('sn_select')
    r_select = request.GET.get('r_select')
    spp_select = request.GET.get('spp_select')

    if sc_select  or sz_select  or st_select \
        or sp_select  or sn_select \
           or spp_select or r_select:
        products = products.filter(available=True)

        if sz_select != ' ' and sz_select:
            products = products.filter(size__sz=sz_select)
            cd.append(sz_select)
        if sc_select != ' ' and sc_select:
            products = products.filter(color__name=sc_select)
            cd.append(sc_select)
        if st_select != ' ' and st_select:
            products = products.filter(type__name=st_select)
            cd.append(st_select)
        if sp_select != ' ' and sp_select:
            if sp_select == 'Дороже':
                products = products.order_by('-price')
            if sp_select == 'Дешевле':
                products = products.order_by('price')
            cd.append(sp_select)
        if sn_select != ' ' and sn_select:
            if sn_select == 'A':
                products = products.order_by('name')
            if sn_select == 'Z':
                products = products.order_by('-name')
            cd.append(sn_select)
        if r_select:
            products = products.annotate(score=Avg('rate__rating')).order_by('-score')
            cd.append(r_select)
        if spp_select != '5000' and spp_select:
            products = products.filter(price__lte=spp_select)
            cd.append(spp_select)

    products = pager(products, 6, request)
    return render(request, 'list.html', { 'category': category,'categories': categories,
                                          'products': products , 'form': form, 'words': words, 'colors': colors, 'cd': cd })


def ProductDetail(request, id, slug):
    rating_form = RatingCreateForm()
    cart_product_form = CartAddProductForm()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    ## все цвета и размеры на станице товара для данной модели ##
    clrs = []
    sizs = []
    for cs in list(Product.objects.filter(slug=slug).values('size__sz', 'color__name')):
        if cs['color__name'] not in clrs:
            clrs.append(cs['color__name'])
        if cs['size__sz'] not in sizs:
            sizs.append(cs['size__sz'])
    clrs = (', ').join(clrs)
    sizs = (', ').join(sizs)
    ######
    if request.method == "POST":
        rating_form = RatingCreateForm(request.POST)
        if rating_form.is_valid():
            cd = rating_form.cleaned_data
            Rating.objects.create(rating=cd['rating'], product_id=product.id, email=cd['email'], 
                author=cd['author'], ratingcomment=cd['ratingcomment'])
            link = 'localhost:8000' + product.get_absolute_url()
            text = 'от: %s. \nОтзыв: %s. \nПоставил(а) оценку: %s. \nссылка на товар: %s \nНапоминание: необходимо разрешить показывать' \
                    ' этот отзыв на сайте или удалить...' % (cd['author'].title(), cd['ratingcomment'].capitalize(), cd['rating'], link)
            sender_mail('Оставлен новый комментарий о товаре', text)
            return render(request, 'detail.html', {'product': product, 'cart_product_form': cart_product_form })
    return render(request, 'detail.html', {'product': product, 'cart_product_form': cart_product_form, 'rating_form': rating_form, 'clrs':clrs , 'sizs':sizs})


def successPage(request):
    categories = Category.objects.all()
    # m = request.POST ## словари
    # n = request.GET
    return render(request, 'success.html', {'categories': categories})



 # ###Сериализация для Vue
        # vue_prods = products.values('id', 'name', 'size__sz', 'description', 'price', 'image', 'type__name')
        # for item in vue_prods:
        #     #получаем url картинки
        #     item['image'] = settings.MEDIA_URL + item['image']
        #     #получаем url товара
        #     prod_url  = get_object_or_404(Product, id=item['id'])
        #     prod_url = prod_url.get_absolute_url()
        #     item['url'] = prod_url
        #     #пишем кверисет в словарь
        #     dict(item)
        # vue_products = renderers.JSONRenderer().render(vue_prods, 'application/json')
        # ###


# # фильтр по характеристикам старый
    # def page_filter(prod):
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         s_size = cd['sz_select']
    #         if s_size != 'V':
    #             prod = prod.filter(size__sz=s_size)
    #         s_type = cd['st_select']
    #         if s_type != 'V':
    #             prod = prod.filter(type__name=s_type)
    #         s_price = cd['sp_select']
    #         if s_price != 'V':
    #             if s_price == 'Дороже':
    #                 prod = prod.order_by('-price')
    #             if s_price == 'Дешевле':
    #                 prod = prod.order_by('price')
    #         s_alfa = cd['sn_select']
    #         if s_alfa != 'V':
    #             if s_alfa == 'A':
    #                 prod = prod.order_by('name')
    #             if s_alfa == 'Z':
    #                 prod = prod.order_by('-name')
    #         s_color = cd['sc_select']
    #         if s_color != 'V':
    #             if s_color == 'W':
    #                 prod = prod.filter(color__name='Белый')
    #             if s_color == 'G':
    #                 prod = prod.filter(color__name='Зеленый')
    #             if s_color == 'B':
    #                 prod = prod.filter(color__name='Бежевый')
    #         sp_price = cd['spp_select']
    #         if sp_price != '5000':
    #             prod = prod.filter(price__lte=sp_price)
    #         r_rate = cd['r_select']
    #         if r_rate:
    #            # агрегация по полю отношения rate__rating с подсчетом среднего арифметического и сортировкой по убыванию
    #            # собираем все значения поля rating (табл Rating) через отношение related_name=rate (табл Product)
    #            prod = prod.annotate(score = Avg('rate__rating')).order_by('-score')
    #            #prod.values('rate').annotate(score = Sum('rate')).order_by('-score')
    #            #prod.values('rate').annotate(score = Avg('rate__rating')).order_by('-score')
    #            #.aggregate(Avg('price'))
    #         return prod

    # ## фильтр по характеристикам Django
    # if request.method == "POST":
    #     form = MyFilterForm(request.POST)
    #     # меняется порядок сортировки по дате при пустом фильтре если включить ниже строку
    #     products = all_products.filter(category=category, available=True)
    #     #products = page_filter(products)
