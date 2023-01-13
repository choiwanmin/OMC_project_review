
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
# from omc.signup_form import UserForm
from django.contrib.auth import authenticate, login
from .models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM, RecipeOrder, Ingredient, RecipeHashTag, UserIngredient
# from .forms import CategoryForm
from django.core.paginator import Paginator

# Create your views here.
def index(requests):
    # recipe = recipe.objects.all().order_by("-")
    return render(requests,"index.html")

# def category(request):
#     if request.method == 'POST':
#         cat = request.POST.get('cat', '')
#         request.session['cat_name'] = cat
#         request.session['cat_type'] = "cat"

#         return redirect('/recipe/')

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
        context['category'] = {
            '종류별' : CategoryT.objects.all(),
            '상황별' : CategoryS.objects.all(),
            '재료별' : CategoryI.objects.all(),
            '방법별' : CategoryM.objects.all(),
        }

        return context

class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'omc/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetail,self).get_context_data()
        context['ingredients'] = Ingredient.objects.filter(recipeId=context['recipe'].pk)
        context['ingredients_types'] = Ingredient.objects.filter(recipeId=context['recipe'].pk).values_list('type').distinct().values('type')
        context['recipehastags'] = RecipeHashTag.objects.filter(recipeId=context['recipe'].pk)
        context['recipe_order'] = RecipeOrder.objects.filter(recipeId=context['recipe'].pk)
        if context['recipe'].categoryTId != None:
            context['category_t'] = CategoryT.objects.get(pk=context['recipe'].categoryTId_id)
            context['category_s'] = CategoryS.objects.get(pk=context['recipe'].categorySId_id)
            context['category_i'] = CategoryI.objects.get(pk=context['recipe'].categoryIId_id)
            context['category_m'] = CategoryM.objects.get(pk=context['recipe'].categoryMId_id)
        return context

class RefrigeratorList(TemplateView):
    template_name = 'omc/refrigerator_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super(RefrigeratorList, self).get_context_data()
        context['ingredients'] = UserIngredient.objects.all()
        context['ingredients_types'] = UserIngredient.objects.all().values_list('type').distinct().values('type')
        return context


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
    # 사용자 인증
            login(request, user) # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'omc/signup_view.html', {'form': form})

    
class RecipeSearch(RecipeList):
    paginate_by = 40
    # paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']

        recipe_queryset = Recipe.objects.filter(name__contains=q)
        irg_queryset = Recipe.objects.filter(ingredient__name__contains=q)
        recipe_order_queryset = Recipe.objects.filter(recipeorder__description__contains=q)
        hashtag_queryset = Recipe.objects.filter(recipehashtag__description__contains=q)
        recipe_queryset = recipe_queryset.union(irg_queryset,recipe_order_queryset,hashtag_queryset).order_by('-viewCount')
        return recipe_queryset

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

class RecipeCategory(RecipeList):
    
    def post(self,request, **kwargs):
        print('post 함수 실행')
        cat = request.POST.get('cat')
        print(cat)

        catt_pk = CategoryT.objects.filter(name=cat).values('pk')[0]['pk']
        print(catt_pk)
        
        self.object_list = Recipe.objects.filter(categoryTId=catt_pk)
        context = self.get_context_data(**kwargs)
        context['recipe_list'] = Recipe.objects.filter(categoryTId=catt_pk).order_by('pk')
        # print(request.get_host())
        print(request.build_absolute_uri())
        request.path_info = request.build_absolute_uri()[:-3] + str(catt_pk) + '/'
        print(request.path_info)
        # print(context.get('paginator').num_pages)
        return render(request, self.template_name, context)
        #redirect(f'/recipe/category/{catt_pk}')
        # render(request, self.template_name, context)