from elasticsearch import Elasticsearch
import json
from omc.models import Recipe, RecipeOrder, RecipeHashTag, Ingredient
import requests

def run():
    # es = Elasticsearch(hosts=[{'host': '127.0.0.1', 'port':9200, 'scheme': 'https'}], http_auth=('elastic','elastic'))
    es = Elasticsearch(['127.0.0.1'], http_auth=('elastic', 'elastic'), scheme='https', port=9200)
    print(es.indices.exists(index='dictionary')) # -> 이게 문제임..
    # if es.indices.exists(index='dictionary'):
    #     pass
    # else:
        # es.indices.create(
        #     index='dictionary',
        #     body= {
        #         "settings": {
        #             "index": {
        #                 "analysis": {
        #                     "analyzer": {
        #                         "korean_analyzer": {
        #                             "type": "custom",
        #                             "tokenizer": "nori_tokenizer"
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #         "mappings": {
        #             "properties": {

        #             }
        #         }
        #     }
        # )
    recipes = Recipe.objects.filter(id__lte=20000)
    recipe_orders = RecipeOrder.objects.filter(recipeId__lte=20000)
    recipe_hashtags = RecipeHashTag.objects.filter(recipeId__lte=20000)
    ingredients = Ingredient.objects.filter(recipeId__lte=20000)
    print(recipes)