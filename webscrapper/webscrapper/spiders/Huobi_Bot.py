# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from string import digits
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



class HuobiBotSpider(scrapy.Spider):
    name = 'Huobi_Bot'
    allowed_domains = ['www.huobi.com']
    start_urls = ['http://www.huobi.com/xrp_usdt/exchange//']
    
        
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()    
        mystr=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dt').text
        remove_digits = str.maketrans('', '', digits)
        data=mystr.translate(remove_digits)
        s=data.split('/')
        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result['Last_current_price']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dt/span').text

        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[2]/span').text

        result['24Hr_high_price']=self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[3]/span').text

        result['24Hr_low_price']= self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[4]/span').text

        result['24Hr_volume']= (self.driver.find_element_by_xpath('//*[@id="ticker_wrap"]/dd[5]/span').text).split()[0]

        result['Coins']= s[0]

        result['BaseCurrency']=s[1]

        result['Exchanges_URL']=response.url

        result['Exchanges']="Huobi"

        mysql_output(self.name, result)


   
