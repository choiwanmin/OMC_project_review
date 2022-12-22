import json
import os
from omc.models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM


def run():
    with open(os.path.abspath(f'./scripts/jsons/catT1.json'),'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for keys in json_data['update_keys']:
            recipe = Recipe.objects.filter(mangaeId__iexact=keys['mangaeId'])
            recipe.update(
                categoryTId=CategoryT.objects.get(index=keys['categoryTId']),
                categorySId=CategoryS.objects.get(index=keys['categorySId']),
                categoryIId=CategoryI.objects.get(index=keys['categoryIId']),
                categoryMId=CategoryM.objects.get(index=keys['categoryMId']),
            )
        f.close()