import os
import forecastio 
import requests
import re
from bs4 import BeautifulSoup as bs
from pprint import pprint

FORECAST_TOKEN = os.environ.get('FORECAST_TOKEN', None) 
AQICN_API_KEY = os.environ.get('AQICN_API_KEY',None)

#weather 파일 메인 함수
def weather(text): 
	#위치 입력시 받아오는 기능. defalt = 강남구
	lat, lng, location_message = forecast_location(text)
	#데이터 가져옴
	icon, output_summary, output_temperature, output_apparentTemperature, output_humidity, output_precipProbability, output_precipIntensity, datamessage = forecast(text, lat, lng, location_message)
	#date 메시지
	datamessage = str(datamessage) + " 날씨를 알려드릴께요."

	if '주간' in text or '요약' in text:
		forecast_message = str([
			{
				"type": "section",
				"text": {   
					"type": "plain_text",
					"text": datamessage
				}
			},
			{
				"type": "context",
				"elements": [
					{
						"type": "mrkdwn",
						"text": location_message
					}
				]
			},
			{
				"type": "section",
				"text": {   
					"type": "plain_text",
					"text": output_summary
				}
			}
		])

	else:
		#메시지에 들어갈 이미지 선택
		forecast_img = forecast_image(icon)
		#미세먼지, 초미세먼지 파싱
		output_fine_dust, output_ultra_fine_dust = fine_dust(location_message)

		forecast_message = str([
			{
				"type": "section",
				"text": {   
					"type": "plain_text",
					"text": datamessage
				}
			},
			{
				"type": "context",
				"elements": [
					{
						"type": "mrkdwn",
						"text": location_message
					}
				]
			},
			{
				"type": "section",
				"fields": [
					{
						"type": "plain_text",
						"text": output_summary
					},
					{
						"type": "plain_text",
						"text": output_fine_dust
					},
					{
						"type": "plain_text",
						"text": output_temperature
					},
					{
						"type": "plain_text",
						"text": output_ultra_fine_dust
					},
					{
						"type": "plain_text",
						"text": output_apparentTemperature
					},
					{
						"type": "plain_text",
						"text": output_precipProbability
					},
					{
						"type": "plain_text",
						"text": output_humidity
					},
					{
						"type": "plain_text",
						"text": output_precipIntensity
					}
				],
				"accessory": {
					"type": "image",
					"image_url": forecast_img,
					"alt_text": "plants"
				}
			}
		])
	return forecast_message


#weather 파일 메인 함수
def forecast(text, lat, lng, location_message): 
	#dark_sky_api 데이터 값 받아옴
	forecast = forecastio.load_forecast(FORECAST_TOKEN, lat, lng, lang = 'ko') 
	Dailydata = forecast.daily()
	
	if '오늘' in text: 
		datamessage = "오늘"
		byDaily = Dailydata.data[0]

	elif '내일' in text:
		datamessage = "내일"
		byDaily = Dailydata.data[1]

	elif '모레' in text:
		datamessage = "모레"
		byDaily = Dailydata.data[2]

	elif '주' in text:
		datamessage = "주간"
		byDaily = Dailydata
		if '가능성' in byDaily.summary:
			summary = str(byDaily.summary) + "이 있습니다."
		elif '비' in byDaily.summary:
			summary = str(byDaily.summary) + "가 있을 예정입니다."
		elif '눈' in byDaily.summary:
			summary = str(byDaily.summary) + "이 있을 예정입니다."
		else:
			summary = str(byDaily.summary)
		none = " "
		return none, summary, none, none, none, none, none, datamessage
	else:
		datamessage = "오늘"
		byDaily = Dailydata.data[0]

	icon = str(byDaily.icon)
	output_summary = "날씨 : " + str(byDaily.summary)
	output_temperature = "온도 : "  + str(round(byDaily.temperatureMax,1)) + "° ~ " + str(round(byDaily.temperatureMin,1)) + "°" 
	output_apparentTemperature = "체감온도 : "  + str(round(byDaily.apparentTemperatureMax,1)) + "° ~ " + str(round(byDaily.apparentTemperatureMin,1)) + "°"
	output_humidity = "습도 : " + str(round(byDaily.humidity * 100,0)) + "%"
	output_precipProbability = "강수확률 : " + str(round(byDaily.precipProbability * 100,1)) + "%"

	#강수확률이 10%이상일때만 강수량 출력
	output_precipIntensity = " "
	if(byDaily.precipProbability > 0.1):
		output_precipIntensity = "강수량 : " +  str(round(byDaily.precipIntensity *10,2)) + "mm"

	return icon, output_summary, output_temperature, output_apparentTemperature, output_humidity, output_precipProbability, output_precipIntensity, datamessage

#날씨에 따른 이미지 선택.
#input byHour.summary
#return img_url
#	https://ssl.gstatic.com/onebox/weather/64/sunny.png 맑음
#	https://ssl.gstatic.com/onebox/weather/48/partly_cloudy.png 약간흐림
#	https://ssl.gstatic.com/onebox/weather/48/cloudy.png 흐림
#	https://ssl.gstatic.com/onebox/weather/48/rain_light.png 약한 비 
#	https://ssl.gstatic.com/onebox/weather/48/rain.png 비 
#	https://ssl.gstatic.com/onebox/weather/48/snow_s_rain.png 눈 비 


def forecast_image(data):

	if data == 'partly-cloudy-day':
		forecast_img = 'https://ssl.gstatic.com/onebox/weather/48/partly_cloudy.png'
	if data == 'cloudy':
		forecast_img = 'https://ssl.gstatic.com/onebox/weather/48/cloudy.png'
	if data == 'clear-day':
		forecast_img = 'https://ssl.gstatic.com/onebox/weather/64/sunny.png'
	if data == 'rain':
		forecast_img = 'https://ssl.gstatic.com/onebox/weather/48/rain.png'
	return forecast_img

#미세먼지 가져오기. 네이버 파싱. 
#input location_message
#return 미세먼지, 초미세먼지
def fine_dust(location_message): 
	request_url = str('http://search.naver.com/search.naver?query='+location_message+' 날씨')
	html = requests.get(request_url)
	if not html:
		a = '해당 url에 접속하지 못했습니다.'
		return a, a

	soup = bs(html.text,'html.parser')
	if not soup:
		a = "서버에 접속하지 못했습니다."
		return a, html

	data1 = soup.find('div',{'class':'detail_box'})
	if not data1:
		a = "데이터를 가져오지 못했습니다."
		return a, soup
	else:
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
		
	return fine_dust_message, ultra_fine_dust_mesage

#입력된 값으로 위치 찾기. #defalt 값 강남구
#input text(사용자 입력 명령어)
#return 경도, 위도, 위치
def forecast_location(text): 
	if '회사' in text:
		lat = 37.4959854
		lng = 127.0664091
		location_message = '서울특별시 강남구'
	elif '도봉' in text:
		lat = 37.6658609
		lng = 127.0317674
		location_message = '서울특별시 도봉구'
	elif '은평' in text:
		lat = 37.6176125
		lng = 126.9227004
		location_message = '서울특별시 은평구'
	elif '동대문' in text:
		lat = 37.5838012
		lng = 127.0507003
		location_message = '서울특별시 동대문구	'
	elif '동작' in text:
		lat = 37.4965037
		lng = 126.9443073
		location_message = '서울특별시 동작구'
	elif '금천' in text:
		lat = 37.4600969
		lng = 126.9001546
		location_message = '서울특별시 금천구'
	elif '구로' in text:
		lat = 37.4954856
		lng = 126.858121
		location_message = '서울특별시 구로구'
	elif '종로' in text:
		lat = 37.5990998
		lng = 126.9861493
		location_message = '서울특별시 종로구'
	elif '강북' in text:
		lat = 37.6469954
		lng = 127.0147158
		location_message = '서울특별시 강북구'
	elif '중랑' in text:
		lat = 37.5953795
		lng = 127.0939669
		location_message = '서울특별시 중랑구'
	elif '강남' in text:
		lat = 37.4959854
		lng = 127.0664091
		location_message = '서울특별시 강남구'
	elif '강서' in text:
		lat = 37.5657617
		lng = 126.8226561
		location_message = '서울특별시 강서구'
	elif '중' in text:
		lat = 37.5579452
		lng = 126.9941904
		location_message = '서울특별시 중구'
	elif '강동' in text:
		lat = 37.5492077
		lng = 127.1464824
		location_message = '서울특별시 강동구'
	elif '광진' in text:
		lat = 37.5481445
		lng = 127.0857528
		location_message = '서울특별시 광진구'
	elif '마포' in text:
		lat = 37.5622906
		lng = 126.9087803
		location_message = '서울특별시 마포구'
	elif '서초' in text:
		lat = 37.4769528
		lng = 127.0378103
		location_message = '서울특별시 서초구'
	elif '성북' in text:
		lat = 37.606991
		lng = 127.0232185
		location_message = '서울특별시 성북구'
	elif '노원' in text:
		lat = 37.655264
		lng = 127.0771201
		location_message = '서울특별시 노원구'
	elif '송파' in text:
		lat = 37.5048534
		lng = 127.1144822
		location_message = '서울특별시 송파구'
	elif '서대문' in text:
		lat = 37.5820369
		lng = 126.9356665
		location_message = '서울특별시 서대문구	'
	elif '양천' in text:
		lat = 37.5270616
		lng = 126.8561534
		location_message = '서울특별시 양천구'
	elif '영등포' in text:
		lat = 37.520641
		lng = 126.9139242
		location_message = '서울특별시 영등포구	'
	elif '관악' in text:
		lat = 37.4653993
		lng = 126.9438071
		location_message = '서울특별시 관악구'
	elif '성동' in text:
		lat = 37.5506753
		lng = 127.0409622
		location_message = '서울특별시 성동구'
	elif '용산' in text:
		lat = 37.5311008
		lng = 126.9810742
		location_message = '서울특별시 용산구'
	else:
		lat = 37.4959854 ##defalt 위치 => 강남역
		lng = 127.0664091
		location_message = "서울특별시 강남구"
		
	return lat, lng, location_message

