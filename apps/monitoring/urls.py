from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('search/', views.SearchAPIView.as_view(), name='search_api'),
    path('results/', views.SearchResultsView.as_view(), name='search_results'),
]
