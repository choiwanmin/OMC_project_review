import json
import os
from omc.models import Recipe, Ingredient, RecipeOrder, RecipeHashTag


def run():
    all_data={}
    start, end = 1, 1299
    for page in range(start, end+1):
        with open(os.path.abspath(f'./scripts/jsons/page/page{page}.json'),'r', encoding='utf-8') as f:
            json_data = json.load(f)
            if page == 1:
                all_data=json_data
            else:
                all_data['table']['recipe'].extend(json_data['table']['recipe'])
                all_data['table']['ingredient'].extend(json_data['table']['ingredient'])
                all_data['table']['recipe_order'].extend(json_data['table']['recipe_order'])
                all_data['table']['hashtag'].extend(json_data['table']['hashtag'])
            f.close()
        print(f'page{page} finished ---')
    # with open(os.path.abspath(f'./scripts/jsons/page_combined_{start}to{end}_page_recipe.json'),'w', encoding='utf-8') as f:
    #     json.dump(all_data['table']['recipe'], f, ensure_ascii=False, indent=4)
    # with open(os.path.abspath(f'./scripts/jsons/page_combined_{start}to{end}_page_ingredient.json'),'w', encoding='utf-8') as f:
    #     json.dump(all_data['table']['ingredient'], f, ensure_ascii=False, indent=4)
    # with open(os.path.abspath(f'./scripts/jsons/page_combined_{start}to{end}_page_recipe_order.json'),'w', encoding='utf-8') as f:
    #     json.dump(all_data['table']['recipe_order'], f, ensure_ascii=False, indent=4)
    # with open(os.path.abspath(f'./scripts/jsons/page_combined_{start}to{end}_page_hashtag.json'),'w', encoding='utf-8') as f:
    #     json.dump(all_data['table']['hashtag'], f, ensure_ascii=False, indent=4)
    with open(os.path.abspath(f'./scripts/jsons/page_combined_{start}to{end}.json'),'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)