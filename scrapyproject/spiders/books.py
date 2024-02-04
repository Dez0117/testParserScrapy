import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        URL = "https://books.toscrape.com"
        yield scrapy.Request(url=URL, callback=self.book_page_parse)

    def book_page_parse(self, response):
        for selector in response.css('article.product_pod'):
            yield {
                'title': selector.css('h3 > a::attr(title)').extract_first(),
                'price': selector.css('.price_color::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.book_page_parse)


# http://books.toscrape.com/catalogue/page-1.html
