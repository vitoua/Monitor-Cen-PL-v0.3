from .base import run
SHOP='Sferis';KIND='retail';URL='https://www.sferis.pl/szukaj?q={q}'
SELECTORS=[('div.product-box','a.product-name','[class*="price"]','a.product-name'),('article','h2, h3','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
