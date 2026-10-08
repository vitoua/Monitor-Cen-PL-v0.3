from .base import run
SHOP='Allegro';KIND='marketplace';URL='https://allegro.pl/listing?string={q}'
SELECTORS=[('article','h2','[aria-label*="zł"], [class*="price"]','a[href*="oferta"]')]
def scrape(page,p):return run(page,p,SHOP,KIND,URL,SELECTORS)
