import scrapy

from scrapy.loader import ItemLoader
from ..items import DnbplItem
from itemloaders.processors import TakeFirst


class DnbplSpider(scrapy.Spider):
	name = 'dnbpl'
	start_urls = ['https://www.dnb.pl/pl/aktualnosci/']

	def parse(self, response):
		post_links = response.xpath('//h4/a[@class="green_color"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="information-content-wrapper"]/h4/text()').get()
		description = response.xpath('//div[@class="information-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=DnbplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
