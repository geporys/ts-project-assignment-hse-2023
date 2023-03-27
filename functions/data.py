import requests
import pandas as pd
import yfinance as yf

def get_NIC_from_yFinance():
    nic = yf.Ticker("NIC.AX")
    nic_df = nic.history(start="2018-10-31")
    nic_df = nic_df.asfreq(freq='B', method='ffill').fillna(method='ffill')
    nic_df = nic_df[:'2022-09-30']
    return nic_df

def get_NIC_from_csv():
    nic_df = pd.read_csv('NICStockPriceMonthly.csv')
    nic_df['Date'] = [pd.Timestamp(t, tz='Australia/Sydney') for t in nic_df['Date']]
    #df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, utc=True)
    nic_df.set_index('Date', inplace=True)
    nic_df.drop(columns=['Open', 'High', 'Low'], inplace=True)
    return nic_df

def get_nickel_data_from_businessinsider(nic_df):
    r = requests.get('https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Commodity&tkData=300002,10,0,333&from=20170817&to={0}'.format(nic_df.index[-1].strftime('%Y%m%d')))
    nickelHist = pd.DataFrame(r.json())
    nickelHist['Date'] = [pd.Timestamp(t, tz='Australia/Sydney') for t in nickelHist['Date']]
    nickelHist.index = nickelHist['Date']
    nickelHist = nickelHist[nickelHist.index >= nic_df.index[0]]
    nickelHist = nickelHist.asfreq(freq='B', method='ffill').fillna(method='ffill')
    nic_df = nic_df[nic_df.index <= nickelHist.index[-1]]

    return nic_df, nickelHist

def get_rates(nic_df):
    rates = pd.DataFrame(data=[
        {'date': nic_df.index[-1].strftime('%m/%d/%Y'),	'rate': 3.60},
#         {'date': "03/08/2023",	'rate': 3.60},
#         {'date': "02/08/2023",	'rate': 3.35},
#         {'date': "12/07/2022",	'rate': 3.10},
#         {'date': "11/02/2022",	'rate': 2.85},
#         {'date': "10/05/2022",	'rate': 2.60},
        {'date': "09/07/2022",	'rate': 2.35},
        {'date': "08/03/2022",	'rate': 1.85},
        {'date': "07/06/2022",	'rate': 1.35},
        {'date': "06/08/2022",	'rate': 0.85},
        {'date': "05/04/2022",	'rate': 0.35},
        {'date': "11/04/2020",	'rate': 0.10},
        {'date': "03/20/2020",	'rate': 0.25},
        {'date': "03/04/2020",	'rate': 0.50},
        {'date': "10/02/2019",	'rate': 0.75},
        {'date': "07/03/2019",	'rate': 1.00},
        {'date': "06/05/2019",	'rate': 1.25},
        {'date': "08/03/2016",	'rate': 1.50}
    ] )
    rates['date'] = [pd.Timestamp(t, tz='Australia/Sydney') for t in rates['date']]
    rates.index = rates['date']
    rates = rates.drop(columns=['date'])
    rates = rates.asfreq(freq='B').fillna(method='ffill')
    rates = rates[rates.index >= nic_df.index[0]]
    return rates

def union_data_in_one_df(nick, rates, nic, currency, production, mining, indonesia_metal_products):
    data  = pd.DataFrame(data={
        'NIC': nic['Close'], 
        'Nickle price': nick['Close'], 
        'Rate': rates['rate'], 
        'AUD/IDR': currency['Close'],
        'NPI production': production['value'],
        'Mining': mining['value'],
        'Metal products in indonesia': indonesia_metal_products['Base metal products']
    }, index=nic.index)
    
    data = data.asfreq(freq='W-FRI').fillna(method='ffill')
    
    return data

def get_endog_and_exog(data):
    endog = 'NIC'
    exog = list(filter(lambda column: column != endog, data.columns))
    
    return (endog, exog)

def get_AUDIDR_from_yFinance():
    currency = yf.Ticker("AUDIDR=X")
    currency_df = currency.history(start="2018-10-31", end="2022-12-31")
    currency_df = currency_df.tz_convert('Australia/Sydney')
    currency_df = currency_df[currency_df['Close'] > 7600]
    currency_df = currency_df.asfreq(freq='B', method='ffill').fillna(method='ffill')
    currency_df.index = currency_df.index.normalize()
    return currency_df

def get_AUDIDR_from_csv():
    currency_df = currency_df
