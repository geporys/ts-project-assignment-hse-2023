import requests
import pandas as pd
import yfinance as yf

def get_NIC_from_yFinance():
    nic = yf.Ticker("NIC.AX")
    nic_df = nic.history(period="max")
    nic_df = nic_df.asfreq(freq='B', method='ffill').fillna(method='ffill')
    nic_df = nic_df[:'2023-01-01']
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
        {'date': "12/07/2022",	'rate': 3.10},
        {'date': "11/02/2022",	'rate': 2.85},
        {'date': "10/05/2022",	'rate': 2.60},
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

def union_data_in_one_df(nick, rates, nic):
    data  = pd.DataFrame(data={'NIC': nic['Close'], 'Nickle price': nick['Close'], 'Rate': rates['rate']}, index=nic.index)
    
    return data

def get_endog_and_exog(data):
    endog = 'NIC'
    exog = list(filter(lambda column: column != endog, data.columns))
    
    return (endog, exog)


