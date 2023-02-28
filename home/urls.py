from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('term_autocomplete/<str:model_type>/', views.term_autocomplete, name='term_autocomplete'),
    path('graph_update/', views.graph_update, name='graph_update'),
]