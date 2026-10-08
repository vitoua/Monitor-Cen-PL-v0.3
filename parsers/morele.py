from .base import run
SHOP='Morele';KIND='retail';URL='https://www.morele.net/wyszukiwarka/?q={q}'
SELECTORS=[('div.product-item','a.productLink','div.price-new, div.price','a.productLink'),('div.cat-product','a','[class*="price"]','a')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
