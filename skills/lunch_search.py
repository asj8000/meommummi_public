from oauth2client.service_account import ServiceAccountCredentials
import gspread
import re
import requests
import random
from bs4 import BeautifulSoup as bs


def lunch_search(text):
	url = DB_search()


	data_title, data_stars, data_location, data_food_type, data_price, data_img = parsing(url)
	
	random_message = ['이런 메뉴는 어때요?','이 메뉴 어때요?','이 메뉴를 추천해줄께요!','오늘은 이거! 어떠신가요?','요긴 어때요?','메뉴를 추천해드릴께요!','오늘의 점심은 이거?!','점심을 추천해드릴께요!','오늘 점심은 이거!! 콜?!']
	random_int = str(random.randrange(0,7))
	title_message = random_message[random.randrange(0,7)]




	forecast_message = str([
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": title_message
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ">>> *"+data_title+"*                   <https://map.naver.com/v5/search/"+data_location+"%20"+data_title+"|위치보기>\n"+data_stars+"\n 음식 종류 : "+data_food_type+" \n 가격대 : "+ data_price
			},
			"accessory": {
				"type": "image",
				"image_url": data_img,
				"alt_text": "맛있겠죠?"
			}
		}
	])
	
	return forecast_message





def DB_search():
	scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	        './pjst.json', scope)
	spread_data = gspread.authorize(credentials)

	#메뉴 DB 가져옴
	alldata = spread_data.open("Bot_DB").worksheet('Lunch_DB')
	lunch_db_data = alldata.get_all_values()

	#랜덤 변수 생성용. 메뉴 DB 최대 개수 출력
	DB_length = len(lunch_db_data) - 1
	
	#마지막에 추천한 메뉴 제거용
	#마지막 메뉴 체크 DB 가져옴
	last_menu_check_data = spread_data.open("Bot_DB").worksheet('Lunch_last_menu_check')
	last_menu_check_array = last_menu_check_data.get_all_values()
	#기록되어있는 값들을 array로 불러옴
	latest_record = last_menu_check_array[0]


	#랜덤으로 변수 생성(최근 추천한 메뉴는 제외)
	state = 0;
	while state < 1:
		random_data = str(random.randrange(0,DB_length))
		if random_data in latest_record: 
			state = 0;
		else:
			state = 1;
		random_int = int(random_data)


	#마지막 등록한 위치 데이터
	last_record_location = last_menu_check_array[1][0]

	#마지막 식당 추천 내역을 입력할 셀 찾기.
	int_to_eng_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
	int_to_eng = int_to_eng_array[int(last_record_location)]
	#해당 위치에 랜덤 추천값을 입력.
	location = str(int_to_eng+'1')
	last_menu_check_data.update_acell(location, random_int)

	#A2셀(마지막 변경 위치)의 데이터를 가져와 +1해서 업데이트
	record_last = int(last_record_location)+1
	if record_last >= 21:
		record_last = 0
	last_menu_check_data.update_acell('A2', record_last)
	
	#Lunch_DB 시트 랜덤열의 B셀 데이터(url) 리턴
	return lunch_db_data[random_int][1]
	

def parsing(url):
	#데이터 파싱부분
	request_headers = {
	    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
	                   '(KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'),
	}
	request_data = requests.get(url, headers = request_headers)
	soup = bs(request_data.text,'html.parser')


	info_data = soup.find('table',{'class':'info'}).text
	info_data_array = info_data.split('\n')


	stars = (soup.find('strong',{'class':'rate-point'}).text).strip()


	if not stars:
		data_stars = " "
	else:
		stars = float(stars)

	if not stars:
		data_stars = " "
	elif stars >= float(4.9):
		data_stars = ':star_active::star_active::star_active::star_active::star_active:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 	
	elif stars >= float(4.4):
		data_stars = ':star_active::star_active::star_active::star_active::star_half:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(3.9):
		data_stars = ':star_active::star_active::star_active::star_active::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(3.4):
		data_stars = ':star_active::star_active::star_active::star_half::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(2.9):
		data_stars = ':star_active::star_active::star_active::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(2.4):
		data_stars = ':star_active::star_active::star_half::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(1.9):
		data_stars = ':star_active::star_active::star_disable::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(1.4):
		data_stars = ':star_active::star_half::star_disable::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(0.9):
		data_stars = ':star_active::star_disable::star_disable::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	elif stars >= float(0.4):
		data_stars = ':star_half::star_disable::star_disable::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 
	else :
		data_stars = ':star_disable::star_disable::star_disable::star_disable::star_disable:(' + (soup.find('strong',{'class':'rate-point'}).text).strip() + ') ' + str(soup.find('span',{'class':'cnt review'}).text) + ' Reviews' 



	data_title = soup.find('h1',{'class':'restaurant_name'}).text
	data_location = info_data_array[5]
	data_food_type = info_data_array[14] 
	data_price = info_data_array[19]
	data_img = str(soup.find('img',{'class':'center-croping'})['src'])


	return data_title, data_stars, data_location, data_food_type, data_price, data_img
	

 