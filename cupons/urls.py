from django.conf.urls import url
#from .views import CuponApply
from . import views


urlpatterns = [
    url(r'^apply', views.CuponApply, name='apply')
]
