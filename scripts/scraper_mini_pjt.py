import requests
from bs4 import BeautifulSoup

url = "https://www.10000recipe.com/recipe/6963110"
res = requests.get(url)
soup = BeautifulSoup(res.text,"html.parser")
# print(soup)
# alpha = soup.select("div.list0")
# print(alpha)

items = soup.select("#contents_area")
# print(items)
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
    
    #재료
    ingredients = item.select('b.ready_ingre3_tt')[0].text.strip()
    # cook_steps = item.select('div.besttit')[0].text.strip()
    # print(cook_steps)

    #상세 재료
    #재료 명
    ingredient_name = []
    #재료 단위
    ingredient_unit = []
    for i in range(len(item.select('div.ready_ingre3 ul li'))):
        ingredient = item.select('div.ready_ingre3 ul li')[i].text.replace("구매"," ").replace(' ','').split()
        ingredient_name.append(ingredient[0])
        ingredient_unit.append(ingredient[1])

    #조리순서 - 조리순서 사진
    recipe_sequence = []
    recipe_thumbnail = []
    # recipe_sequence = item.select('div.view_step #stepDiv1')[0].text.strip()
    for i in range(len(item.select('div.view_step div.view_step_cont.media'))):
        recipe = item.select('div.view_step div.view_step_cont.media')[i].text.strip()
        thumbnail = item.select(f'div.view_step div.view_step_cont.media.step{i+1} img')[0].get('src').strip()
        recipe_sequence.append(recipe)
        recipe_thumbnail.append(thumbnail)
    
    hash_tag = item.select('div.view_step div.view_tag')[0].text.replace(" ","").strip().split('#')[1:]
    print(hash_tag)