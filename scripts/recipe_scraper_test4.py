import requests
from bs4 import BeautifulSoup
from omc.models import Recipe,CategoryT, CategoryS, CategoryI, CategoryM
import json
file_path = 'C:\recipe_pjt'

def run():
    categoryT = CategoryT.objects.all()
    categoryS = CategoryS.objects.all()
    categoryI = CategoryI.objects.all()
    categoryM = CategoryM.objects.all()
    data = {}
    data['update_keys'] = []
    for catT in categoryT:
        for catS in categoryS:
            for catI in categoryI:
                for catM in categoryM:
                    url = f'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&order=date&page=1'
                    res = requests.get(url)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    page = 1

                    while soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a'):
                        url = f'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&order=date&page={page}'
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        items = soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a')
                        idx = 0
                        for item in items:
                            recipe_link = item.get('href').strip()
                            recipe_link = recipe_link.split('/')[-1]
                            recipe = Recipe.objects.filter(mangaeId__iexact=recipe_link)
                            # print(recipe_link)
                            # print(Recipe.objects.get(mangaeId='6843136').name)
                            data['update_keys'].append(
                            {
                                'recipe_pk' : Recipe.objects.all()[idx].pk,
                                'categoryTId' : catT.pk,
                                'categorySId' : catS.pk,
                                'categoryIId' : catI.pk,
                                'categoryMId' : catM.pk,
                            })
                            print(data)
                            idx+=1
                            if idx == 2:
                                break
                            # if recipe:
                            #     recipe.update(categoryTId=catT,categorySId=catS, categoryIId=catI, categoryMId=catM)
                        # page += 1
                        # else:
                        #     print('검색결과가 없습니다.')
                        break
                    break
                print(f'category I : {catI.index} 종료')
                break
    #       print(f'category S : {catS.index} 종료')
            break
        # with open(file_path, 'w') as outfile:
        #     json.dump(data, outfile)
    #   print(f'category T : {catT.index} 종료')
        break




 

# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=&cat4=&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=&cat4=63&fct=&order=reco&lastcate=cat1&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=

# 레시피 카테고리가 비어있는 url
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=42&cat2=22&cat3=34&cat4=54&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=

# 레시피 카테고리 페이지 넘기기 확인용 url
# https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=6&cat2=12&cat3=71&cat4=63&fct=&order=reco&lastcate=cat1&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource=
# https://www.10000recipe.com/recipe/list.html?cat1=6&cat2=12&cat3=71&cat4=63&order=reco&page=2
# https://www.10000recipe.com/recipe/list.html?cat1=6&cat2=12&cat3=71&cat4=63&order=reco&page=3

# https://www.10000recipe.com/recipe/list.html?cat1=7&cat2=12&cat3=71&cat4=63&order=reco&page=2