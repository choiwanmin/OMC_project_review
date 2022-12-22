import requests
from bs4 import BeautifulSoup
from omc.models import Recipe,CategoryT, CategoryS, CategoryI, CategoryM
import json
import os
from user_agent import generate_user_agent
import time


def run():
    categoryT = CategoryT.objects.all()
    categoryS = CategoryS.objects.all()
    categoryI = CategoryI.objects.all()
    categoryM = CategoryM.objects.all()
    timeout = 5
    for catT in categoryT:
        if catT.pk==1:
            continue
        data = {}
        data['update_keys'] = []
        for catS in categoryS:
            for catI in categoryI:
                if catT.pk ==1 and catS.pk == 1 and catI.pk <= 4:
                    continue
                for catM in categoryM:
                    url = f'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&order=date&page=1'
                    res = requests.get(url, timeout=timeout)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    items = soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a')
                    page = 1
                    while len(soup.select('#contents_area_full ul div.result_none')) == 0:
                        try:
                            if page >= 2:
                                headers = {'User-Agent' : generate_user_agent(os='win', device_type='desktop')}
                                url = f'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&order=date&page={page}'
                                res = requests.get(url, timeout=timeout, headers=headers)
                                soup = BeautifulSoup(res.text, 'html.parser')
                                items = soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a')
                                
                            for item in items:
                                recipe_link = item.get('href').strip()
                                recipe_link = recipe_link.split('/')[-1]
                                recipe = Recipe.objects.filter(mangaeId__iexact=recipe_link)
                                # print(recipe_link)
                                # print(Recipe.objects.get(mangaeId='6843136').name)
                                data['update_keys'].append(
                                {
                                    'mangaeId' : recipe_link,
                                    'categoryTId' : catT.index,
                                    'categorySId' : catS.index,
                                    'categoryIId' : catI.index,
                                    'categoryMId' : catM.index,
                                })
                                if recipe:
                                    recipe.update(categoryTId=catT,categorySId=catS, categoryIId=catI, categoryMId=catM)
                            page += 1
                        except requests.exceptions.ConnectTimeout as e:
                            print('connection timeout ...')
                            timeout += 1
                            time.sleep(5)
                            print('====restart====')
                            continue
                        except requests.exceptions.ConnectionError as e:
                            print("connection aborted by the server ..")
                            time.sleep(5)
                            print("====restart====")
                            continue
                        except Exception as e :
                            print('error occured ...')
                            time.sleep(5)
                            print("===restart===")
                            continue

                    # print(f'category M : {catM.index} 종료')
                print(f'category I : {catI.index} 종료')
            print(f'category S : {catS.index} 종료')
        print(f'category T : {catT.index} 종료')
        with open(os.path.abspath(f'./scripts/jsons/catT{catT.pk}.json'),'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)




 

# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=&cat4=&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=&cat4=63&fct=&order=reco&lastcate=cat1&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=

# 레시피 카테고리가 비어있는 url
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=42&cat2=22&cat3=34&cat4=54&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=

# 레시피 카테고리 페이지 넘기기 확인용 url
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=6&cat2=12&cat3=71&cat4=63&fct=&order=reco&lastcate=cat1&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=
# https://www.10000recipe.com/recipe/list.html?cat1=6&cat2=12&cat3=71&cat4=63&order=reco&page=2
# https://www.10000recipe.com/recipe/list.html?cat1=6&cat2=12&cat3=71&cat4=63&order=reco&page=3

# https://www.10000recipe.com/recipe/list.html?cat1=7&cat2=12&cat3=71&cat4=63&order=reco&page=2