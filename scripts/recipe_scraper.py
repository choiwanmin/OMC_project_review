import requests
from bs4 import BeautifulSoup
from omc.models import Recipe,Ingredient,RecipeOrder,RecipeHashTag
import json
import os
from user_agent import generate_user_agent
import time
import traceback

res = requests.get("https://www.10000recipe.com/recipe/list.html", timeout=3)

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

def remove_bracket(text):
    text = list(text)
    result = ''
    for i in text:
        if i != '[' and i != ']':
            result += i
    return result


def soup_element_none(soup, selector, name):
    soup_element = soup.select(selector)
    elements_dict = {
        'None': None,
        '0_text_strip': lambda s: s[0].text.strip(),
        'rep_split': lambda s: s[0].text.replace(" ","").strip().split('#')[1:],
        '0_src_strip': lambda s: s[0].get('src').strip(),
    }
    if soup_element:
        return elements_dict[name](soup_element)
    else:
        return elements_dict['None']

def json_default(value):
    if isinstance(value, Recipe):
        return value.mangaeId

def run():
    page_num = 1
    while True:
        if os.path.isfile(f'./scripts/jsons/page/page{page_num}.json'):
            page_num += 1
            continue
        json_index = 0
        error_json = {}
        error_json['error_type'] = []
        error_json['error_recipe'] = []
        error_json['traceback'] = []
        error_json['error_recipe_mid'] = []
        page_json = {}
        page_json['table'] = {}
        page_json['table']['recipe'] = []
        page_json['table']['ingredient'] = []
        page_json['table']['recipe_order'] = []
        page_json['table']['hashtag'] = []
        res = requests.get(f"https://www.10000recipe.com/recipe/list.html?order=reco&page={page_num}")
        soup = BeautifulSoup(res.text, 'html.parser')
        if len(soup.select('#contents_area_full ul div.result_none')) != 0:
            break
        items = soup.select('#contents_area_full ul ul li.common_sp_list_li')
        for item in items:
            try:
                data = {}
                # 게시물 링크
                recipe_link = item.select('div.common_sp_thumb a')[0].get('href').strip()
                recipe_link = recipe_link.split('/')[-1] # 만개의레시피 아이디, int로 DB에 저장
                data['mangaeId'] = recipe_link
                recipe_link = 'https://www.10000recipe.com/recipe/' + recipe_link
                data['link'] = recipe_link

                # 레시피 타이틀
                recipe_title = item.select('div.common_sp_caption div.common_sp_caption_tit.line2')[0].text.strip()
                data['name'] = recipe_title                                 
                #------------------상세페이지-----------------------#
                headers = {'User-Agent' : generate_user_agent(os='win', device_type='desktop')}
                res = requests.get(recipe_link, timeout=5, headers=headers)
                soup = BeautifulSoup(res.text,"html.parser")

                detail = soup.select("#contents_area")[0]
                recipe_sequence_length = len(detail.select('div.view_step div.view_step_cont.media'))

                if recipe_sequence_length == 0:
                    continue

                #썸네일 이미지
                image = detail.select('div.view2_pic div.centeredcrop img')[0].get("src").strip()
                data['thumbnail'] = image
                
                #요리 설명
                explain = soup_element_none(detail, 'div.view2_summary_in', '0_text_strip')
                data['description'] = explain
                
                #음식 양, 조리 시간, 조리 난이도
                cook_amount = soup_element_none(detail, 'span.view2_summary_info1', '0_text_strip')
                data['amount'] = cook_amount
                cook_time = soup_element_none(detail, 'span.view2_summary_info2' ,'0_text_strip')
                data['time'] = cook_time
                cook_level= soup_element_none(detail, 'span.view2_summary_info3' ,'0_text_strip')
                data['level'] = cook_level

                #상세 재료
                # 재료 카테고리, 재료 명, 재료 단위
                ingredient_category = [] 
                ingredient_name = []
                ingredient_unit = []
                ingredient_ul = detail.select('div.ready_ingre3 ul')
                for i in ingredient_ul:
                    for n in range(len(i.select('li'))):
                        ingredient_category.append(remove_bracket(i.select('b')[0].text.strip()))
                        ingredient_li = i.select('li')[n].text.replace("구매"," ").replace(' ','').split()
                        ingredient_name.append(ingredient_li[0])
                        if len(ingredient_li) == 2:
                            ingredient_unit.append(ingredient_li[1])
                        else:
                            ingredient_unit.append('적당량')

                # 조리순서 - 조리순서 사진
                recipe_sequence = []
                recipe_thumbnail = []
                for i in range(recipe_sequence_length):
                    recipe = detail.select('div.view_step div.view_step_cont.media')[i].text.strip()
                    thumbnail = soup_element_none(detail, f'div.view_step div.view_step_cont.media.step{i+1} img', '0_src_strip')
                    recipe_sequence.append(recipe)
                    recipe_thumbnail.append(thumbnail)

                hash_tag = soup_element_none(detail, 'div.view_step div.view_tag', 'rep_split')

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
                
                data['star'] = star

                # 리뷰 갯수
                if item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_ea'):
                    review_count = item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_rv_ea')[0].text.strip()
                    review_count = int_in_str(review_count)
                else:
                    review_count = 0
                data['reviewCount'] = review_count

                if item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_buyer'):
                    views_count = item.select('div.common_sp_caption div.common_sp_caption_rv span.common_sp_caption_buyer')[0].text.strip()
                    views_count = views_count.split(' ')[-1]
                    views_count = int_in_str(views_count)
                else:
                    views_count = 0
                data['viewCount'] = views_count

                if Recipe.objects.filter(link__iexact=recipe_link).count() == 0:
                    Recipe(**data).save()
                page_json['table']['recipe'].append(data)
                page_json['table']['ingredient'].append([])
                page_json['table']['recipe_order'].append([])
                page_json['table']['hashtag'].append([])

                recipe = Recipe.objects.filter(link__iexact=recipe_link)[0]
                # recipe = Recipe.objects.get(link=recipe_link)
                
                if Ingredient.objects.filter(recipeId=recipe).count() == 0:
                    for idx in range(len(ingredient_category)):
                        igrnt = {
                            'type': ingredient_category[idx],
                            'name': ingredient_name[idx],
                            'volume': ingredient_unit[idx],

                            'recipeId': recipe,
                        }
                        Ingredient(**igrnt).save()
                        page_json['table']['ingredient'][json_index].append(igrnt)

                if RecipeOrder.objects.filter(recipeId=recipe).count() == 0:
                    for i in range(recipe_sequence_length):
                        order = {
                            'number': i+1,
                            'description': recipe_sequence[i],
                            'thumbnail': recipe_thumbnail[i],
                            'recipeId': recipe,
                        }
                        RecipeOrder(**order).save()
                        page_json['table']['recipe_order'][json_index].append(order)

                if hash_tag != None:
                    if RecipeHashTag.objects.filter(recipeId=recipe).count() == 0:
                        for i in hash_tag:
                            if len(i.encode('utf-8'))>30:
                                continue
                            hash_tag = {
                                'description':i,
                                'recipeId':recipe,
                            }
                            RecipeHashTag(**hash_tag).save()
                            page_json['table']['hashtag'][json_index].append(hash_tag)
                json_index += 1
            except IndexError as e:
                print(e)
                print(recipe_title)
                error_json['error_type'].append(e)
                error_json['error_recipe'].append(recipe_title)
                error_json['error_recipe_mid'].append(recipe_link)
                error_json['traceback'].append(traceback.format_exc())
                json_index = len(page_json['table']['ingredient'])
            except requests.exceptions.ConnectionError as e:
                error_json['error_type'].append(e)
                error_json['error_recipe'].append(recipe_title)
                error_json['error_recipe_mid'].append(recipe_link)
                error_json['traceback'].append('')
                print("connection aborted by the server ..")
                time.sleep(5)
                print("====restart====")
                continue
            except Exception as e:
                print(e)
                print(recipe_title)
                error_json['error_type'].append(e)
                error_json['error_recipe'].append(recipe_title)
                error_json['error_recipe_mid'].append(recipe_link)
                error_json['traceback'].append(traceback.format_exc())
                json_index += 1
                
        with open(os.path.abspath(f'./scripts/jsons/page/page{page_num}.json'),'w', encoding='utf-8') as f:
            json.dump(page_json, f, ensure_ascii=False, indent=4, default=json_default)
        with open(os.path.abspath(f'./scripts/jsons/page/page{page_num}_error.json'),'w', encoding='utf-8') as f:
            json.dump(error_json, f, ensure_ascii=False, indent=4, default=json_default)
        page_num += 1
                    