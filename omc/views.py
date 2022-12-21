from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import models

# Create your views here.
def index(requests):
    # recipe = recipe.objects.all().order_by("-")
    return render(requests,"index.html")

class Recipe_list(TemplateView):
    template_name = 'omc/recipe.html'

class Recipe_detail(TemplateView):
    template_name = 'omc/recipe_detail.html'
