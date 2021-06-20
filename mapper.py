from operator import itemgetter
import sys

a=[]

for line in sys.stdin:
    a.append(line)
 
list_names, list_danger, list_long, list_lati, list_category, list_area, list_country, list_region = [None]*len(a),[None]*len(a),[None]*len(a),[None]*len(a),[None]*len(a),[None]*len(a),[None]*len(a),[None]*len(a),
data = {}
for i in range(len(a)):
    index = 0
    res = ''
    index = a[i].find(' is ')
    list_names[i] = a[i][0:index]
    if a[i].find('safe'):
        list_danger[i] = 0
    else:
        list_danger[i] = 1
        
    index = 0
    if a[i].find('The area of the site is '):
        index = (a[i].find('The area of the site is '))
    if index != -1:
        index+=24
        res = '' 
        for idx in range(index, len(a[i])):
            if a[i][idx] == ' ': 
                break
            res += a[i][idx]
        if res == 'nan' or res == ' ' or res == '':
            list_area[i] = 0
        else:
            list_area[i] = float(res)
    else:
        list_area[i] = 0
    
    if a[i].find('cultural'):
        list_category[i] = 'C'
        temp = a[i].find('cultural')
    elif a[i].find('natural'):
        list_category[i] = 'N'
        temp = a[i].find('natural')
    else:
        list_category[i] = 'C/N'
        temp = a[i].find('cultural-natural')
        
        
    index = a[i].find('coordinates')+13
    res = ''    
    for idx in range(index, len(a[i])):
        if a[i][idx] == ',': 
            break
        res += a[i][idx]
    list_long[i] = float(res)
    index = index+len(res)+1
    res = ''
    for idx in range(index, len(a[i])):
        if a[i][idx] == ')': 
            break
        res += a[i][idx]
    list_lati[i] = float(res)   


    index = a[i].find('Site located in')+16
    res = ''
    for idx in range(index, len(a[i])):
        if a[i][idx] == '[': 
            break
        res += a[i][idx]
    list_country[i] = res
    index = index+len(res)+1
    res = ''
    for idx in range(index, len(a[i])):
        if a[i][idx] == ']': 
            break
        res += a[i][idx]
    list_region[i] = res
    data[list_names[i]] = {}
    data[list_names[i]]['Danger'] = list_danger[i]
    data[list_names[i]]['Longitude'] = list_long[i]
    data[list_names[i]]['Latitude'] = list_lati[i]
    data[list_names[i]]['Category'] = list_category[i]
    data[list_names[i]]['Area'] = list_area[i]
    data[list_names[i]]['Country'] = list_country[i]
    data[list_names[i]]['Region'] = list_region[i]
    list = ['Danger', 'Longitude', 'Latitude', 'Category', 'Area', 'Country', 'Region']
for i in range(len(a)):
    for j in range(len(list)):
        tuple = list_names[i].strip() + '|' + str(data[list_names[i]][list[j]])
        print("%s" %tuple)
