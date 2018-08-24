# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from googletrans import Translator
import mysql.connector

def mysql_output(spyder_name, dic):
    mydb = mysql.connector.connect(
       host = "localhost",
       user = "root",
       password = "root123"
    )
    mycursor = mydb.cursor()
    mycursor.execute("create database if not exists CryptoDatabase")
    mycursor.execute("use CryptoDatabase")
    mycursor.execute("create table if not exists Cryptotable (Datetime varchar(255), Last_current_price varchar(255), 24Hr_price_change varchar(255), 24Hr_high_price varchar(255), 24Hr_low_price varchar(255), 24Hr_volume varchar(255), Coins varchar(255), BaseCurrency varchar(255), Exchanges_URL varchar(1000), Exchanges varchar(255))")
    qry = "Insert Into Cryptotable(Datetime, Last_current_price, 24Hr_price_change, 24Hr_high_price, 24Hr_low_price, 24Hr_volume, Coins, BaseCurrency, Exchanges_URL, Exchanges) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(qry, tuple(dic.values()))
    mydb.commit()
            
class UpbitBotSpider(scrapy.Spider):
    name = 'Upbit_Bot'
    allowed_domains = ['upbit.com']
    start_urls = ['https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    def __init__(self):
        options = Options()
        #options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)
        self.driver.maximize_window()
    
    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(10)
        result=dict()
        translator = Translator()
        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result['Last_current_price']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[1]/strong').text

        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[2]/strong[1]').text

        result['24Hr_high_price']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[1]/dd[1]/strong').text

        result['24Hr_low_price']= self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[1]/dd[2]/strong').text

        result['24Hr_volume']= self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[3]/dl[2]/dd[1]/strong').text

        result['Coins']= translator.translate(self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/span/a/strong').text, dest='en')

        result['BaseCurrency']=self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/div/section[1]/article[2]/div/span[1]/div[1]/span[1]/em').text

        result['Exchanges_URL']=response.url

        result['Exchanges']="Upbit"

        mysql_output(self.name, result)
