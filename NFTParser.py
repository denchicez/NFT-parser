import os
import re
import time

import requests as rq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class OpenSeaParser:
    def __init__(self, log=False):
        self.url = 'https://opensea.io/activity?search[eventTypes][0]=AUCTION_SUCCESSFUL'
        self.insts = []
        self.twitters = []
        self.tokens = []
        self.users_was = []
        self.log = log

    def createBrowser(self):
        options = Options()
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        self.browser = browser

    def closeBrowser(self):
        self.browser.close()

    def parse_account(self, url):  # берет ланные аккаунта по url
        self.browser.set_page_load_timeout(4)
        try:
            self.browser.get(url)
        except:
            pass
        self.browser.set_page_load_timeout(60)
        html = self.browser.page_source
        try:
            token = re.findall(r'"address":"([^"]*)"', html)[0]
        except:
            token = ''
        try:
            twitter = r"https://twitter.com/" + re.findall(r'"https:\/\/twitter\.com\/([^"]*)"', html)[0]
        except:
            twitter = ""
        try:
            inst = r"https://instagram.com/" + re.findall(r'"https:\/\/instagram\.com\/([^"]*)"', html)[0]
        except:
            inst = ""

        soup = BeautifulSoup(html, "html.parser")
        try:
            login = soup.find("div", class_="AccountHeader--title").text
        except:
            login = ''
        try:
            desc = soup.find("div", class_="AccountHeader--bio").text
        except:
            desc = ""
        return token, login, desc, twitter, inst

    def task(self, user):
        token, login, desc, twitter, inst = self.parse_account(r"https://opensea.io/" + user)
        return token, login, desc, twitter, inst

    def getAllData(self, insert_value, type_of_data):
        self.createBrowser()
        all_data = [0, 0]
        while (True):
            self.browser.get(self.url)
            time.sleep(5)  # donwload nft
            html = self.browser.page_source
            soup = BeautifulSoup(html, "html.parser")
            links = soup.findAll("a", class_="AccountLink--ellipsis-overflow", href=True)
            for index in range(1, len(links), 2):
                link = links[index]
                if (link['href'] in self.users_was):
                    continue
                self.users_was.append(link['href'])
                if self.log:
                    print("Now parse this user -> " + link['href'])
                token, login, desc, twitter, inst = self.task(link['href'])
                if self.log:
                    print("Find this parametrs")
                    print("token -> " + token)
                    print("login -> " + login)
                    print("desc -> " + desc)
                    print("twitter -> " + twitter)
                    print("inst -> " + inst)
                if (inst != ''):
                    self.insts.append(inst)
                if (twitter != ''):
                    self.twitters.append(twitter)
                all_data[0] = len(self.insts)
                all_data[1] = len(self.twitters)
                if (all_data[type_of_data] >= insert_value):
                    break
            if (all_data[type_of_data] >= insert_value):
                break
        self.closeBrowser()

    def getInstagram(self, counter):
        self.getAllData(counter, 0)
        return self.insts

    def getTwitters(self, counter):
        self.getAllData(counter, 1)
        return self.twitters

    def downloadPhotos(self, counter):
        try:
            os.mkdir("images")
        except:
            pass
        counternow = 0
        self.createBrowser()
        self.browser.get('https://opensea.io/activity?search[eventTypes][0]=AUCTION_SUCCESSFUL')
        while (True):
            html = self.browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find('div', role="list").findAll("div", role="listitem")
            # print(items)
            for item in items:
                try:
                    img = item.find("img", class_="Image--image")['src']
                    price = item.find("div", class_="Price--fiat-amount").text
                    price = price.replace(" ", "")
                    price = price.split(",")[0]
                    img = img + "00"
                    img = rq.get(img)
                    out = open(f"images\img{counternow}_{price}.jpg", "wb")
                    out.write(img.content)
                    out.close()
                    counternow += 1
                    if (counternow > counter):
                        break
                except Exception as e:
                    print(e)
                    continue
            time.sleep(30)
        self.closeBrowser()

# if __name__ == '__main__':
#     parser = OpenSeaParser()
#     parser.log = True
#     instagrams = parser.downloadPhotos(1)
#     print(instagrams)
