# from django.shortcuts import render
from omc.models import Recipe, Ingredient
# from django.conf import settings
import os
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import OneHotEncoder


def get_one_hot_encoder():
    data_recp = Recipe.objects.filter(id__lt=20000).values_list('id','name')
    data_irdn = Ingredient.objects.filter(recipeId_id__lt=20000).values_list('name','recipeId_id')
    df_recp = pd.DataFrame.from_records(data=data_recp,columns=['id','recipe_name'])
    df_irdn = pd.DataFrame.from_records(data=data_irdn, columns=['name','recipeId'])
    df_join = pd.merge(df_irdn,df_recp, how='left', left_on='recipeId', right_on='id')
    scriptpath = os.path.dirname(__file__)
    with open(os.path.join(scriptpath,'./mapping.json'), 'r', encoding='utf-8') as f:
        map = json.load(f)
    df_join['new_ing'] = [map.get(n) for n in df_join['name']]
    df_join = df_join.loc[df_join['new_ing'].notna()].reset_index()
    
    cols = ['new_ing']
    enc = OneHotEncoder()
    tmp = pd.DataFrame(
        enc.fit_transform(df_join[cols]).toarray(),
        columns = enc.get_feature_names_out()
    )
    features = pd.concat([df_join,tmp],axis=1)
    columns = features.columns[6:]
    one_hot_df = features.groupby(['id','recipe_name'])[columns].sum().reset_index()
    one_hot_df = one_hot_df.set_index('id', drop=False)
    one_hot_df['vector'] = one_hot_df[columns].values.tolist()
    one_hot_vec = one_hot_df.loc[:,['id','vector']]
    
    return enc, one_hot_vec