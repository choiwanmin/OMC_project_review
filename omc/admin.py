from django.contrib import admin
from .models import Recipe, RecipeOrder, Ingredient, CategoryT, CategoryS, CategoryI, CategoryM

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeOrder)
admin.site.register(CategoryT)
admin.site.register(CategoryS)
admin.site.register(CategoryI)
admin.site.register(CategoryM)