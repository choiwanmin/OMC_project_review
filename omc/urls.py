from django.urls import path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.Recipe_list.as_view(), name='recipe_view'),
    path('detail/', views.Recipe_detail.as_view(), name='recipe_detail_view')
]