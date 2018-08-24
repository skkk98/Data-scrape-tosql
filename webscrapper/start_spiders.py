import sched
import time
from scrapy.crawler import CrawlerProcess, CrawlerRunner
#from webscrapper.spiders.Binance_Bot import BinanceBotSpider
from webscrapper.spiders.Bitfinex_Bot import BitfinexBotSpider
from webscrapper.spiders.Bitstamp_Bot import BitstampBotSpider
from webscrapper.spiders.Bittrex_Bot import BittrexBotSpider
from webscrapper.spiders.Cryptopia_Bot import CryptopiaBotSpider
from webscrapper.spiders.Gateio_Bot import GateioBotSpider
from webscrapper.spiders.Huobi_Bot import HuobiBotSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

"""process= CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(YobitSpider)
process.start()
del process


scheduler= sched.scheduler(time.time, time.sleep)
waiting= 10
while True:
    repeated= CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'    
    })
    repeated.crawl(YobitSpider)
    scheduler.enter(waiting, 2, repeated.start)
    scheduler.run()

    print("\n waiting for %d seconds before more action. Pres CTRL+Z to cancel\n"%(waiting))
    repeated.stop()
    del repeated
"""


def crawl_job():
    """Job to start spiders"""
    runner = CrawlerRunner({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    runner.crawl(BitstampBotSpider)
    runner.crawl(BitfinexBotSpider)
    runner.crawl(BittrexBotSpider)
    runner.crawl(CryptopiaBotSpider)
    runner.crawl(GateioBotSpider)
    runner.crawl(HuobiBotSpider)
    
    return runner.join()

def schedule_next_crawl(null, sleep_time):
    """ Schedule next crawl"""
    reactor.callLater(sleep_time, crawl)

def crawl():
    """A "recursive" function that schedules a crawl 30 seconds after each successful crawl."""
    d = crawl_job()
    d.addCallback(schedule_next_crawl, 20)
    d.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)

if __name__=="__main__":
    crawl()
    reactor.run()
