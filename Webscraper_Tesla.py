#!/usr/bin/env python
# coding: utf-8

# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# In[3]:


get_ipython().system('pip install yfinance')
#!pip install pandas
#!pip install requests
get_ipython().system('pip install bs4')
#!pip install plotly


# In[4]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ## Define Graphing Function
# 

# In[5]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# 

# In[54]:


tesla=yf.Ticker('TSLA')


# In[55]:


tesla_data=tesla.history(period="max")


# In[56]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# In[93]:


url=" https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue."
html_data=requests.get(url).text


# In[94]:


beautiful_soup=BeautifulSoup(html_data,"html5lib")


# In[98]:


tables=beautiful_soup.find_all("table")
for index,table in enumerate(tables):
    if("Tesla Quarterly Revenue" in str(table)):
        table_index=index
tesla_revenue=pd.DataFrame(columns=["Date","Revenue"])

for row in tables[1].tbody.find_all('tr'):
    col=row.find_all("td")
    if(col!=[]):
        date=col[0].text
        revenue=col[1].text.strip().replace("$","").replace(",","")
        tesla_revenue=tesla_revenue.append({"Date":date,"Revenue":revenue},ignore_index=True)
tesla_revenue.head()


# In[99]:


print(tesla_revenue)

tesla_revenue.dropna(inplace=True)
not_empty=tesla_revenue["Revenue"]!=""
tesla_revenue=tesla_revenue[not_empty]


# In[100]:


tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract Stock Data
# 

# In[62]:


gmestop=yf.Ticker("GME")


# In[63]:


gme_data=gmestop.history(period="max")


# In[68]:


gme_data.reset_index(inplace=True)
gme_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# In[69]:


url="https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue."
html_data=requests.get(url).text


# In[73]:


beautiful_soup=BeautifulSoup(html_data,"html.parser")


# In[81]:


tables=beautiful_soup.find_all("table")
for index,table in enumerate(tables):
    if(str(table)=="GameStop Quarterly Revenue"):
        table_index=index

gme_revenue=pd.DataFrame(columns=["Date","Revenue"])

for row in tables[1].tbody.find_all("tr"):
    col=row.find_all("td")
    if(col!=[]):
        date=col[0].text
        revenue=col[1].text.replace("$","").replace(",","")
        gme_revenue=gme_revenue.append({"Date":date,"Revenue":revenue},ignore_index=True)
gme_revenue.head()


# In[82]:


gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph
# 

# In[87]:


make_graph(tesla_data,tesla_revenue,'Tesla')


# ## Question 6: Plot GameStop Stock Graph
# 

# In[88]:


make_graph(gme_data,gme_revenue,'GameStop')

