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


class CryptopiaBotSpider(scrapy.Spider):
    name = 'Cryptopia_Bot'
    allowed_domains = ['www.cryptopia.co.nz']
    start_urls = ['https://www.cryptopia.co.nz/Exchange?market=EOS_BTC']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        self.driver =wd.Chrome("/home/kalyan/Documents/chromedriver",chrome_options=options)

    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url)
        time.sleep(10)
        result=dict()

        result['Datetime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result['Last_current_price']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/div/b').text

        result['24Hr_price_change']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[3]/div/b[1]').text+"%"

        result['24Hr_high_price']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/div/b').text

        result['24Hr_low_price']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[1]/td[5]/div/b').text

        result['24Hr_volume']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[2]/table/tbody/tr[2]/td/b[2]').text

        result['Coins']= self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[1]/div/div[2]/span[1]').text

        result['BaseCurrency']=self.driver.find_element_by_xpath('//*[@id="market-main"]/div[1]/div/div[1]/div/div[2]/span[2]').text

        result['Exchanges_URL']=response.url

        result['Exchanges']="Cryptopia"

        mysql_output(self.name, result)

