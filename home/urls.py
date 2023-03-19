from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('generic/', views.generic, name='generic'),
    path('elements/', views.elements, name='elements'),

    path('term_autocomplete/<str:model_type>/', views.term_autocomplete, name='term_autocomplete'),
    path('graph_update/', views.graph_update, name='graph_update'),
    path('reverse/', views.reverse, name='reverse'),
]