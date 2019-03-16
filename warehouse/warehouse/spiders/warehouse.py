import scrapy
from ..items import WarehouseItem
from scrapy_redis.spiders import RedisSpider


class WarehouseSpider(RedisSpider):
    name = "warehouse"
    allowed_domains = ("barneyswarehouse.com", )
    prefix_url = "https://www.barneyswarehouse.com"
    # start_urls = ("https://www.barneyswarehouse.com/category/men/clothing/activewear/N-1f3gneh", )
    DEFAULT_REQUEST_HEADERS = {
      ':authority': 'www.barneyswarehouse.com',
      ':method': 'GET',
      ':path': '/category/men/clothing/activewear/N-1f3gneh',
      ':scheme': 'https',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US;q=0.9,en;q=0.8',
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    # def make_request_from_url(self, url):
    #      pass

    def parse(self, response):
        categories_url = response.xpath('//ul[@id="category-level-1"]//a/@href').extract()
        categories_text = response.xpath('//ul[@id="category-level-1"]//a/text()').extract()
        categories = zip(categories_text, categories_url)

        for category_text, url in categories:
            url = self.prefix_url + url
            yield scrapy.Request(url, headers=self.DEFAULT_REQUEST_HEADERS, meta={"category_text": category_text}, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath('//ul[@class="product-set"]//a[@class="thumb-link"]/@href').extract()

        for url in urls:
            yield scrapy.Request(self.prefix_url + url,
                                 meta={"category_text": response.meta["category_text"]},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        fields_item = WarehouseItem()
        page = response.xpath('//div[contains(@class, "primary-content")]').extract_first()
        product_info = page.xpath(".//div[@id='productInfoContainer']").extract_first()
        fields_item["company"] = product_info.xpath('.//span[@class="prd-brand"]//a/text()').extract_first()
        fields_item["title"] = product_info.xpath(".//h1[@class='product-title']/text()").extract_first().strip()
        fields_item["images"] = page.xpath(".//div[contains(@class, 'product-image-carousel')]//img/@src").extract()
        fields_item["sizes"] =[size.strip() for size in product_info.xpath(".//div[contains(@class, 'atg_store_sizePicker')]// \
                               a[not (contains(@class, 'disabled-size'))]/text()").extract()]
        fields_item["price"] = product_info.xpath(".//span[@class='red-discountPrice']/text()")\
                                                  .extract_first().strip()
        fields_item["description"] = "".join([paragraph.strip() for paragraph in \
                                              product_info.xpath('.//div[@class="hidden-xs hidden-sm"]/node()').extract()])
        fields_item["category"] = response.meta["category_text"]
        return fields_item

    def sizes(self, response):
        pass

    def description(self, response):
        pass
