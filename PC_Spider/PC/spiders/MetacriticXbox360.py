# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#class Major_Nelson_Blog_BC_List_Spider(scrapy.Spider):
import scrapy
from scrapy.selector import Selector
# from scrapy.http import Request
from XboxBC.items import MetacriticXbox360Item
import re

class MetacriticXbox360(scrapy.Spider):
    name = "MetacriticXbox360"
    allowed_domains = ["metacritic.com"]

    start_urls = (
        'http://www.metacritic.com/browse/games/score/metascore/all/xbox360/all?hardware=all&page=0',
    )
    def parse(self, response):
        print "=" * 50
        numberOfPages = int(response.xpath('//*[@id="main"]/div[1]/div[2]/div/div[2]/ul/li[10]/a/text()').extract()[0])
        print(numberOfPages)
        print "=" * 50
        for j in range(0,numberOfPages):
            next_page = 'http://www.metacritic.com/browse/games/score/metascore/all/xbox360/all?hardware=all&page=' + str(j)
            print("Page" + str(j))
            yield scrapy.Request(next_page, callback=self.metacriticX360Find)

    def metacriticX360Find(self, response):
            rows_in_big_table = response.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/div[3]/div/div/div')
            print(rows_in_big_table.extract())
            for i, onerow in enumerate(rows_in_big_table):
                metacriticGameItem = MetacriticXbox360Item()
                gameName = onerow.xpath('div[3]/a/text()').extract()[0].strip()
                reviewScorePro = onerow.xpath('div[2]/div/text()').extract()[0].strip()
                reviewScoreUser = onerow.xpath('div[4]/span[2]/text()').extract()[0].strip()
                if reviewScoreUser== 'tbd':
                    reviewScoreUser = ''
                print(gameName)
                print(reviewScorePro)
                print(reviewScoreUser)
                # releaseDate
                # isOnXboxOne
                # publisher
                # developer
                # ESRBRating
                metacriticGameItem['gameName'] = gameName
                metacriticGameItem['reviewScorePro'] = reviewScorePro
                metacriticGameItem['reviewScoreUser'] = reviewScoreUser
                print "=" * 50
                yield metacriticGameItem
