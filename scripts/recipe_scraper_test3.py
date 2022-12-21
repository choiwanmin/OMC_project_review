import requests
from bs4 import BeautifulSoup
from omc.models import CategoryT, CategoryS, CategoryI, CategoryM

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

def run():
    category1 = []
    category2 = []
    category3 = []
    category4 = []
    for i in items.select('div.cate_list'):
        for n in i.select('a'):
            man_cat = remove_bracket(n.get('href')[25:]).split(',')
            # print(man_cat,n.text)
            if man_cat[0] == 'cat4' and n.text != '전체':
                category1.append([int(man_cat[1]),n.text.strip()])
                # if (CategoryT.objects.filter(index__iexact=int(man_cat[1])).count() == 0):
                #     CategoryT(
                #         index=int(man_cat[1]),
                #         name=n.text.strip()
                #     ).save()
            elif man_cat[0] == 'cat2' and n.text != '전체':
                category2.append([int(man_cat[1]),n.text])
                # if (CategoryS.objects.filter(index__iexact=int(man_cat[1])).count() == 0):
                #     CategoryS(
                #         index=int(man_cat[1]),
                #         name=n.text.strip()
                #     ).save()
            elif man_cat[0] == 'cat3' and n.text != '전체':
                category3.append([int(man_cat[1]),n.text])
                # if (CategoryI.objects.filter(index__iexact=int(man_cat[1])).count() == 0):
                #     CategoryI(
                #         index=int(man_cat[1]),
                #         name=n.text.strip()
                #     ).save()
            elif man_cat[0] == 'cat1' and n.text != '전체':
                category4.append([int(man_cat[1]),n.text])
                # if (CategoryM.objects.filter(index__iexact=int(man_cat[1])).count() == 0):
                #     CategoryM(
                #         index=int(man_cat[1]),
                #         name=n.text.strip()
                #     ).save()
    print('category1 :', len(category1))
    print('category2 :', len(category2))
    print('category3 :', len(category3))
    print('category4 :', len(category4))