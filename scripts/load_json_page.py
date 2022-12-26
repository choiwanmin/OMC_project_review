import json
import os
from omc.models import Recipe, Ingredient, RecipeOrder, RecipeHashTag


def run():
    for page in range(1,201):
        with open(os.path.abspath(f'./scripts/jsons/page/page{page}.json'),'r', encoding='utf-8') as f:
            json_data = json.load(f)
            for recipe in json_data['table']['recipe']:
                if Recipe.objects.filter(mangaeId__iexact=recipe['mangaeId']).count() == 0:
                    Recipe(**recipe).save()
            for ingredients in json_data['table']['ingredient']:
                if ingredients and Ingredient.objects.filter(recipeId=Recipe.objects.get(mangaeId=ingredients[0]['recipeId'])).count() == 0:
                    for i in ingredients:
                        i['recipeId'] = Recipe.objects.get(mangaeId=i['recipeId'])
                        Ingredient(**i).save()
            for recipe_orders in json_data['table']['recipe_order']:
                if recipe_orders and RecipeOrder.objects.filter(recipeId=Recipe.objects.get(mangaeId=recipe_orders[0]['recipeId'])).count() == 0:
                    for ro in recipe_orders:
                            ro['recipeId'] = Recipe.objects.get(mangaeId=ro['recipeId'])
                            RecipeOrder(**ro).save()
            for hashtags in json_data['table']['hashtag']:
                if hashtags and RecipeHashTag.objects.filter(recipeId=Recipe.objects.get(mangaeId=hashtags[0]['recipeId'])).count() == 0:
                    for ht in hashtags:
                        if len(ht['description'].encode('utf-8'))>30:
                            continue
                        ht['recipeId'] = Recipe.objects.get(mangaeId=ht['recipeId'])
                        RecipeHashTag(**ht).save()
            f.close()
        print(f'page{page} finished ---')