from oauth2client.service_account import ServiceAccountCredentials
import gspread
import re
import requests
import random


scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './My Project 17698-b19fc811c553.json', scope)
spread_data = gspread.authorize(credentials)

#메뉴 DB 가져옴
alldata = spread_data.open("Bot_DB").worksheet('Lunch_DB')
DBdata = alldata.get_all_values()

#랜덤 변수 생성용. 메뉴 DB 최대 개수 출력
DB_length = len(DBdata) - 1

#마지막에 추천한 메뉴 제거용
#마지막 메뉴 체크 DB 가져옴
last_menu_check_data = spread_data.open("Bot_DB").worksheet('Lunch_last_menu_check')
latest_record = last_menu_check_data.get_all_values()
latest_record = latest_record[0]

#랜덤으로 변수 생성(최근 추천한 메뉴는 제외)
state = 0;
while state < 1:
	random_data = str(random.randrange(0,DB_length))
	if random_data in latest_record: 
		state = 0;
	else:
		state = 1;
	random_int = int(random_data)
	
#Lunch_last_menu_check에 최근 내역 넣는 기능 구현해야함.
print(DBdata[random_int][1])
	
