import json,re
from urllib.parse import quote_plus,urljoin
from bs4 import BeautifulSoup

def money(v):
    if v is None:return None
    s=str(v).replace('\xa0',' ').replace('PLN','').replace('zł','')
    s=re.sub(r'[^0-9,.-]','',s).replace(',','.')
    try:
        x=round(float(s),2);return x if 20 <= x <= 50000 else None
    except:return None

def result(product,shop,kind,status,url='',price=None,availability='nieznana',title='',method='',message='',confidence='niska'):
    return {'pn':product['PN'],'ean':product['EAN'],'nazwa':product['NAZWA'],'zrodlo':shop,'typ':kind,'cena':price,'waluta':'PLN','dostepnosc':availability,'tytul_oferty':title,'url':url,'status':status,'metoda':method,'pewnosc':confidence,'komunikat':message}

def queries(p):
    out=[]
    for x in (p.get('EAN',''),p.get('PN',''),p.get('NAZWA','')):
        x=str(x or '').strip()
        if x and x not in out:out.append(x)
    return out

def blocked(response): return bool(response and response.status in (401,403,429))
def product_match(text,p):
    t=re.sub(r'\s+',' ',str(text).lower())
    return any(str(x).lower() in t for x in (p.get('EAN',''),p.get('PN','')) if str(x).strip())
def jsonld(html,base,p):
    soup=BeautifulSoup(html,'lxml')
    for tag in soup.select('script[type="application/ld+json"]'):
        try:
            raw=json.loads(tag.get_text(strip=True));stack=raw if isinstance(raw,list) else [raw]
            while stack:
                o=stack.pop(0)
                if isinstance(o,list):stack.extend(o);continue
                if not isinstance(o,dict):continue
                if isinstance(o.get('@graph'),list):stack.extend(o['@graph'])
                if isinstance(o.get('itemListElement'),list):stack.extend([x.get('item',x) for x in o['itemListElement'] if isinstance(x,dict)])
                if o.get('@type') not in ('Product','IndividualProduct'):continue
                title=str(o.get('name','')); sku=' '.join(str(o.get(k,'')) for k in ('sku','gtin','gtin13','mpn'))
                if not product_match(title+' '+sku,p):continue
                offers=o.get('offers') or {}
                if isinstance(offers,list):offers=offers[0] if offers else {}
                pr=money(offers.get('price') or offers.get('lowPrice'))
                if pr:
                    av=str(offers.get('availability','')).split('/')[-1] or 'nieznana'
                    return pr,av,urljoin(base,o.get('url') or offers.get('url') or base),title
        except:pass
    return None

def cards(page,selectors,p):
    for card_sel,title_sel,price_sel,link_sel in selectors:
        loc=page.locator(card_sel)
        for i in range(min(loc.count(),30)):
            card=loc.nth(i)
            try:
                text=card.inner_text(timeout=1500)
                if not product_match(text,p):continue
                title=card.locator(title_sel).first.inner_text(timeout=1000) if title_sel else text[:160]
                raw=card.locator(price_sel).first.inner_text(timeout=1000)
                pr=money(raw)
                if not pr:continue
                href=card.locator(link_sel).first.get_attribute('href',timeout=1000) if link_sel else None
                return pr,'nieznana',urljoin(page.url,href or page.url),title
            except:continue
    return None

def run(page,p,shop,kind,url_template,selectors):
    last='';last_msg='brak wyniku'
    for q in queries(p):
        last=url_template.format(q=quote_plus(q))
        try:
            resp=page.goto(last,wait_until='domcontentloaded',timeout=30000);page.wait_for_timeout(1800)
            if blocked(resp): return result(p,shop,kind,'zablokowano',last,message=f'HTTP {resp.status}')
            found=jsonld(page.content(),page.url,p)
            if found:return result(p,shop,kind,'ok',found[2],found[0],found[1],found[3],'JSON-LD','', 'wysoka')
            found=cards(page,selectors,p)
            if found:return result(p,shop,kind,'ok',found[2],found[0],found[1],found[3],'karta produktu','', 'średnia')
            last_msg=f'brak dopasowanej karty dla {q}'
        except Exception as e:last_msg=str(e)[:180]
    return result(p,shop,kind,'brak',last,message=last_msg)
