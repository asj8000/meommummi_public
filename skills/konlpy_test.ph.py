from oauth2client.service_account import ServiceAccountCredentials
from soynlp.hangle import jamo_levenshtein
from konlpy.tag import Komoran
import gspread
import re
import numpy as np

input_text = '멈뭄미 문서 도서'
scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './pjst.json', scope)
spread_data = gspread.authorize(credentials)

#해당 DB 가져옴
all_data = spread_data.open("Bot_DB").worksheet('file_search')
#행 열 바꿔서 데이터 넣기
DB_array = np.transpose(all_data.get_all_values())


#입력값 데이터를 키워드로 나누기(명사만)
nlp = Komoran()
text = input_text.replace('멈뭄미', ' ')
text = text.replace('문서', ' ')
text = text.replace('찾기', ' ')
#중요한 명사만 배열로 추출하기
text_data = (nlp.morphs(text))

search_text = text_data[0]
array = DB_array[0]


array = (nlp.morphs(array[2]))
if search_text in array:
    print('포함')
else:
    print('미포함')

