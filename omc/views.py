from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
# from omc.signup_form import UserForm
from django.contrib.auth import authenticate, login
from .models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM, RecipeOrder, Ingredient, RecipeHashTag, UserIngredient, Comment, Icebox
# from .forms import CategoryForm
from django.core.paginator import Paginator
from .forms import CommentForm, UserForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
import boto3, uuid
import env_info
from django.contrib import messages
from OMC_PJT import settings
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q

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
        context['category'] = {
            '종류별' : CategoryT.objects.all(),
            '상황별' : CategoryS.objects.all(),
            '재료별' : CategoryI.objects.all(),
            '방법별' : CategoryM.objects.all(),
        }
        context['pages'] = [1]
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
        context['recipehastags'] = RecipeHashTag.objects.filter(recipeId=context['recipe'].pk)
        context['recipe_order'] = RecipeOrder.objects.filter(recipeId=context['recipe'].pk)
        if context['recipe'].categoryTId != None:
            context['category_t'] = CategoryT.objects.get(pk=context['recipe'].categoryTId_id)
            context['category_s'] = CategoryS.objects.get(pk=context['recipe'].categorySId_id)
            context['category_i'] = CategoryI.objects.get(pk=context['recipe'].categoryIId_id)
            context['category_m'] = CategoryM.objects.get(pk=context['recipe'].categoryMId_id)
        context['comment_form'] = CommentForm
        return context


class RefrigeratorList(TemplateView):
    template_name = 'omc/refrigerator_list_view.html'

    def get(self, request):
        if not request.user.is_anonymous:
            context = self.get_context_data()
            icebox, created = Icebox.objects.get_or_create(userId_id=request.user.id, defaults={'userId': request.user})
            context['icebox'] = icebox
            context['exist_ingredients'] = icebox.userIngredientId.all()
            context['created'] = created
        else:
            return redirect('/login/')
        return render(request, self.template_name, context)

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
            nickname = form.cleaned_data.get('nickname')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(nickname=nickname, password=raw_password)
            if user:
    # 사용자 인증
                login(request, user, backend='django.contrib.auth.backends.ModelBackend') # 로그인
                return redirect('/recipe/refrigerator_list_vue/')
            else:
                return redirect('/login/')
    else:
        form = UserForm()
    return render(request, 'signup_view.html', {'form': form})
    

class RecipeSearch(RecipeList):
    paginate_by = 40

    def get_queryset(self):
        q = self.kwargs['q']

        recipe_queryset = Recipe.objects.filter(name__contains=q)
        irg_queryset = Recipe.objects.filter(ingredient__name__contains=q)
        recipe_order_queryset = Recipe.objects.filter(recipeorder__description__contains=q)
        hashtag_queryset = Recipe.objects.filter(recipehashtag__description__contains=q)
        recipe_queryset = recipe_queryset.union(irg_queryset,recipe_order_queryset,hashtag_queryset).order_by('-viewCount')
        return recipe_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        context['search_word'] = q
        return context
    

class RecipeCategory(RecipeList):
    paginate_by = 40

    def post(self, request, **kwargs):
        current_url = request.build_absolute_uri().split('/')[-2]
        categorys = {
            'categoryTId': request.POST.get('cat1'),
            'categorySId': request.POST.get('cat2'),
            'categoryIId': request.POST.get('cat3'),
            'categoryMId': request.POST.get('cat4'),
        }

        query_dict = {}
        for idx, val in enumerate(categorys.items()):
            key, value = val
            if value is None:
                category_url = current_url[idx*2:(idx*2)+2]
                if category_url != '00':
                    query_dict[key] = int(category_url)
            else:
                query_dict[key] = int(categorys[key])
        
        self.object_list = Recipe.objects.filter(**query_dict)
        context = self.get_context_data(query_dict, **kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, query_dict, **kwargs):
        context = super().get_context_data(**kwargs)
        category_mapping = {'categoryTId':'종류별', 'categorySId':'상황별', 'categoryIId':'재료별', 'categoryMId':'방법별'}
        selected_categorys = {}
        for key, value in query_dict.items():
            if value >= 1:
                selected_categorys[category_mapping[key]] = context['category'][category_mapping[key]][value-1].name
        context['selected_category'] = selected_categorys
        return context

class RecipeRecommend(ListView):
    model = Recipe
    template_name = 'omc/recipe_recommend.html'
    enc = settings.ENCODER
    one_hot_vec = settings.ONE_HOT_MATRIX

    def get(self, request, **kwargs):
        self.object_list = Recipe.objects.all()
        if request.user.is_authenticated:
            try:
                icebox = Icebox.objects.get(userId_id=request.user.id)
                user_ingredients = icebox.userIngredientId.all()
                user_inputs = [ user_ingr.name for user_ingr in user_ingredients ]
                context = self.get_context_data(user_inputs=user_inputs)
                context['icebox_exist'] = True
                context['icebox_ingr'] = (len(user_ingredients) > 0)
            except Exception as e:
                context = self.get_context_data()
                context['icebox_exist'] = False
                context['icebox_ingr'] = False
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        user_inputs = request.POST.get('selected').split(',')
        if user_inputs == ['']:
            user_inputs = []
            icebox_ingr = False
        if not request.user.is_anonymous:
            icebox = Icebox.objects.get(userId_id=request.user.id)
            icebox.userIngredientId.clear()
            for input in user_inputs:
                try:
                    input_ing = UserIngredient.objects.get(name=input)
                    icebox.userIngredientId.add(input_ing)
                    icebox_ingr = True
                except:
                    icebox_ingr = False
        self.object_list = Recipe.objects.all()
        context = self.get_context_data(user_inputs=user_inputs)
        context['icebox_exist'] = True
        context['icebox_ingr'] = icebox_ingr
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(RecipeRecommend, self).get_context_data(**kwargs)
        spring = Recipe.objects.filter(recipehashtag__description__contains='봄').distinct().order_by('-viewCount')
        summer = Recipe.objects.filter(recipehashtag__description__contains='여름').distinct().order_by('-viewCount')
        autumn = Recipe.objects.filter(recipehashtag__description__contains='가을').distinct().order_by('-viewCount')
        winter = Recipe.objects.filter(recipehashtag__description__contains='겨울').distinct().order_by('-viewCount')
        context['seasons'] = {
            '봄' : spring,
            '여름' : summer,
            '가을' : autumn,
            '겨울' : winter,
        }
        baby = Recipe.objects.filter(
            Q(recipehashtag__description__contains='아이') | Q(recipehashtag__description__contains='아기')
            ).distinct().order_by('-viewCount')
        all_recipe = Recipe.objects.all().count() - baby.count()
        context['baby_chart'] = { 
            '아이' : baby.count(),
            '기타' : all_recipe
            }
        context['baby'] = baby

        if kwargs.get('user_inputs') is not None and len(kwargs.get('user_inputs')) > 0:
            keys = self.get_recommendations(kwargs['user_inputs'], limit=50)
            context['recommend'] = self.get_filtered_recommendations(keys)
        return context

    def get_recommendations(self, ingt, enc=enc, limit=20):
        user_input = pd.DataFrame(ingt,columns=['new_ing'])
        input_temp = enc.transform(user_input).toarray().sum(axis=0)
        cos = cosine_similarity(self.one_hot_vec['vector'].tolist(), input_temp.reshape(1,-1))
        cos_idx = list(enumerate(cos))
        cos_idx.sort(key=lambda x: x[1], reverse=True)
        result = self.one_hot_vec.iloc[[i[0] for i in cos_idx[:limit]],:2]
        return result['id'].tolist()
    
    def get_filtered_recommendations(self, keys):
        recipe_list = Recipe.objects.filter(id__in=keys)
        categoryT_list = list(recipe_list.values_list('categoryTId',flat=True).distinct())
        recipe_list = list(recipe_list)
        recipe_list.sort(key=lambda recipe: keys.index(recipe.id))
        recommend_list = []
        for recipe in recipe_list:
            if recipe.categoryTId_id in categoryT_list:
                recommend_list.append(recipe)
                categoryT_list.remove(recipe.categoryTId_id)
        for recipe in recipe_list:
            if len(recommend_list) >= 10:
                break
            if recipe not in recommend_list:
                recommend_list.append(recipe)
        return recommend_list

class NewComment(TemplateView):
    template_name = 'new_comment'
    s3_client = boto3.client(
                    's3',
                    aws_access_key_id=env_info.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=env_info.AWS_SECRET_ACCESS_KEY
                )
    
    def post(self,request, pk):
        if request.user.is_authenticated:
            recipe = get_object_or_404(Recipe, pk=pk)
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment_form.cleaned_data['recipeId'] = recipe
                comment_form.cleaned_data['userId'] = request.user
                comment = comment_form.save(commit=True)
                # comment.recipeId = recipe
                # comment.userId = request.user
                # print(comment)
                # comment.save()
                
                return redirect(recipe.get_absolute_url())
            else:
                messages.warning(request, '올바른 파일 형식을 업로드해 주세요')
                return redirect(recipe.get_absolute_url())
        else:
            raise PermissionDenied

class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().userId:
            return super(UpdateComment, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    recipe = comment.recipeId
    if request.user.is_authenticated and request.user == comment.userId:
        comment.delete()
        return redirect(recipe.get_absolute_url())
    else:
        raise PermissionDenied


def alert_message(request, message):
    messages.warning(request, message)
