import json
import os
from omc.models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM


def run():
    with open(os.path.abspath(f'./scripts/jsons/catT1.json'),'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for keys in json_data['update_keys']:
            recipe = Recipe.objects.filter(mangaeId__iexact=keys['mangaeId'])
            recipe.update(
                categoryTId=CategoryT.objects.get(pk=keys['categoryTId']),
                categorySId=CategoryS.objects.get(pk=keys['categorySId']),
                categoryIId=CategoryI.objects.get(pk=keys['categoryIId']),
                categoryMId=CategoryM.objects.get(pk=keys['categoryMId']),
            )
        f.close()