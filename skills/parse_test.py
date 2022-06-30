import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

html = requests.get('http://search.naver.com/search.naver?query=날씨')
soup = bs(html.text,'html.parser')
data1 = soup.find('div',{'class':'detail_box'})
data2 = data1.findAll('dd')

fine_dust = data2[0].find('span',{'class':'num'}).text
int_fine_dust = int(re.findall("\d+", fine_dust)[0])

ultra_fine_dust = data2[1].find('span',{'class':'num'}).text
int_ultra_fine_dust = int(re.findall("\d+", ultra_fine_dust)[0])


if 0 <= int_fine_dust <= 30 :
	fine_dust_message = '미세먼지 : 좋음 (' + fine_dust + ')'
elif 31 <= int_fine_dust <= 80 :
	fine_dust_message = '미세먼지 : 보통 (' + fine_dust + ')'
elif 81 <= int_fine_dust <= 150 :
	fine_dust_message = '미세먼지 : 나쁨 (' + fine_dust + ')'
elif 151 <= int_fine_dust:
	fine_dust_message = '미세먼지 : 매우나쁨 (' + fine_dust + ')'

if 0 <= int_ultra_fine_dust <= 15 :
	ultra_fine_dust_mesage = '초미세먼지 : 좋음 (' + ultra_fine_dust + ')'
elif 16 <= int_ultra_fine_dust <= 35 :
	ultra_fine_dust_mesage = '초미세먼지 : 보통 (' + ultra_fine_dust + ')'
elif 36 <= int_ultra_fine_dust <= 75 :
	ultra_fine_dust_mesage = '초미세먼지 : 나쁨 (' + ultra_fine_dust + ')'
elif 76 <= int_ultra_fine_dust:
	ultra_fine_dust_mesage = '초미세먼지 : 매우나쁨 (' + ultra_fine_dust + ')'

print(fine_dust_message, ultra_fine_dust_mesage)