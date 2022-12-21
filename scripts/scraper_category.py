import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.10000recipe.com/recipe/list.html")
soup = BeautifulSoup(res.text, 'html.parser')
items = soup.select_one('#id_search_category table tbody tr td div.rcp_cate.st3')

def remove_bracket(text):
    text = list(text)
    result = ''
    for i in text:
        if i != '(' and i != ')' and i != "'":
            result += i
    return result

category1 = []
category2 = []
category3 = []
category4 = []

def run():
    for i in items.select('div.cate_list'):
        for n in i.select('a'):
            man_cat = remove_bracket(n.get('href')[25:]).split(',')
            if man_cat[1] != "" and n.text != "전체":
                category1.append([man_cat[1],n.text])
                print(category1)