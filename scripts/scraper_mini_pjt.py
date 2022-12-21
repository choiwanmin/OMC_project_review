import requests
from bs4 import BeautifulSoup

url = "https://www.10000recipe.com/recipe/6994051"
res = requests.get(url)
soup = BeautifulSoup(res.text,"html.parser")
# print(soup)
# alpha = soup.select("div.list0")
# print(alpha)

items = soup.select("#contents_area")

for item in items :
    #썸네일 이미지
    image = item.select('div.view2_pic div.centeredcrop img')[0].get("src").strip()
    # print(image)
    
    #요리 설명
    explain = item.select('div.view2_summary_in')[0].text.strip() 
    # print(explain)
    
    #음식 양, 조리 시간, 조리 난이도
    mini_info_1 = item.select('span.view2_summary_info1')[0].text.strip()
    mini_info_2 = item.select('span.view2_summary_info2')[0].text.strip()
    mini_info_3 = item.select('span.view2_summary_info3')[0].text.strip()

    #상세 재료
    lst = []
    #재료 명
    # ingredient_name = []
    #재료 단위
    # ingredient_unit = []
    # for i in range(len(item.select('div.ready_ingre3 ul'))):
    #     ingredient = item.select('div.ready_ingre3 ul')[i].text.replace("구매"," ").replace(' ','').split()

        # ingredient_name.append(ingredient[0])
        # ingredient_unit.append(ingredient[1])
        # print(ingredient_unit)
    ingredient_category = []
    ingredient_name = []
    #재료 단위
    ingredient_unit = []

    ingredient_ul = item.select('div.ready_ingre3 ul')
    for i in ingredient_ul:
        for n in range(len(i.select('li'))):
            ingredient_category.append(i.select('b')[0].text.strip())
            ingredient_li = i.select('li')[n].text.replace("구매"," ").replace(' ','').split()
            ingredient_name.append(ingredient_li[0])
            if len(ingredient_li) == 2 :
                ingredient_unit.append(ingredient_li[1])
            else : 
                ingredient_unit.append('적당량')

    print(ingredient_unit)

    #조리순서 - 조리순서 사진
    recipe_sequence = []
    recipe_thumbnail = []
    # recipe_sequence = item.select('div.view_step #stepDiv1')[0].text.strip()
    for i in range(len(item.select('div.view_step div.view_step_cont.media'))):
        recipe = item.select('div.view_step div.view_step_cont.media')[i].text.strip()
        thumbnail = item.select(f'div.view_step div.view_step_cont.media.step{i+1} img')[0].get('src').strip()
        recipe_sequence.append(recipe)
        recipe_thumbnail.append(thumbnail)

    if item.select('div.view_step div.view_tag'):
        hash_tag = item.select('div.view_step div.view_tag')[0].text.replace(" ","").strip().split('#')[1:]
    else:
        hash_tag = None
    print(hash_tag)