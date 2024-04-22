#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install pandas')
get_ipython().system('pip install requests')
get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install plotly')


# In[2]:


import yfinance as yf

# テスラの株価データの取得
tesla_stock_data = yf.download("TSLA", start="2020-01-01", end="2023-01-01")
print(tesla_stock_data.head())


# In[4]:


import requests
from bs4 import BeautifulSoup
import pandas as pd  # pandasをインポートする

def scrape_yahoo_finance(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/history"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find('table').find_all('tr')

    data = []
    for row in rows[1:]:  # ヘッダーを除外
        cols = row.find_all('td')
        if len(cols) > 1:  # 正しいデータ行のみを抽出
            date = cols[0].text.strip()
            close = cols[4].text.strip()
            data.append([date, close])

    return pd.DataFrame(data, columns=['Date', 'Close'])

# テスラの収益データを取得して表示
tesla_revenue_data = scrape_yahoo_finance("TSLA")
print(tesla_revenue_data.head())


# In[5]:


# GameStopの株価データの取得
gme_stock_data = yf.download("GME", start="2020-01-01", end="2023-01-01")
print(gme_stock_data.head())



# In[6]:


import plotly.graph_objects as go

def create_dashboard(stock_data, revenue_data, stock_name):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f"{stock_name} Stock Price", f"{stock_name} Revenue Data"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], name='Close Price'), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data['Date'], y=revenue_data['Close'], name='Close Price'), row=2, col=1)
    fig.update_layout(height=800, showlegend=True, title=f"{stock_name} Dashboard")
    fig.show()

create_dashboard(tesla_stock_data, tesla_revenue_data, "Tesla")


# In[7]:


create_dashboard(gme_stock_data, gme_revenue_data, "GameStop")


# In[8]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_yahoo_finance(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/history"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 仮にtableのクラスが確認できれば、そのクラスを指定します
    # 例: <table class="W(100%) M(0)">
    table = soup.find('table', {'class': 'W(100%) M(0)'})
    if not table:
        # テーブルが見つからなかった場合、別の手段を試す
        print("Table not found, checking for JSON data...")
        # JSONデータがスクリプトタグ内に埋め込まれているかもしれない
        scripts = soup.find_all('script')
        for script in scripts:
            if 'root.App.main' in script.text:
                json_data = script.text.split('root.App.main = ')[1]
                json_data = json_data.split(';\n}(this));')[0]
                return pd.read_json(json_data)  # JSONから直接DataFrameを作成
        return pd.DataFrame()  # JSONも見つからない場合は空のDataFrameを返す

    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            date = cols[0].text.strip()
            close = cols[4].text.strip()
            data.append([date, close])

    return pd.DataFrame(data, columns=['Date', 'Close'])

# テスラの収益データを取得して表示
tesla_revenue_data = scrape_yahoo_finance("TSLA")
print(tesla_revenue_data.head())


# In[9]:


# GameStopの株価データをダウンロード
gme_stock_data = yf.Ticker("GME")
gme_hist = gme_stock_data.history(period="max")  # 使用可能な全期間のデータを取得

print(gme_hist.head())  # 最初のデータを表示


# In[10]:


import plotly.graph_objects as go

# ダッシュボードの作成
fig = go.Figure()

# テスラ株価のグラフ追加
fig.add_trace(go.Scatter(x=tesla_hist.index, y=tesla_hist['Close'], name='Tesla Close Price'))

fig.update_layout(title='Tesla Stock Performance', xaxis_title='Date', yaxis_title='Close Price')
fig.show()


# In[11]:


# ダッシュボードの作成
fig = go.Figure()

# GameStop株価のグラフ追加
fig.add_trace(go.Scatter(x=gme_hist.index, y=gme_hist['Close'], name='GameStop Close Price'))

fig.update_layout(title='GameStop Stock Performance', xaxis_title='Date', yaxis_title='Close Price')
fig.show()


# In[12]:


import yfinance as yf
import plotly.graph_objects as go

# テスラの株式データをダウンロード
tesla_stock_data = yf.Ticker("TSLA")
tesla_hist = tesla_stock_data.history(period="max")  # 使用可能な全期間のデータを取得

# ダッシュボードの作成
fig = go.Figure()

# テスラ株価のグラフ追加
fig.add_trace(go.Scatter(x=tesla_hist.index, y=tesla_hist['Close'], name='Tesla Close Price'))

fig.update_layout(title='Tesla Stock Performance', xaxis_title='Date', yaxis_title='Close Price')
fig.show()


# In[ ]:




