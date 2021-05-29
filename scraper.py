from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

# Interfaz de usuario
print("Bienvenido al scraper de los comentarios guardados de Reddit!")
usernameinput = input("Ingresa tu usuario de tu cuenta de Reddit: > ")
passwordinput = input("Ingresa tu contraseña: > ")
print("Muchas gracias! Esto quizas demore un poco, no toques nada pibe...")
sleep(3)

# Put on your seat-belts!!!
chrome_options = Options()

#Disable pop-ups
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

#Headless chrome
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")

url = "https://www.reddit.com/"
driver = webdriver.Chrome("D:\workspace\python\pythonprojects\chromedriver.exe", options=chrome_options)
driver.get(url)


# Login button that pop-ups the login iframe
loginbutton = driver.find_element_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[1]/header/div/div[2]/div/div[1]/a[1]')
loginbutton.click()

# Login iframe
# an iframe is a webpage inside a webpage, that's why we need to switch frames
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[2]/div/iframe'))

usernamefield = driver.find_element_by_id("loginUsername")
passwordfield = driver.find_element_by_id("loginPassword")

usernamefield.send_keys(usernameinput)
passwordfield.send_keys(passwordinput)

driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()

sleep(5)
url = "https://www.reddit.com/user/"+usernameinput+"/saved/"
driver.get(url)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

elements = soup.find_all('p')

comments = []
for i in elements: 
    comments.append(i)
sleep(3)


rss = open("rss.txt","w+", encoding="utf-8")

for i in comments:
    rss.write(i.text)
    rss.write("||")

rss.close()
rss = open("rss.txt","r+", encoding="utf-8")

stripped = []

for i in rss.read():
    stripped.append(i)

rss.close()

rss = open("rss.txt","w+", encoding="utf-8")

counter = 0
charactersperline = 72

for i in stripped:
    rss.write(i)
    counter += 1
    if counter >= charactersperline:
        if i == " ":
            rss.write("\n")
            counter = 0

rss.close()

rss = open("rss.txt","r+", encoding="utf-8")
text = rss.read().replace("|", "\n")

rss.close()

rss = open("rss.txt","w+", encoding="utf-8")

rss.write(text)