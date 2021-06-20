import pandas as pd
import re

df = (pd.read_csv(r'C:\BDA Innovative\whc-sites-2019.csv', sep=',', encoding='latin-1'))
list_names = df['name'].tolist()
list_danger = df['danger'].tolist()
list_description = df['short_description_en'].tolist()
list_inscribe = df['date_inscribed'].tolist()
list_long = df['longitude'].tolist()
list_lati = df['latitude'].tolist()
list_category = df['category_short'].tolist()
list_area = df['area_hectares'].tolist()
list_country = df['country'].tolist()
list_region = df['region'].tolist()
p = open("db.txt", "w", encoding='utf-8')
para = []
for i in range(len(list_names)):
    if str(list_danger[i]) == '0':
        p1 = 'a safe'
    else:
        p1 = 'an endangered'
    if list_area[i]:
        p2 = ' The area of the site is ' + str(list_area[i]) + ' hectares.'
    else:
        p2 = ''
    if list_category[i] == 'C':
        p3 = ' cultural'
    elif list_category[i] == 'N':
        p3 = ' natural'
    else:
        p3 = ' cultural-natural'

    para = re.sub("<.*?>", "", str(list_names[i])) + ' is ' + p1 + p3 + ' World Heritage Site located in ' + list_country[i] + '[' + list_region[i] +  '] at coordinates (' + str(list_lati[i]) + ',' + str(list_long[i]) + ').' +  p2 + ' It joined the elite list in ' + str(list_inscribe[i]) + '. ' + re.sub("<.*?>", "", str(list_description[i]))
    with open('C:\BDA Innovative\db.txt', 'a', encoding='utf-8') as db:
        db.write("%s\n" %para)