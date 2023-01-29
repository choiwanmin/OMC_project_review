import json
import os
from omc.models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM


def run():
    categoryT = CategoryT.objects.all()
    categoryS = CategoryS.objects.all()
    categoryI = CategoryI.objects.all()
    for catT in categoryT:
        for catS in categoryS:
            for catI in categoryI:
                if os.path.isfile(f'./scripts/jsons/category/catT{catT.index}-catS{catS.index}-catI{catI.index}.json'):
                    with open(os.path.abspath(f'./scripts/jsons/category/catT{catT.index}-catS{catS.index}-catI{catI.index}.json'),'r', encoding='utf-8') as f:
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
                        print(f'catT{catT.index}-catS{catS.index}-catI{catI.index} finished---')