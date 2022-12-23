from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe

# Create your views here.
def index(requests):
    # recipe = recipe.objects.all().order_by("-")
    return render(requests,"index.html")


class RecipeList(ListView):
    model = Recipe
    paginate_by = 40

class Recipe_detail(DetailView):
	model = Recipe

class Refrigerator_list(TemplateView):
    template_name = 'omc/refrigerator_list.html'
