# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:52:46 2020

@author: Bharat
"""
import enchant
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from math import radians, sin, cos, sqrt, atan2
import time
import csv

#-----------------------------Taking input-----------------------------
start = time.time()
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

np.set_printoptions(threshold=np.inf)
df = (pd.read_csv(r'C:\BDA Innovative\whc-sites-2019.csv', sep=',', encoding='latin-1'))
list_names = df['name'].tolist()
list_names = [site for site in list_names]
w = open("sites.txt", "w", encoding='utf-8')
w.write('\n'.join(list_names) + '\n')


with open('input.txt', 'r') as f:
    input = [row for row in csv.reader(f, delimiter=':')]

place       = input[0][1]
ct          = input[1][1]
opt         = input[2][1]
cultural    = input[3][1]
natural     = input[4][1]
danger      = input[5][1]
km          = float(input[6][1])
foreign     = input[7][1]





#-----------------------------Origin finder-----------------------------
place = place.title()
find_name = []
for i in range(len(list_names)):
    find_name.append(similar(place,list_names[i]))
sorted = np.flipud(np.argsort(np.asarray(find_name)))

origin = list_names[sorted[0]]
#[print(col) for col in df.columns]
#print(df[df['name']==origin].index.values, origin)

d = enchant.request_pwl_dict("sites.txt")
d.check(place)
origin = d.suggest(place)[0]
origin_index = df[df['name']==origin].index.values[0]
#print(origin, origin_index)

#-----------------------------Making attributes-----------------------------
list_danger = df['danger'].tolist()
list_long = df['longitude'].tolist()
list_lati = df['latitude'].tolist()
list_category = df['category_short'].tolist()
list_area = df['area_hectares'].tolist()
list_country = df['country'].tolist()
list_region = df['region'].tolist()
list_dist = []
site = list_names[419]
site_index = df[df['name']==site].index.values[0]
for site_index in range(len(list_names)):
    R = 6373.0
    lat1 = radians(list_lati[origin_index])
    lon1 = radians(list_long[origin_index])
    lat2 = radians(list_lati[site_index])
    lon2 = radians(list_long[site_index])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    list_dist.append(distance)

def attributes(origin, site):
    site_index = df[df['name']==site].index.values[0]
    #-----------1.Distance----------
    distance_scale = list_dist[site_index]/20000

    #-----------2.Area--------------
    area_ratio = (list_area[site_index]/list_area[origin_index] if (list_area[origin_index]*list_area[site_index] > 0) else 0)

    #-----------3.Category----------
    if (list_category[origin_index] == list_category[site_index]):
        cat_match = 0
    elif ((list_category[origin_index]=='C' and list_category[site_index]=='N') or (list_category[origin_index]=='N' and list_category[site_index]=='C')):
        cat_match = 1
    else:
        cat_match = 0.5

    #-----------4.Danger------------
    danger = 0 if list_danger[site_index]==0 else 1

    #-----------5.Region vicinity----------

    if list_region[origin_index]==list_region[site_index] : vicinity_score = 0
    if list_region[origin_index]=='Asia and the Pacific':
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.3
        if list_region[site_index]=='Arab States' : vicinity_score = 0.1
        if list_region[site_index]=='Africa' : vicinity_score = 0.3
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.6
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.2
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.4
    elif list_region[origin_index]=='Europe and North America':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.3
        if list_region[site_index]=='Arab States' : vicinity_score = 0.2
        if list_region[site_index]=='Africa' : vicinity_score = 0.4
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.1
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.2
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.3
    elif list_region[origin_index]=='Arab States':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.1
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.2
        if list_region[site_index]=='Africa' : vicinity_score = 0.1
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.5
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.3
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.4
    elif list_region[origin_index]=='Africa':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.3
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.4
        if list_region[site_index]=='Arab States' : vicinity_score = 0.1
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.3
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.4
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.3
    elif list_region[origin_index]=='Latin America and the Caribbean':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.6
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.1
        if list_region[site_index]=='Arab States' : vicinity_score = 0.5
        if list_region[site_index]=='Africa' : vicinity_score = 0.3
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.4
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.3
    elif list_region[origin_index]=='Europe and North America,Asia and the Pacific':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.2
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.2
        if list_region[site_index]=='Arab States' : vicinity_score = 0.3
        if list_region[site_index]=='Africa' : vicinity_score = 0.4
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.4
        if list_region[site_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean' : vicinity_score = 0.2
    elif list_region[origin_index]=='Europe and North America,Asia and the Pacific,Latin America and the Caribbean':
        if list_region[site_index]=='Asia and the Pacific' : vicinity_score = 0.4
        if list_region[site_index]=='Europe and North America' : vicinity_score = 0.3
        if list_region[site_index]=='Arab States' : vicinity_score = 0.4
        if list_region[site_index]=='Africa' : vicinity_score = 0.3
        if list_region[site_index]=='Latin America and the Caribbean' : vicinity_score = 0.3
        if list_region[site_index]=='Europe and North America,Asia and the Pacific' : vicinity_score = 0.2

    #-----------6.Locality----------
    locality = (0 if (list_country[origin_index]==list_country[site_index]) else 1)
    recommendation = distance_scale + area_ratio*0.05 + cat_match*0.4 + danger*1 + vicinity_score*0.2 + locality*0.8
    return recommendation

#-------------------------------Printing--------------------------------
if opt=='N':
    recommendations, dict_unfiltered = [], {}
    recommendations = [attributes(origin, site) for site in list_names]
    raw_recommendation = np.asarray(recommendations)
    recommendations = raw_recommendation.argsort()
    for i in range(int(ct)):
        if (1-round(raw_recommendation[recommendations[i]],5))>0:
            dict_unfiltered[list_names[recommendations[i]]] = '{:.3%}'.format(1-round(raw_recommendation[recommendations[i]],5))
    print(dict_unfiltered)
elif opt=='Y':
    recommendations, dict_filtered = [], {}
    recommendations = [attributes(origin, site) for site in list_names]
    #print(recommendations)
    if cultural=='Y' and natural=='Y':
        recommendations = recommendations
    elif cultural=='Y' and natural=='N':
        for i in range(len(recommendations)):
            if list_category[i]=='C/N' or list_category[i]=='N':
                recommendations[i] = 99
    elif cultural=='N' and natural=='Y':
        for i in range(len(recommendations)):
            if list_category[i]=='C/N' or list_category[i]=='C':
                recommendations[i] = 99
    else:
        print("Please type Y or N in cultural and natural sites input.")

    if danger=='N':
        for i in range(len(recommendations)):
            if list_danger[i]=='1':
                recommendations[i] = 99
    elif danger=='Y':
        recommendations = recommendations
    else:
        print("Please type Y or N in danger sites input.")
    if km>=0 and km<=20000:
        for i in range(len(recommendations)):
            if list_dist[i]>km:
                recommendations[i] = 99
    elif km=='N':
        recommendations = recommendations
    else:
        print("Please type valid search radius input.")
    
    if foreign=='N':
        for i in range(len(recommendations)):
            if list_country[i]!=list_country[origin_index]:
                recommendations[i] = 99
    elif foreign=='Y':
        recommendations = recommendations
    else:
        print("Please type Y or N in foreign sites input.")
    
    raw_recommendation = np.asarray(recommendations)
    recommendations = raw_recommendation.argsort()
    ct = (len(recommendations) if int(ct)>len(recommendations) else ct)
    for i in range(int(ct)):
        if (1-round(raw_recommendation[recommendations[i]],5))>0:
            dict_filtered[list_names[recommendations[i]]] = '{:.3%}'.format(1-round(raw_recommendation[recommendations[i]],5))
    print(dict_filtered)
else:
    print("Please type Y or N in site filtering input.")
    
    

