from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Recipe, Ingredient, RecipeOrder, RecipeHashTag

# Create your views here.
def index(requests):
    # recipe = recipe.objects.all().order_by("-")
    return render(requests,"index.html")


class RecipeList(ListView):
    model = Recipe
    paginate_by = 40
    template_name = 'omc/recipe_list_view.html'
    ordering='pk'

    def get_context_data(self, **kwargs):
        context = super(RecipeList, self).get_context_data(**kwargs)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context

class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'omc/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetail,self).get_context_data()
        context['ingredients'] = Ingredient.objects.filter(recipeId=context['recipe'].pk)
        context['ingredients_types'] = Ingredient.objects.filter(recipeId=context['recipe'].pk).values_list('type').distinct().values('type')
        print(context)
        return context

        
class RefrigeratorList(TemplateView):
    template_name = 'omc/refrigerator_list_view.html'
    
    def get_context_data(self, **kwargs):
        context=super(RefrigeratorList, self).get_context_data()
        context['ingredients']=Ingredient.objects.all().order_by('pk')[:5]
        return context
