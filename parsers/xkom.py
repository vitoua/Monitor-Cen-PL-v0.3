from .base import run
SHOP='x-kom';KIND='retail';URL='https://www.x-kom.pl/szukaj?q={q}'
SELECTORS=[('div[data-name="productCard"]','h3','span[data-name="productPrice"]','a'),('article','h3','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
