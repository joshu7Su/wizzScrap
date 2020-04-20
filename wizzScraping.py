from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import time
import requests
import json
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup 
from datetime import datetime, timedelta
from dateutil import parser
import re
import argparse



pars = argparse.ArgumentParser(
        description='Find your fly')
pars.add_argument('--add', '--a', nargs="+", type=str, 
                    help='search for destinations')
pars.add_argument('--origin', '--o', type=str, required=True, help="fly from")
pars.add_argument('--all', type=str, help="all destinations from given origin")
pars.add_argument('--list', type=str, 
                    help="get list of available destinations (use with origin)")
pars.add_argument('--date', type=str, help="search untill..(example: 2020-04-01)")
args = pars.parse_args()



class wizzScrap:

    def __init__(self, url, Origin, searched_date=None, Arrival=None):
        self.driver = None
        self.url = url
        self.by = None
        self.value = None
        self.Origin = Origin
        self.Arrival = Arrival
        self.searched_date = searched_date

        self.web_element = None


    def setUpDriver(self):
        #  Set up driver
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-proxy-server')
        options.add_argument('--incognito')
        prefs = {"profile.default_content_setting_values.geolocation" :2}
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome( 
                "/Users/adamke/Downloads/chromedriver", 
                options=options)
        return self.driver

    def startDriver(self):
        self.driver.get(self.url)

    def find(self, by, value):
        element = WebDriverWait(
            self.driver, 20).until(
            EC.visibility_of_element_located((by, value)))
        self.web_element = element
        return self.web_element

    def inputText(self, text):
        return self.web_element.send_keys(text)

    def click(self, by, value):
        element = WebDriverWait(
            self.driver, 20).until(
            EC.element_to_be_clickable((by, value)))
        self.web_element = element
        element.click()
        return self.web_element

    def text(self):
        text = self.web_element.text
        return text

    def switch_tabs(self):
        #  Close unneded tab and focus on the main one
        WebDriverWait(self.driver, 20).until(
            EC.number_of_windows_to_be(2))

        mainWindow = self.driver.window_handles[1]  #  Thats the Tab we want
        self.driver.close()
        self.driver.switch_to.window(mainWindow)

    def isElementExist(self, by, value):
        try:
            self.find(by, value)
        except NoSuchElementException:
            result = False
        else: 
            result = True
        print(result)

    def closeDriver(self):
        self.driver.quit()

    def stringToNum(self, string):
        # price = int(''.join(re.findall('\d+', get_price)))
        number = int(''.join(ele for ele in string if ele.isdigit()))
        return number

    def return_date(self):
        #  Get recent date and convert it to the string format
        html = self.driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        date_picker = soup.findAll("li",{
                "class":"js-magical-width-item js-date-item flight-select__"
                "flight-date-picker__day js-selectable"})
        for i in date_picker:
            date_time = i.div.time['datetime']
            date_parse = parser.parse(date_time)
            date = str(datetime.date(date_parse))
        return date

    def findDestinations(self):
        #  Find available destinations for specific Airport
        self.setUpDriver()
        self.startDriver()
        self.StartingAirport()

        html = self.driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        find_airport = soup.findAll("label",{"class":"locations-container__location"})

        available_destinations = []
        for i in find_airport:
            try:
                airport = i.strong.getText()
            except:
                pass
            else:
                available_destinations.append(airport)
                print(airport)
        with open('airports.json', 'w', encoding='utf8') as f:
            json.dump(available_destinations, f, ensure_ascii=False, indent=4)
        return available_destinations

    def StartingAirport(self):
        self.click(By.XPATH, "//*[@id='search-departure-station']")
        self.inputText(self.Origin)
        self.click(By.CSS_SELECTOR, 
        "strong[class='locations-container__location__name']")
        self.click(By.XPATH, "//*[@id='search-arrival-station']")
        time.sleep(1)

    def ArrivalAirport(self):
        self.inputText(self.Arrival)
        self.click(By.CSS_SELECTOR, 
        "strong[class='locations-container__location__name']")
        #  Start searching
        self.click(By.CSS_SELECTOR, "button[data-test='flight-search-submit']")

    def collectDatesPrices(self):
        prices_dates = {}  
        prices_dates[self.Arrival] = [] 

        html = self.driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        date_picker = soup.findAll("li",{
                "class":"js-magical-width-item js-date-item flight-select"
                "__flight-date-picker__day js-selectable"})

        for i in date_picker:
            get_price = i.div.div.span.getText()
            price = self.stringToNum(get_price)
            #  get date as string
            date_time = i.div.time['datetime']
            date_parse = parser.parse(date_time)
            date = str(datetime.date(date_parse))

            prices_dates[self.Arrival].append({  
                'price': price,
                'date': date
            })

        filename = 'tickets.json'
        try:
            json_obj = self.load_json_content()
        except:
            with open(filename, 'w') as f:
                json.dump(prices_dates, f, indent=4)
        else:
            json_obj.update(prices_dates)
            with open(filename, 'w') as f:
                json.dump(json_obj, f, indent=4)
            
    def load_json_content(self):
        filename = 'tickets.json'
        try:
            with open(filename, 'r') as f:
                json_obj = json.load(f)
        except FileNotFoundError:
            return None
        else:
            return json_obj
     
    def parse(self):
        self.setUpDriver()
        self.startDriver()
        self.driver.maximize_window()
        self.StartingAirport()
        self.ArrivalAirport()
        self.switch_tabs()

        #  wait untill data is loaded
        button_element = self.find(By.XPATH, 
            "//button[@class='flight-select__flight-date-picker__button "
            "flight-select__flight-date-picker__button--next']")
        #  Clicking element untill searched date = recent date
        count_click = 0
        while True:
            recent_date = self.return_date()
            print('recent date' + recent_date)
            if recent_date <= self.searched_date:
                button_execute = self.driver.execute_script(
                        "return document.getElementsByClassName"
                        "('flight-select__flight-date-picker__button flight-select"
                        "__flight-date-picker__button--next')[0].click();"
                        )
                time.sleep(2)
                count_click += 1
                print(count_click)
            else:
                break

        # self.save_content_to_jsons()
        self.collectDatesPrices()


url = 'https://wizzair.com'
search_destination = []

Origin = args.origin
Origin.capitalize()

if Origin and args.list:
    #  Open driver to find available destinations for given airport
    #  and store them in available_destinations
    Page = wizzScrap(url, Origin)
    available_destinations = Page.findDestinations()
    print(available_destinations)
    Page.closeDriver()

elif Origin and args.add and args.date:
    print(args.add)
    for airport in args.add:
        Arrival = airport.capitalize()

        Page = wizzScrap(url, Origin, args.date, Arrival)
        Page.parse()
        Page.closeDriver()

elif Origin and args.all and args.date:
    Page = wizzScrap(url, Origin)
    available_destinations = Page.findDestinations()
    Page.closeDriver()

    for Arrival in available_destinations:
        Page = wizzScrap(url, Origin, args.date, Arrival)
        Page.parse()
        Page.closeDriver()




    