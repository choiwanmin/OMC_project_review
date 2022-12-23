from django.urls import path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list'),
    path('detail/', views.Recipe_detail.as_view(), name='recipe_detail_view'),
    path('refrigerator/', views.Refrigerator_list.as_view(), name='refrigerator_view'),
]