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

class BittrexBotSpider(scrapy.Spider):
    name = 'Bittrex_Bot'
    allowed_domains = ['www.bittrex.com']
    start_urls = ['https://www.bittrex.com/home/markets/']
    
    
        
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        options.add_argument('window-size=1920x1080')
        #options.add_argument('--disable-gpu')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()
        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        i=0
        
        while self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']').get_attribute("title")!="Go to USDT-TRX (TRON)...":
            i+=1
        
        result['Last_current_price']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr[12]/td[5]').text
        
        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr[12]/td[4]/span[1]').text
        
        result['24Hr_high_price']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[6]').text+"%"
        
        result['24Hr_low_price']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[7]').text
        
        result['24Hr_volume']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[3]').text
        
        result['Coins']= self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/table/tbody/tr['+str(i+1)+']/td[2]').text
        
        result['BaseCurrency']=self.driver.find_element_by_xpath('//*[@id="home-wrapper"]/div[2]/div[4]/div/div/h2/span[1]').text
        
        result['Exchanges_URL']=response.url
        
        result['Exchanges']="Bittrex"
        mysql_output(self.name, result)
       
        
 
 
        
        
