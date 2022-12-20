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
        
        for :
            res = requests.get(recipe_link)
            soup = BeautifulSoup(res.text, 'html.parser')

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


        print(recipe_link)
        print(recipe_title)
        print(star)
        print(review_count)
        print(views_count)
