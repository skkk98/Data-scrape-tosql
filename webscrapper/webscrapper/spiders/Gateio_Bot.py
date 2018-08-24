# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
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



class GateioBotSpider(scrapy.Spider):
    name = 'Gateio_Bot'
    allowed_domains = ['gate.io']
    start_urls = ['https://gate.io/trade/BTG_USDT']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        options.add_argument('window-size=1920x1080')
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)

    def parse(self, response):
        
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()

        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result['Last_current_price']="N/A"#self.driver.find_element_by_xpath('').text
  
        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id= "top_last_rate_change"]/em/span').text

        result['24Hr_high_price']="N/A"#self.driver.find_element_by_xpath('').text

        result['24Hr_low_price']= "N/A"#self.driver.find_element_by_xpath('').text

        result['24Hr_volume']= self.driver.find_element_by_xpath('//*[@id="currVol"]').text[9:]

        result['Coins']= "Bitcoin Gold"

        result['BaseCurrency']=self.driver.find_element_by_xpath('//*[@id="mianTlist"]/span[1]/strong').text[7:]

        result['Exchanges_URL']=response.url

        result['Exchanges']="Gate.io"

        mysql_output(self.name, result)
