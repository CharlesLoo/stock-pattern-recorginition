import requests
import csv
import re
import pandas as pd
import datetime
import numpy as np
import urllib
import os 

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick2_ohlc
from datetime import timezone



def get_google_data(ticker, period, days):

    url = 'https://finance.google.com/finance/getprices?p={}Y&f=d,o,h,l,c,v&q={}&i={}'.format(days, ticker, period)

    doc = requests.get(url)
    data = csv.reader(doc.text.splitlines())
    data1 = csv.reader(doc.text.splitlines())
    #save file
    path = 'text/';
    file_name = path + ticker+'_'+str(days)+'Y'+'.csv';
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data1)
    
    columns = ['Date','Close', 'High', 'Low', 'Open', 'Volume']
    rows = []
    rows_timestamp = []
    stuff_timestamp = []
    times = []
    for row in data:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]),timezone.utc)
                times.append(start)
            else:
                time = start+datetime.timedelta(seconds=period*int(row[0]))
                times.append(time)
                
                #change to toordinal
                timestamp = time.replace(tzinfo=timezone.utc).timestamp()
                #timestamp = time.
                single_row = [timestamp] + list(map(float, row[1:]))
                rows_timestamp.append(single_row)
                rows.append([time] + list(map(float, row[1:])))

    if len(rows):
        #stuff = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'), columns=columns)
        stuff_timestamp = pd.DataFrame(rows_timestamp, columns=columns)
        stuff = pd.DataFrame(rows, columns=columns)
    else:
        #stuff = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
        stuff_timestamp = pd.DataFrame(rows_timestamp)
        stuff = pd.DataFrame(rows)
    return stuff_timestamp, stuff

def save_file(path,file_name,data):
    #np.savetxt(path+'/'+file_name, data, delimiter=",")
    data.to_csv(path+'/'+file_name, index=True, header=True)

#functions for visual data
def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    

def draw_one_picture(data,name,epco_num,time):

    fig = plt.figure(figsize=(8, 6))
    ax1 = plt.subplot2grid((1,1), (0,0))
   
    candlestick2_ohlc(ax1, data['Open'],data['High'],data['Low'],data['Close'], width=0.4, colorup='#77d879', colordown='#db3f3f')

    #for label in ax1.xaxis.get_ticklabels():
    #    label.set_rotation(45)

    xdate = [datetime.datetime.fromtimestamp(i) for i in data['Date']]
    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''  
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))    

    #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

    fig.autofmt_xdate()
    #fig.tight_layout()

    #ax1.grid(True)
    

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(ticker)
    #plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

    #save figure
    file_name = r'figures/'+ticker+'/'+ticker+'_'+str(time)+'Y_'+str(epco_num)+'.jpg';
    plt.savefig(file_name,bbox_inches='tight')
    #plt.show()
    plt.close()

def draw_pictures(ticker,name,time,period,window_size):
    if os.path.exists(r'figures/'+name) == False:
       os.mkdir(r'figures/'+name)
    if os.path.exists(r'labels/'+name) == False:
       os.mkdir(r'labels/'+name)

    #print(ticker)
    #every hour has 3600 seconds, sequence size is 'period', there are 3600 / peroid sequence in 1h, every day has 6.5 hour data, then in the window has (3600 / period) * 6.5 * window_size recored data. Each step size is 1 day. 
    size = int((3600 / period) * 6.5 * window_size)
    step_size = int((3600 / period) * 6.5)
    rows = []
    columns = ['Date','Close', 'High', 'Low', 'Open']
    epco_num = 1;
    current_size = 0
    index = 0
    while(index < len(ticker)):
        if current_size < size:
            rows.append(ticker.loc[index].values[0:-1])
            current_size = current_size + 1
            index = index + 1
            #print("current_size....."+str(current_size))
        else:
           if(len(rows) >= size):
               print("drawing pictures.....")
               epco = pd.DataFrame(rows, columns=columns)
               #draw one picture
               draw_one_picture(epco,name,epco_num,time)
               
               #reset the index
               index = step_size * epco_num
               epco_num = epco_num + 1
               rows = []
               current_size = 0
               #check whther left data is enough to draw another picture  

if __name__ == "__main__":
    tickers = ('AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL',
'AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'MSFT', 'GOOG','ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA', 'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS')
   
    for i in range (0,1):
       ticker = tickers[i];
       period = 600;
 
       #total history data time, 1 year
       time = 2;
       #windows size, days
       window_size = 7;

       data_timestamp, data = get_google_data(ticker,period,time);
    
       #save file
       path = 'text_time';
       file_name = ticker+'_'+str(time)+'Y'+'.txt';
       save_file(path,file_name,data);

       #visual data
       draw_pictures(data_timestamp,ticker,time,period,window_size)
    



    
