from oauth2client.service_account import ServiceAccountCredentials
from soynlp.hangle import jamo_levenshtein
from konlpy.tag import Komoran
import gspread
import re
import numpy as np


def file_search(text):
	DB_array = DB_search()
	similarity_array = similarity(text, DB_array)



def DB_search():
	scope = ['https://spreadsheets.google.com/feeds',
		         'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	        './pjst.json', scope)
	spread_data = gspread.authorize(credentials)

	#해당 DB 가져옴
	all_data = spread_data.open("Bot_DB").worksheet('file_search')
	#행 열 바꿔서 데이터 넣기
	DB_array = np.transpose(all_data.get_all_values())
	return DB_array
	
def similarity(text,DB_array)
	#입력값 데이터를 키워드로 나누기(명사만)
	nlp = Komoran()
	text = text.replace('멈뭄미', ' ')
	text = text.replace('문서', ' ')
	text = text.replace('찾기', ' ')
	#중요한 명사만 배열로 추출하기
	text_data = (nlp.morphs(text))
	


	Matrix = [[0]*2 for i in range(20)]
	#개수만큼 만들기
	return similarity_array

