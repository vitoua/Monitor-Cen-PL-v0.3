import io
import pandas as pd
import streamlit as st
from playwright.sync_api import sync_playwright
from parsers.registry import PARSERS
st.set_page_config(page_title='Monitor Cen PL',page_icon='💰',layout='wide')
st.title('Monitor Cen PL');st.caption('v0.3 • dedykowany parser dla każdego źródła • walidacja dopasowania i ceny')
def load(f):
 d=pd.read_excel(f,dtype=str).fillna('');d.columns=[str(c).strip().upper() for c in d.columns]
 if 'PN' not in d:raise ValueError('Plik musi zawierać PN')
 for c in ['EAN','NAZWA']:
  if c not in d:d[c]=''
 return d[['PN','EAN','NAZWA']][d.PN.str.strip()!=''].drop_duplicates('PN')
def excel(d):
 b=io.BytesIO();valid=d[d.status=='ok'].copy();low=valid.sort_values(['pn','cena']).groupby('pn',as_index=False).first() if not valid.empty else valid
 quality=d.groupby('zrodlo').agg(proby=('pn','count'),poprawne=('status',lambda x:(x=='ok').sum()),zablokowane=('status',lambda x:(x=='zablokowano').sum())).reset_index();quality['skutecznosc']=quality.poprawne/quality.proby
 with pd.ExcelWriter(b,engine='openpyxl') as w:
  d.to_excel(w,index=False,sheet_name='Wszystkie');valid[valid.typ=='retail'].to_excel(w,index=False,sheet_name='Retail');valid[valid.typ=='marketplace'].to_excel(w,index=False,sheet_name='Marketplace');low.to_excel(w,index=False,sheet_name='Najniższe ceny');quality.to_excel(w,index=False,sheet_name='Jakość źródeł')
 return b.getvalue()
u=st.file_uploader('Wgraj XLSX',type=['xlsx']);demo=st.checkbox('Użyj products.xlsx',value=u is None)
try:d=load(u if u else 'products.xlsx') if (u or demo) else pd.DataFrame()
except Exception as e:st.error(str(e));st.stop()
if not d.empty:
 st.success(f'Wczytano produktów: {len(d)}');st.dataframe(d,use_container_width=True,height=220)
 selected=st.multiselect('Źródła',list(PARSERS),default=list(PARSERS));limit=st.number_input('Limit produktów',1,len(d),min(2,len(d)))
 if st.button('Uruchom skan',type='primary',disabled=not selected):
  rows=[];bar=st.progress(0);total=int(limit)*len(selected);done=0
  with st.spinner('Skanowanie...'):
   with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']);ctx=browser.new_context(locale='pl-PL',timezone_id='Europe/Warsaw',viewport={'width':1365,'height':900});page=ctx.new_page()
    for _,r in d.head(int(limit)).iterrows():
     p=r.to_dict()
     for source in selected:
      rows.append(PARSERS[source](page,p));done+=1;bar.progress(done/total)
    ctx.close();browser.close()
  st.session_state.result=pd.DataFrame(rows)
if 'result' in st.session_state:
 r=st.session_state.result;c1,c2,c3,c4=st.columns(4);c1.metric('Rekordy',len(r));c2.metric('Poprawne',int((r.status=='ok').sum()));c3.metric('Zablokowane',int((r.status=='zablokowano').sum()));c4.metric('Źródła',r.zrodlo.nunique())
 t1,t2,t3,t4=st.tabs(['Wszystkie','Poprawne','Problemy','Jakość źródeł']);t1.dataframe(r,use_container_width=True);t2.dataframe(r[r.status=='ok'],use_container_width=True);t3.dataframe(r[r.status!='ok'],use_container_width=True)
 q=r.groupby('zrodlo').agg(proby=('pn','count'),poprawne=('status',lambda x:(x=='ok').sum()),zablokowane=('status',lambda x:(x=='zablokowano').sum())).reset_index();q['skuteczność %']=(100*q.poprawne/q.proby).round(1);t4.dataframe(q,use_container_width=True)
 st.download_button('Pobierz raport Excel',excel(r),'raport_cen_v03.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
