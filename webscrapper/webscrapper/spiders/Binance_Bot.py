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


class BinanceBotSpider(scrapy.Spider):
    name = 'Binance_Bot'
    allowed_domains = ["www.binance.com"]
    start_urls = ["https://www.binance.com/en/trade/BTC_USDT"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    
    def __init__(self):
        options = Options()
        #options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        #options.add_argument('window-size=1366x168')
        #options.addArgument("--start-maximized");
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)
        

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()
        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result['Last_current_price']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span').text
        
        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]/span[2]').text.split()[0]
        
        result['24Hr_high_price']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/span').text
        
        result['24Hr_low_price']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/span').text
        
        result['24Hr_volume']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/span').text.split()[0]
        
        result['Coins']= self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/h2/div/a').text
        
        result['BaseCurrency']=self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/h2/span[2]').text.split()[1]
        
        result['Exchanges_URL']=response.url
        
        result['Exchanges']="Binance"
        
        mysql_output(self.name, result)


