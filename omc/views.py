from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM
from django.db.models import Q
# from .forms import CategoryForm

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

        context['category_t'] = CategoryT.objects.all()
        context['category_s'] = CategoryS.objects.all()
        context['category_i'] = CategoryI.objects.all()
        context['category_m'] = CategoryM.objects.all()

        return context

class Recipe_detail(DetailView):
	model = Recipe

class Refrigerator_list(TemplateView):
    template_name = 'omc/refrigerator_list.html'

class RecipeSearch(RecipeList):
    paginate_by = 40
    # paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        recipe_list = Recipe.objects.filter(
            Q(name__contains=q) # | Q(tags__name__contains=q) | Q(content__contains=q)
        ).distinct()
        return recipe_list

    def get_context_data(self, **kwargs):
        context = super(RecipeSearch, self).get_context_data(**kwargs)

        if not context.get('is_paginated', False):
            pages = [1]
        else:
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
        context['category_t'] = CategoryT.objects.all()
        context['category_s'] = CategoryS.objects.all()
        context['category_i'] = CategoryI.objects.all()
        context['category_m'] = CategoryM.objects.all()
        
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        context['search_word'] = q
        return context