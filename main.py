from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd





PATH = "C:\Program Files (x86)\chromedriver.exe"
service = Service(executable_path=PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# Create a new Chrome driver instance
driver = webdriver.Chrome(service=service, options=options)

columns=['content','date','recommend','hours','found_helpful','user_products']
data=[]
user_products=[]
def scroll():

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# Navigate to the Amazon product page
driver.get("https://steamcommunity.com/app/2195250/reviews/?browsefilter=toprated&snr=1_5_100010_")

for i in range(615):
    time.sleep(2)
    scroll()
containers=driver.find_elements(By.CLASS_NAME,"apphub_CardContentMain")
for container in containers:
    content = container.find_element(By.CLASS_NAME, 'apphub_CardTextContent').text
    date_posted = container.find_element(By.CLASS_NAME, 'date_posted').text
    title = container.find_element(By.CLASS_NAME, 'title').text
    hours = container.find_element(By.CLASS_NAME, 'hours').text
    found_helpful = container.find_element(By.CLASS_NAME, 'found_helpful').text


    # Append the extracted data to the "data" list as a dictionary
    data.append({
        'content': content,
        'date': date_posted,
        'recommend': title,
        'hours': hours,
        'found_helpful': found_helpful,
    })
df = pd.DataFrame(data)
authors=driver.find_elements(By.CLASS_NAME,'apphub_friend_block_container')
for author in authors:
    try:
        product_count=author.text
    except:
        product_count=None
    user_products.append({'product_count':product_count})
df2=pd.DataFrame(user_products)
df.to_csv('review.csv')
df2.to_csv('user.csv')
