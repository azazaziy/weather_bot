from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from config import OWM_API

def ReturnWeather(place):
	try:
		owm = OWM(OWM_API)
		mgr = owm.weather_manager()
		config_dict = get_default_config()
		config_dict['language'] = 'ru' 
		observation = mgr.weather_at_place(place)
		w = observation.weather
		clouds = w.detailed_status         # 'clouds'
		wind_speed = w.wind()['speed']                 # {'speed': 4.6, 'deg': 330}
		hum = w.humidity                # 87
		temp = w.temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
		f_like = w.temperature('celsius')['feels_like']
		rains = w.rain
		if len(rains) == 0:
			rains = 0
		else:
			rains = rains['1h']*100
		return f'Погода в городе {place}\nтучи: {clouds}\nскорость ветра: {wind_speed}м/с\nВлажность: {hum}%\nТемпература: {temp}, ощущается как: {f_like}\nВероятность дождя в ближайший час: {rains}%'
	except:
		return "Вы ошиблись в названии города"