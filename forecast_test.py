# -*- coding: utf-8 -*-


import forecastio
FORECAST_TOKEN = '##FORECAST_TOKEN##'



def forecast2(lat, lng):
    forecast = forecastio.load_forecast(FORECAST_TOKEN, lat, lng, lang = 'ko')
    byHour = forecast.hourly()
    message = byHour.summary
    print(message)

lat = 37.5124413
lng = 126.9540519
forecast2(lat, lng)

'''

import forecastio 

FORECAST_TOKEN = ('FORECAST_TOKEN', None) 
def forecast(): 
	lat = 37.497931
	lng = 127.027649
	forecast = forecastio.load_forecast(FORECAST_TOKEN, lat, lng, lang = 'ko') 
	byHour = forecast.hourly() 
	w1 = byHour.summary
	w2 = byHour.temperature + "°"
	w3 = currently.humidity * 100 + "%"
	message = "날씨 : " + w1 + "\n기온 : " + w2 + "\n습도 : " + w3


print(message);

'''

#interpreter*?*

''' 

import forecastio
FORECAST_TOKEN = '##FORECAST_TOKEN##'
lat = 37.5124413
lng = 126.9540519
forecast = forecastio.load_forecast(FORECAST_TOKEN, lat, lng, lang = 'ko') 


byHour = forecast.daily()
message =  byHour.summary  
print(message)

w1 = byHour.summary
w2 = byHour.temperature + "°"
w3 = currently.humidity * 100 + "%"
message = "날씨 : " + w1 + "\n기온 : " + w2 + "\n습도 : " + w3



byHour = forecast.currently()
message =  byHour.humidity  
print(message)




**Methods**
- **currently()**   약간 흐림
- Returns a ForecastioDataPoint object
- **minutely()**   None
- Returns a ForecastioDataBlock object
- **hourly()**  온종일 맑음
- Returns a ForecastioDataBlock object
- **daily()**   오늘동안 이슬비 가능성
- Returns a ForecastioDataBlock object
- **update()**    None
- Refreshes the forecast data by making a new request.



'''