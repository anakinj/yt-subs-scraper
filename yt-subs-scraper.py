from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import re

class WebDriver:
    DOWNLOAD_DIR = '/tmp'

    def __init__(self, headless=True):
        self.options = webdriver.ChromeOptions()

        self.username = os.getenv('GUSERNAME')
        self.password = os.getenv('GPASSWORD')
        self.channel_id = os.getenv('CHANNELID')
        self.phonenumber = os.getenv('PHONENUMBER')
        self.options.add_argument('--disable-extensions')

        if headless:
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-gpu')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"')

        self.options.add_experimental_option(
            'prefs', {
                'download.default_directory': self.DOWNLOAD_DIR,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            }
        )

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)

    def close(self):
        self.driver.quit()

    def login(self):
        self.driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
        f'https://studio.youtube.com/channel/{self.channel_id}'+\
        '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
        self.driver.implicitly_wait(15)
        loginBox = self.driver.find_element_by_xpath('//*[@id ="identifierId"]')
        loginBox.send_keys(self.username)

        nextButton = self.driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
        nextButton[0].click()

        passWordBox = self.driver.find_element_by_xpath(
            '//*[@id ="password"]/div[1]/div/div[1]/input')
        passWordBox.send_keys(self.password)

        nextButton = self.driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
        nextButton[0].click()

        try:
          phoneNumberBox = self.driver.find_elements_by_xpath('//*[@id ="phoneNumberId"]')
          phoneNumberBox[0].send_keys(self.phonenumber)

          nextButton = self.driver.find_elements_by_xpath('//button[@type ="button"]')
          nextButton[0].click()
        except:
          print("No need to verify login, or something even worse happened")

        print(f"Logged in as {self.username}!")

    def read_subs(self):
        self.driver.refresh()
        self.driver.implicitly_wait(30)
        count_element = self.driver.find_element_by_xpath("//div[contains(@class, 'subscribers-title')]/following-sibling::div")
        return int(re.sub("[^0-9]", "", count_element.text))

with WebDriver() as driver:
  driver.login()
  while True:
    print("Refreshing subscription count...")
    try:
      subs = driver.read_subs()
      print(f"Writing current sub count {subs} to file...")
      text_file = open("subs.txt", "w")
      text_file.write(str(subs))
      text_file.close()
    except:
      print("Failed to get subscription count")
    time.sleep(30)