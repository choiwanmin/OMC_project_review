import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.10000recipe.com/recipe/list.html")

soup = BeautifulSoup(res.text, 'html.parser')

items = soup.select('#contents_area_full ul ul li.common_sp_list_li')

def int_in_str(text):
    if '만' in text:
        return int(float(text[:-1]) * 10000)
    else:
        text = list(text)
        result = ''
        for x in text:
            if x.isdigit() == True:
                result += x
        return int(result)

def run():
    for item in items:
        # 게시물 링크
        recipe_link = item.select('div.common_sp_thumb a')[0].get('href').strip()
        recipe_link = recipe_link.split('/')[-1]
        recipe_link = 'https://www.10000recipe.com/recipe/' + recipe_link

        # 레시피 타이틀
        recipe_title = item.select('div.common_sp_caption div.common_sp_caption_tit.line2')[0].text.strip()
        
        #------------------상세페이지-----------------------#
        res = requests.get(recipe_link)
        soup = BeautifulSoup(res.text,"html.parser")

        details = soup.select("#contents_area")

        for detail in details :
            #썸네일 이미지
            image = detail.select('div.view2_pic div.centeredcrop img')[0].get("src").strip()
            print(image)
            
            #요리 설명
            explain = detail.select('div.view2_summary_in')[0].text.strip() 
            print(explain)
            
            #음식 양, 조리 시간, 조리 난이도
            cook_amount = detail.select('span.view2_summary_info1')[0].text.strip()
            cook_time = detail.select('span.view2_summary_info2')[0].text.strip()
            cook_level = detail.select('span.view2_summary_info3')[0].text.strip()
            print(cook_amount)        
            print(cook_time)        
            print(cook_level)        

            #상세 재료
            #재료 명
            ingredient_name = []
            #재료 단위
            ingredient_unit = []
            for i in range(len(detail.select('div.ready_ingre3 ul li'))):
                ingredient = detail.select('div.ready_ingre3 ul li')[i].text.replace("구매"," ").replace(' ','').split()
                ingredient_name.append(ingredient[0])
                ingredient_unit.append(ingredient[1])
            print(ingredient_name)
            print(ingredient_unit)

            #조리순서 - 조리순서 사진
            recipe_sequence = []
            recipe_thumbnail = []
            for i in range(len(item.select('div.view_step div.view_step_cont.media'))):
                recipe = detail.select('div.view_step div.view_step_cont.media')[i].text.strip()
                thumbnail = detail.select(f'div.view_step div.view_step_cont.media.step{i+1} img')[0].get('src').strip()
                recipe_sequence.append(recipe)
                recipe_thumbnail.append(thumbnail)
            print(recipe_sequence)
            print(recipe_thumbnail)
            
            hash_tag = detail.select('div.view_step div.view_tag')[0].text.replace(" ","").strip().split('#')[1:]
            print(hash_tag)

        # 별점
        if item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_star img'):
            star = item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_star img')
            star_count = 0
            for s in star:
                if s.get('src')[-5].strip().isdigit() == False:
                    star_count += 1
                    star = float(star_count)
        else:
            star = 0

        # 리뷰 갯수
        if item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_ea'):
            review_count = item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_ea')[0].text.strip()
            review_count = int_in_str(review_count)
        else:
            review_count = 0

        if item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_buyer'):
            views_count = item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_buyer')[0].text.strip()
            views_count = views_count.split(' ')[-1]
            views_count = int_in_str(views_count)
        else:
            views_count = 0

        # print(recipe_link)
        # print(recipe_title)
        # print(star)
        # print(review_count)
        # print(views_count)