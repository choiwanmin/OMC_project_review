from django.urls import path, re_path
from . import views

app_name ="omc"
urlpatterns = [
    path('', views.RecipeList.as_view(), name='recipe_list_view'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail_view'),
    path('refrigerator/', views.RefrigeratorList.as_view(), name='refrigerator_view'),
    path('search/<str:q>/', views.RecipeSearch.as_view(), name='recipe_search'),
    re_path(r'category/[0-9]{8}/', views.RecipeCategory.as_view(), name='recipe_category'),
    path('category/<int:pk>/', views.RecipeCategory.as_view(), name='recipe_search'),
    path('recommend/', views.RecipeRecommend.as_view(), name='recipe_recommend'),
    path('<int:pk>/new_comment/', views.NewComment.as_view(), name='new_comment'),
    path('update_comment/<int:pk>/', views.UpdateComment.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]
