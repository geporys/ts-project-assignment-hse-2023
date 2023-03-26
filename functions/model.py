import statsmodels.api as sm
import matplotlib.pyplot as plt
from data import get_endog_and_exog

def first_model(data):
    train_data = data[data.index < '2022-08-21']
    test_data = data[data.index >= '2022-08-21'] 
    
    (endog, exog) = get_endog_and_exog(data)
    
    mod = sm.tsa.arima.ARIMA(order=(4, 1, 1), endog=train_data[endog], exog=train_data[exog], freq="B")
    res = mod.fit()
    
    print(res.summary())
    
    fig, ax = plt.subplots(figsize=(15, 5))
    
    train_data[endog].plot(ax=ax)
    
    res.fittedvalues.plot(ax=ax)
    
    predicted_value = res.get_prediction(test_data.index[0], test_data.index[-1], exog=test_data[exog]).summary_frame()
    
    predicted_value['mean'].plot(ax=ax, style='k--')
    ax.fill_between(predicted_value.index, predicted_value['mean_ci_lower'], predicted_value['mean_ci_upper'], color='k', alpha=0.1);
    
    fig, ax = plt.subplots(figsize=(15, 5))
    data[endog]["2022-01-20":"2022-08-21"].plot(ax=ax)
    predicted_value['mean'].plot(ax=ax, color='red')
    ax.fill_between(
        predicted_value.index, 
        predicted_value['mean_ci_lower'], 
        predicted_value['mean_ci_upper'], 
        color='k',
        alpha=0.1);
    
    from statsmodels.tools.eval_measures import meanabs, mse, rmse
    
    print('meanabs', meanabs(test_data[endog], predicted_value['mean']))
    print('mse', mse(test_data[endog], predicted_value['mean']))
    print('rmse', rmse(test_data[endog], predicted_value['mean']))
    
    return res