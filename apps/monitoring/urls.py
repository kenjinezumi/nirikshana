from django.urls import path
from . import views
from .api import search_api


urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    path('api/search/', search_api, name='search_api'),
]