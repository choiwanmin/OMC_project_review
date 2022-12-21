import json
import os
from omc.models import Recipe, Ingredient, RecipeOrder, RecipeHashTag


def run():
    with open(os.path.abspath(f'./scripts/jsons/page1.json'),'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for recipe in json_data['table']['recipe']:
            Recipe(**recipe).save()
        for ingredients in json_data['table']['ingredient']:
            for i in ingredients:
                i['recipeId'] = Recipe.objects.get(mangaeId=i['recipeId'])
                Ingredient(**i).save()
        for recipe_orders in json_data['table']['recipe_order']:
            for ro in recipe_orders:
                ro['recipeId'] = Recipe.objects.get(mangaeId=ro['recipeId'])
                RecipeOrder(**ro).save()
        for hashtags in json_data['table']['hashtag']:
            for ht in hashtags:
                ht['recipeId'] = Recipe.objects.get(mangaeId=ht['recipeId'])
                RecipeHashTag(**ht).save()
        f.close()