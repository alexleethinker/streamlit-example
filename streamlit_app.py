import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
import wencai as wc
from wencai.core.session import Session

Session.headers.update({'Host':'www.iwencai.com'})
wc.set_variable(cn_col=True)

import warnings
warnings.filterwarnings('ignore')


concepts = wc.search( query = "概念 主营").fillna('')

import pandas as pd
concepts_list = pd.read_csv('./Concepts_List.csv',encoding="gbk")
industry_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['行业'])]['概念名称'].values.tolist()
events_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['事件','知名企业','农村','改革','军工','国企体系'])]['概念名称'].values.tolist()
trading_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['交易'])]['概念名称'].values.tolist() # 区域missing


concepts['行业概念'] = ''
concepts['事件概念'] = ''
concepts['交易概念'] = ''

concept_list = []

for row, l in concepts.iterrows():
    concepts['行业概念'][row] = ','.join(set(l['所属概念'].replace('概念','').split(';')).intersection(industry_concepts_list))
    concepts['事件概念'][row] = ','.join(set(l['所属概念'].replace('概念','').split(';')).intersection(events_concepts_list))
    concepts['交易概念'][row] = ','.join(set(l['所属概念'].replace('概念','').split(';')).intersection(trading_concepts_list))
    concept_list = concept_list + l['所属概念'].replace('概念','').split(';')

concepts['a股市值(不含限售股)'] = pd.to_numeric(concepts['a股市值(不含限售股)'])/100000000

code = concepts.pop('股票代码')
name = concepts.pop('股票简称')

concepts = concepts.drop(columns=['公司网站','经营范围','所属概念','主营产品名称','所属概念数量']).round(2).\
            rename(columns = {'a股市值(不含限售股)':'流通市值'})
concepts.insert(0,'股票简称',name)
concepts.insert(0,'股票代码',code)


st.dataframe(concepts)
