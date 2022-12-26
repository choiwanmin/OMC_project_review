from django.urls import path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list_view'),
    path('detail/', views.Recipe_detail.as_view(), name='recipe_detail_view'),
    path('refrigerator/', views.Refrigerator_list.as_view(), name='refrigerator_view'),
    path('search/<str:q>/', views.RecipeSearch.as_view(), name='recipe_search'),
]
