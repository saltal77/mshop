from django.conf.urls import url
from . import views
urlpatterns = [
    #url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList, name='ProductListByCategory'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductCatItemList, name='ProductListByCategory'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail, name='ProductDetail'),
    url(r'^$', views.ProductList, name='ProductList'),
    #url(r'^$', views.ProductList.as_view(), name='ProductList'),


]