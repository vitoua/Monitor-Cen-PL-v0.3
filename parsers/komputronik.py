from .base import run
SHOP='Komputronik';KIND='retail';URL='https://www.komputronik.pl/search-filter/{q}'
SELECTORS=[('div.product-entry','a','[class*="price"]','a'),('article','h2, h3','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
