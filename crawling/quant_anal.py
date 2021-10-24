import requests
from bs4 import BeautifulSoup as bs
import yaml
import sys
import time

base_url = f"https://finance.naver.com/item/main.naver?code=035720"
response = requests.get( base_url, headers={"User-agent": "Mozilla/5.0"} )
soup = bs(response.text, 'html.parser')

list_skip_str = [
    "link_ifrs",
    "주요재무정보", "최근 연간 실적", "최근 분기 실적",
    "no_data",
]

dict_ym = {}
dict_num = {}

idx = 0
col_cnt = 0
for href in soup.find("table",{"class":"tb_type1 tb_num tb_type1_ifrs"}).find_all("th"):
    finn_th = str(href).replace("\n","")
    skip_tf = False
    for skip_str in list_skip_str:
        if skip_str in finn_th:
            skip_tf = True
            break
    if skip_tf == True: continue
    ym_tf = True
    if "<em>" in finn_th:
        finn_th_str = finn_th.split('scope="col">')[1].strip().split("<em>")[0]
    elif "<strong>" not in finn_th:
        finn_th_str = finn_th.replace('<th class="" scope="col">','').replace("</th>","").strip()    
    else:        
        finn_th_str = finn_th.split("<strong>")[1].replace("</strong></th>","")
        ym_tf = False
    idx += 1
    if ym_tf:
        dict_ym[idx] = finn_th_str
        col_cnt += 1
    else:
        dict_num[idx] = finn_th_str

print(dict_ym)
print(dict_num)

idx = 0
list_nums = []
for href in soup.find("table",{"class":"tb_type1 tb_num tb_type1_ifrs"}).find_all("td"):
    finn_td = str(href).replace("\n","")
    skip_tf = False
    for skip_str in list_skip_str:
        if skip_str in finn_td:
            skip_tf = True
            break
    if skip_tf == True: continue
    finn_td_str = finn_td.replace(" ","").replace("\n","").split(">")[1].split("<")[0].strip().replace(",","")
    try:
        finn_td_num = float(finn_td_str)
    except:
        finn_td_num = 0
        
    idx += 1
    list_nums.append(finn_td_num)
    if idx == col_cnt:
        print(list_nums)
        list_nums = []
        idx = 0