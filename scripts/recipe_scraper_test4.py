import requests
from bs4 import BeautifulSoup
from omc.models import Recipe,CategoryT, CategoryS, CategoryI, CategoryM

# url = 'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1=&cat2=&cat3=&cat4=&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource='
# res = requests.get(url)
# soup = BeautifulSoup(res.text, 'html.parser')
# items = soup.select_one('#id_search_category table tbody tr td div.rcp_cate.st3')
# items = soup.select_one('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a')
def run():
    # 해당 카테고리에 있는 레시피의 Id
    # recipe_link = items.get('href').strip()
    # recipe_link = recipe_link.split('/')[-1]
    # print(recipe_link)
    # Db에 저장되어 있는 mangaeId
    categoryT = CategoryT.objects.all()
    categoryS = CategoryS.objects.all()
    categoryI = CategoryI.objects.all()
    categoryM = CategoryM.objects.all()
    for catT in categoryT:
        for catS in categoryS:
            for catI in categoryI:
                for catM in categoryM:
                    url = f'https://www.10000recipe.com/recipe/list.html?q=&query=&cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&fct=&order=reco&lastcate=cat4&dsearch=&copyshot=&scrap=&degree=&portion=&time=&niresource='
                    res = requests.get(url)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    
                    url_lst = []
                    while soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a'):
                        url_lst.append(url)
                        url = f'https://www.10000recipe.com/recipe/list.html?cat1={catM.index}&cat2={catS.index}&cat3={catI.index}&cat4={catT.index}&order=reco&page={len(url_lst)+1}'
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')

                    for url in url_lst:
                        url = url
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        if soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a'):
                            items = soup.select('#contents_area_full ul ul li.common_sp_list_li div.common_sp_thumb a')
                            for item in items:
                                recipe_link = item.get('href').strip()
                                recipe_link = recipe_link.split('/')[-1]

                                recipe = Recipe.objects.filter(mangaeId__iexact=recipe_link)
                                if recipe:
                                    recipe.update(categoryTId=catT,categorySId=catS, categoryIId=catI, categoryMId=catM)
                                    
                        else:
                            print('검색결과가 없습니다.')
                    break
    #           print(f'category I : {catI.index} 종료')
                break
    #       print(f'category S : {catS.index} 종료')
            break
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