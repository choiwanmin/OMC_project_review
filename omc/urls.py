from django.urls import path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list_view'),
    path('detail/', views.Recipe_detail.as_view(), name='recipe_detail_view'),
    path('refrigerator/', views.RefrigeratorList.as_view(), name='refrigerator_view'),
]
