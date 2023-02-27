from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('term_autocomplete/', views.term_autocomplete, name='term_autocomplete')
    path('term_autocomplete/<str:model_type>/', views.term_autocomplete, name='term_autocomplete'),
#     path('add/', views.add, name='add'),
#     path('add/create/', views.create, name='create')
]