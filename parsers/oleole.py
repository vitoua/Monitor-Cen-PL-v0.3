from .base import run
SHOP='OleOle';KIND='retail';URL='https://www.oleole.pl/search.bhtml?keyword={q}'
SELECTORS=[('div.product-for-list','a','[class*="price"]','a'),('article','h2, h3','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
