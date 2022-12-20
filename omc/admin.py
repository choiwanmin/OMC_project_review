from django.contrib import admin
from .models import Recipe, RecipeOrder, Ingredient

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeOrder)