## -*- coding: utf-8 -*-
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


class ReutersBotSpider(scrapy.Spider):
    name = 'Reuters_Bot'
    allowed_domains = ['www.reuters.com']
    start_urls = ['https://www.reuters.com/finance/currencies/quote?destAmt=&srcAmt=1.00&srcCurr=USD&destCurr=KRW']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)
        result=dict()

        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result['Open']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]/div').text

        result['High']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div').text

        result['Low']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/div').text

        result['Close']= self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]/div').text

        result['Quote Currency']= self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/h5').text.split("/")[1]

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="topContent"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/h5').text.split("/")[0]

        result['Exchanges URL']=response.url


        mysql_output(self.name, result)
