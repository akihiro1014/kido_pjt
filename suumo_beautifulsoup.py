from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from styleframe import StyleFrame
import requests

url_input = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=090&bs=040&ta=40&sc=40135&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1'
url = url_input + '&page={}'
url_search = url.format(1)
r = requests.get(url_search)
sleep(1)
soup = BeautifulSoup(r.text, "html.parser")
sleep(1)


last = soup.find('ol', class_="pagination-parts")
last_page = last.find_all("li")[-1].text
print(last_page)
now_page = 1

d_list = []

Display_page = len(soup.find_all(class_="cassetteitem"))

aparts = soup.find_all(class_="cassetteitem")
while now_page <= int(last_page):
    url_search = url.format(now_page)
    r = requests.get(url_search)
    sleep(2)
    soup = BeautifulSoup(r.text, "html.parser")
    for apart in aparts:
        bukken_name = apart.find(class_="cassetteitem_content-title")
        address = apart.find(class_="cassetteitem_detail-col1")
        station1 = apart.find(class_="cassetteitem_detail-col2")
        stations = station1.find_all(class_="cassetteitem_detail-text")
        station = ''
        for index in stations:
            station = station + index.text + '\n'
        station = station[:-1]
        age = apart.find(class_="cassetteitem_detail-col3").text
        if age[1] == "築":
            age = age.split('年')[0].split('築')[1]
        else:
            age = "1"
        infos = apart.find_all(class_="js-cassette_link")
        for info in infos:
            price = info.find(class_="cassetteitem_price").text.replace('万円', '')
            layout = info.find(class_="cassetteitem_menseki").text.replace('m2', '')
            d = {
                '物件名' : bukken_name.text,
                '住所' : address.text,
                '最寄駅' : station,
                '築年数\n(年)' : float(age),
                '家賃\n(万円)' : float(price),
                '専有面積\n(㎡)' : float(layout),
            }
            d_list.append(d)
    now_page += 1
    print(now_page)



df = pd.DataFrame(d_list)
df_sort = df.sort_values(['築年数\n(年)'])
with StyleFrame.ExcelWriter('ikimatsudai.xlsx')as writer:
    sf = StyleFrame(df_sort)
    sf.set_column_width(columns='物件名',width=50)
    sf.set_column_width(columns='住所',width=50)
    sf.set_column_width(columns='最寄駅',width=50)
    sf.set_column_width(columns='家賃\n(万円)',width=20)
    sf.set_column_width(columns='専有面積\n(㎡)',width=20)
    sf.to_excel(writer, index = False, sheet_name = 'summary')






# df = pd.DataFrame(d_list)
# df.to_csv('かまいたち.csv', encoding='utf_8_sig')
