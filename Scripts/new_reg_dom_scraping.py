from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time


path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'new_reg_dom'))
options = Options()
options.add_argument("--headless")
options.add_argument("start-maximized")
#accept cookies
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2,
                                          'download.default_directory': "YOUR_PATH"})
# installing the instance of browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# browser.implicitly_wait(5)


try:
    #open website with browser
    driver.get('https://www.whoisds.com/newly-registered-domains')


    #To see all components of website you press CTRL+U and then you find the button or link that you want to hit

    download_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="btn btn-primary btn-xs"]')))


    if download_buttons:

        download_buttons[0].click()

        WebDriverWait(driver, 30).until(lambda x: x.find_element(By.XPATH, '//button[@class="btn btn-primary btn-xs"]'))


except Exception as e:
    print(str(e))


time.sleep(15)



driver.quit()
