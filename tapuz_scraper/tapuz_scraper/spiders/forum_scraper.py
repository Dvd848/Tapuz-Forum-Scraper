from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
import w3lib.html
import re

from tapuz_scraper.items import PostItem, MessageItem

def strip_html(html):
    return w3lib.html.remove_tags(
        w3lib.html.remove_tags_with_content(html, which_ones=('script',))
    )

class TapuzScraper(CrawlSpider):
    name = "tapuzscraper"
    allowed_domains= ["www.tapuz.co.il"]
    

    custom_settings = {
        #'CLOSESPIDER_ERRORCOUNT': 1,
        "DOWNLOAD_DELAY": 0.3,
        "FEED_EXPORT_ENCODING": 'utf-8',
    }

    rules = (
        Rule(LinkExtractor(restrict_css="div.p-body-pageContent > div[data-type='thread'] .pageNav-jump--next"), follow=True),
        Rule(LinkExtractor(restrict_css=".structItem--thread > .structItem-cell--main > .structItem-title > a"), callback="parse_post"),
    )

    def __init__(self, forum_id = None, *args, **kwargs):
        usage_message = f"Usage: scrapy crawl {self.name} -a forum_id=<forum_id> [-a user_name=<user_name>] [-O <output_file>]"
        if forum_id is None:
            raise SystemExit(f"Error: Missing forum ID\n{usage_message}")
        self.start_urls = [f"https://www.tapuz.co.il/forums/{forum_id}/"]
        super().__init__(*args, **kwargs)

    def parse_post(self, response):
        if "item" in response.meta:
            post = response.meta['item']
        else:
            post = PostItem()
            post["id"] = int(response.css('html::attr(data-content-key)').get().replace("thread-", ""))
            post["title"] = strip_html(response.css(".p-title > .p-title-value").get()).replace("\t", "").replace("\r", "").replace("\n", "")
            post["author"] = strip_html(response.css(".p-description a.username").get())
            post["date"] = response.css(".p-description time::attr(data-time)").get()
            post["messages"] = []

        for article in response.css('.block-container > .block-body > article.message'):
            message = MessageItem()
            message["id"] = int(article.css('article::attr(data-content)').get().replace("post-", ""))
            message["author"] = article.css('article::attr(data-author)').get()
            message["date"] = article.css("time::attr(data-time)").get()
            message["content"] = re.sub("\\n\\n+", "\n", strip_html(article.css("article.message-body").get()).replace("\t", "").replace("\r", "\n"))
            post["messages"].append(message)

        next_page = response.css('a.pageNav-jump--next::attr(href)')
        if next_page:
            yield Request(response.urljoin(next_page.get()), callback = self.parse_post, meta = {"item": post})
        else:
            if hasattr(self, "user_name"):
                for message in post["messages"]:
                    if message["author"] == self.user_name:
                        yield post
                        break
            else:
                yield post

# scrapy crawl tapuzscraper -a forum_id=617 -O out.json
# scrapy crawl tapuzscraper -a forum_id=617 -a user_name="Dvd848" -O out.json