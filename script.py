from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from config import CHROME_PROFILE_PATH
import pandas as pd
import time
#defino funcion para hacer toda la mierda del webdriver y setear las opciones para que ande headless. avisar a tom que el qr se registra en un cache aparte
#asi que tiene que crear un archivo de sistema con el user-data-dir 

def send_msg(phone, message):
	chrome_options = Options()  
	# chrome_options.add_argument("--headless") 
	chrome_options.add_argument(CHROME_PROFILE_PATH)
	chrome_options.add_argument("user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_experimental_option('useAutomationExtension', False)
	chrome_options.add_argument(r"user-data-dir=./driver/data")

	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #set the search engine
	driver.implicitly_wait(10)
	url = "https://web.whatsapp.com/send?phone="+phone+"&text="+message
	driver.get(url)
	
	try:
		text_section = driver.find_element_by_xpath("//div[text()='Type a message']").click()
		text_section.send_keys(message)
	except:
		pass

	send_button = driver.find_element_by_xpath("//span[@data-testid='send']").click()
	print(message + phone)
	time.sleep(5)
	driver.quit()


#abro el archivo con el mensaje y tel de toda la gente de aol. avisar tom que se puede customizar el mensaje tipo con params como name y eso
df = pd.read_csv("sample.csv")
numeros = df.Numeros.to_list()
mensajes = df.Mensajes.to_list()
diccionario = dict(zip(numeros, mensajes))
#ahi corre el codigo, unicamente la primera vez no tiene que ser headless la proxima se puede descometnar porque ya esta creado el archivo de usuario
#agrego el metodo de items porque sino no puedo hacer el unpackign del dict
for key, value in diccionario.items():
	try:
		send_msg(key, value)
	except:
		print(str(key) + ' no recibio el mensaje')
		continue