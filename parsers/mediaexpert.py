from .base import run
SHOP='Media Expert';KIND='retail';URL='https://www.mediaexpert.pl/search?query%5Bquerystring%5D={q}'
SELECTORS=[('div[data-zone="product"]','a','span[class*="price"]','a'),('article','h2, h3','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
