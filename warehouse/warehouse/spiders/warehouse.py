import scrapy
from ..items import WarehouseItem
from scrapy_redis.spiders import RedisSpider
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class WarehouseSpider(RedisSpider):
    name = "warehouse"
    allowed_domains = ("barneyswarehouse.com", )
    prefix_url = "https://www.barneyswarehouse.com"
    HEADERS = {
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
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/70.0.3538.77 Safari/537.36',
    }

    fields_item = WarehouseItem()

    @property
    def worked(self):
        inprogress = len(self.crawler.engine.slot.inprogress)
        # self.crawler.engine.scheduler_cls.has_pending_requests(self.crawler.engine.slot.scheduler)
        if inprogress <= 1:
            return True
        return False

    def parse(self, response):
        categories_url = response.xpath('//ul[@id="category-level-1"]//a/@href').extract()
        pagination = True if response.xpath('//span[@class="pagination-ipad"]').extract_first() else False
        self.fields_item["url"] = self.take_url(response.request.url)

        if categories_url:
            categories_text = response.xpath('//ul[@id="category-level-1"]//a/text()').extract()
            categories = zip(categories_text, categories_url)

            for category_text, url in categories:
                url = self.prefix_url + url
                yield scrapy.Request(url,
                                     headers=self.HEADERS,
                                     meta={"category_text": category_text},
                                     callback=self.parse_category)
        else:
            url = response.request.url

            if pagination:
                callback = self.pagination
            else:
                callback = self.parse_category
            yield scrapy.Request(url, headers=self.HEADERS, callback=callback)

    def pagination(self, response):
        pagination = response.xpath('//ul[@class="pagination-links"]')

        num_last_page = int(pagination.xpath('.//li')[-2].xpath('.//a/text()').extract_first())
        for num_page in range(1, num_last_page + 1):
            url = response.request.url + "?page=" + str(num_page)
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath('//ul[@class="product-set"]//a[@class="thumb-link"]/@href').extract()

        category_text = response.meta.get("category_text")
        if category_text:
            meta_data = {"category_text": category_text}
        else:
            category_text = response.xpath('//h1[@class="title hidden-xs col-sm-10"]/text()').extract_first().strip()
            meta_data = {"category_text": category_text}

        for url in urls:
            yield scrapy.Request(self.prefix_url + url, headers=self.HEADERS, meta=meta_data,
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        page = response.xpath('//div[contains(@class, "primary-content")]')
        product_info = page.xpath(".//div[@id='productInfoContainer']")
        self.fields_item["company"] = product_info.xpath('.//span[@class="prd-brand"]//a/text()').extract_first()
        self.fields_item["title"] = product_info.xpath(".//h1[@class='product-title']/text()").extract_first().strip()
        self.fields_item["images"] = page.xpath(".//div[contains(@class, 'product-image-carousel')]//img/@src").extract()
        self.fields_item["sizes"] = self.take_sizes(product_info)
        self.fields_item["price"] = self.take_price(product_info)
        self.fields_item["description"] = self.take_description(product_info)
        self.fields_item["category"] = response.meta["category_text"]

        return self.fields_item

    def take_sizes(self, page):
        sizes = page.xpath(".//div[contains(@class, 'atg_store_sizePicker')]//\
                            a[not (contains(@class, 'disabled-size'))]/text()").extract()
        return [size.strip() for size in sizes]

    def take_description(self, page):
        description = page.xpath('.//div[@class="hidden-xs hidden-sm"]/node()').extract()
        return "".join([text_fragment.strip() for text_fragment in description])

    def take_price(self, product_info):
        price = product_info.xpath(".//span[@class='red-discountPrice']/text()").extract_first()
        if price is None:
            price = product_info.xpath(".//div[@class='atg_store_productPrice']/text()").extract_first()
        return price.strip()

    def take_url(self, url):
        if url.split("?")[-1].startswith("page"):
            url = url[:url.find("?")]
        if url.endswith("/"):
            url = url[:-1]
        return url
