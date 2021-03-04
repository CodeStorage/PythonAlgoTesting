import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import timedelta, date

def daterange(start_date, end_date):
   for n in range(int((end_date - start_date).days)):
      yield start_date + timedelta(n)

def SimpleMovingAverage(security_dataframe,long_term_period,short_term_period):
    if len(security_dataframe) < long_term_period:
        return "FAIL"
    dfsize = len(security_dataframe)
    long_term_average = security_dataframe[dfsize-long_term_period:].Close.mean()
    short_term_average = security_dataframe[dfsize-short_term_period:].Close.mean()
    #print "long_term_average \n", security_dataframe[dfsize-long_term_period:].Close,len(security_dataframe[dfsize-long_term_period:].Close)
    #print "short_term_average \n", security_dataframe[dfsize-short_term_period:].Close

    prev_long_term_average = security_dataframe[dfsize-long_term_period-1:-1].Close.mean()
    prev_short_term_average = security_dataframe[dfsize-short_term_period-1:-1].Close.mean()
    #print "prev_long_term_average \n", security_dataframe[dfsize-long_term_period-1:-1].Close,len(security_dataframe[dfsize-long_term_period-1:-1].Close)
    #print "prev_short_term_average \n", security_dataframe[dfsize-short_term_period-1:-1].Close

    #print prev_long_term_average, prev_short_term_average, long_term_average, short_term_average
    if short_term_average > long_term_average:
        if prev_short_term_average < prev_long_term_average:
            print short_term_average, " > ",long_term_average, "AND", prev_short_term_average, " < ", prev_long_term_average
            return "BUY"
    if short_term_average < long_term_average:
        if prev_short_term_average > prev_long_term_average:
            print short_term_average, " < ",long_term_average, "AND", prev_short_term_average, " > ", prev_long_term_average
            return "SELL"
    return "NO_ACTION"
 

plotData = pd.DataFrame(columns=["date","action","price","ltsma","stsma"])
start_date = date(2020,1,1)
end_date = start_date + timedelta(365) 
for single_date in daterange(start_date,end_date):
    history_date = single_date-timedelta(365)
    googl = yf.download("GOOGL",history_date,single_date)
    df = pd.DataFrame(googl)
    #print df.tail(25)
    action = SimpleMovingAverage(df,200,50)
    if action != "NO_ACTION":
        print  single_date,action
    else:
        print single_date,action
    
    row_to_add = pd.Series({'date':single_date,'action':action,'price':df.tail(1).Close.item(),"ltsma":df[-200:].Close.mean(),"stsma":df[-50:].Close.mean()},name=len(plotData))
    plotData = plotData.append(row_to_add)
#print(df.head(5))
#print(df.tail(100).mean())
#print(df.shape)
#print(df.columns)
#print(df['Volume'][:2])
#print(df.describe())
#print(df.Volume)
#print plotData
plt.plot(plotData.date,plotData.ltsma,'b-', label="ltsma")
plt.plot(plotData.date,plotData.stsma, 'r-', label='stsma')
plt.plot(plotData.date,plotData.price, 'g-', label='price')
#plt.plot(plotData.date,plotData.price, 'g-', label='price')
plt.legend()
plt.show()

