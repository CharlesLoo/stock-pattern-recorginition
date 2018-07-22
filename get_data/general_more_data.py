#this file is to general some more trainning data which has Head and Shoulder through vrriation of read data


#import requests
import csv
import re
import pandas as pd
import datetime
import numpy as np
#import urllib
import os 
import random

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick2_ohlc
from datetime import timezone


def draw_one_picture(data,name,des_file):

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
    plt.title(name)
    #plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

    #save figure
    file_name = des_file +'/' + name+'.jpg';
    plt.savefig(file_name,bbox_inches='tight')
    #plt.show()
    plt.close()

def draw_figures(text_path,variation_images):
    files = os.listdir(text_path)
    for file_name in files:
        file_full_name = os.path.join(text_path,file_name)  
        pic_name = file_name[0:file_name.index('.csv')]    
        with open(file_full_name) as f:
             data = csv.reader(f)
             columns = ['Date','Close', 'High', 'Low', 'Open']
             rows = []
             times = []
             for row in data:
                 rows.append(list(map(float,row)))
             epco = pd.DataFrame(rows, columns=columns)
             draw_one_picture(epco,pic_name,variation_images)

#read history data from csv files
def read_data(file_full_name, period, days):
    with open(file_full_name) as f:
         data = csv.reader(f)
    
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
                    #change to toordinal
                    timestamp = start.replace(tzinfo=timezone.utc).timestamp()
                    #timestamp = time.
                    single_row = [timestamp] + list(map(float, row[1:]))
                    rows_timestamp.append(single_row)
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
    #print(stuff_timestamp)
    #print(stuff)
    return stuff_timestamp, stuff
def save_one_related_data(data,name,text_path):
    file_name = name+'.csv'
    data.to_csv(text_path+'/'+file_name, index=False, header=False)

def save_related_data(ticker,name,time,period,window_size,epcos,original_text_path):
    #print(ticker)
    #every hour has 3600 seconds, sequence size is 'period', there are 3600 / peroid sequence in 1h, every day has 6.5 hour data, then in the window has (3600 / period) * 6.5 * window_size recored data. Each step size is 1 day. 
    size = int((3600 / period) * 6.5 * window_size)
    step_size = int((3600 / period) * 6.5)
    rows = []
    columns = ['Date','Close', 'High', 'Low', 'Open' 'Volume']
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
               for ep in epcos:
                   if str(epco_num) == ep: 
                       print("saving data.....")
                       epco = pd.DataFrame(rows, columns=columns)
                       print(epcos)
                       save_one_related_data(epco,name+'_'+str(time)+'Y_'+str(epco_num),original_text_path)
               #reset the index
               index = step_size * epco_num
               epco_num = epco_num + 1
               rows = []
               current_size = 0
               #check whther left data is enough to draw another picture  


#read labels
def read_labels(train_label_csv_path):
    with open (train_label_csv_path) as f:
        data = csv.reader(f)
        train_label = []
        start = 1
        for row in data:
            if start == 1:
                #skip
                start = 0
            else:
                train_label.append(row)
        #sort according first colmun
        train_label.sort(key = lambda x:x[0])
        return train_label

#find related data of those images (those data with "Head and should") from history data
def find_related_data(train_label, period, days,window_size,original_text_path):
    current_ticker = ""
    epcos = []
    for row in train_label:
           #get ticker name
           ticker = row[0][0:row[0].index('_')]
           if current_ticker == "":
              current_ticker = ticker
              epco = row[0][row[0].index('_2Y_')+4:row[0].index('.jpg')]
              text_name = current_ticker + "_2Y.csv"
              test_full_name = os.path.join(text_path,text_name)
              epcos.append(test_full_name)
              epcos.append(epco)
           elif ticker == current_ticker:
              epco = row[0][row[0].index('_2Y_')+4:row[0].index('.jpg')]
              epcos.append(epco)
           else:
              data_timestamp,data = read_data(epcos[0], period, days)
              save_related_data(data_timestamp,current_ticker,time,period,window_size,epcos,original_text_path)
              #reset
              current_ticker = ticker
              epcos = []
              epco = row[0][row[0].index('_2Y_')+4:row[0].index('.jpg')]
              text_name = current_ticker + "_2Y.csv"
              test_full_name = os.path.join(text_path,text_name)
              epcos.append(test_full_name)
              epcos.append(epco)       

#def find the data postion of pattern part in original data
def find_pattern_data(label_information,period,window_size):
    size = int((3600 / period) * 6.5 * window_size)
    #140   760
    x1_ps = label_information[4] 
    x2_ps = label_information[6]
    index1 = round(size * (float(x1_ps) - 140) / (760 - 140))
    index2 = round(size * (float(x2_ps) - 140) / (760 - 140))
    if index2 > (size - 1):
       index2 = size - 1

    return index1,index2
   
def get_random_val(max_val, min_val,a,b):
    r = random.randint(a,b) * 0.01 *(max_val-min_val)
    return r

#make the original pattern taller
def make_taller(epco,index1, index2,name,variation_text_path):
    size = int((3600 / period) * 6.5 * window_size)
    #find max and min value in this area
    max_val = epco.loc[index1].values[1]
    min_val = epco.loc[index1].values[1]
    
    for i in range (index1,index2+1):
        for j in range (1,5):
            val = epco.loc[i].values[j]
            if val > max_val:
               max_val = val
            if val < min_val:
               min_val = val
    columns = ['Date','Close', 'High', 'Low', 'Open']
    

    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values increase at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] + get_random_val(max_val, min_val,0,10);
        epco1['High'][i] = epco1['High'][i] + get_random_val(max_val, min_val,0,10);
        epco1['Low'][i] = epco1['Low'][i] + get_random_val(max_val, min_val,0,10);
        epco1['Open'][i] = epco1['Open'][i] + get_random_val(max_val, min_val,0,10);

        #save data
    name1 = name + "_taller_10"
    save_one_related_data(epco1,name1,variation_text_path)


    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values increase at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] + get_random_val(max_val, min_val,0,20);
        epco1['High'][i] = epco1['High'][i] + get_random_val(max_val, min_val,0,20);
        epco1['Low'][i] = epco1['Low'][i] + get_random_val(max_val, min_val,0,20);
        epco1['Open'][i] = epco1['Open'][i] + get_random_val(max_val, min_val,0,20);

        #save data
    name1 = name + "_taller_20"
    save_one_related_data(epco1,name1,variation_text_path)

#make the original pattern wider
def make_wider(epco,index1, index2,name,variation_text_path):
    size = int((3600 / period) * 6.5 * window_size)
    #find max and min value in this area
    max_val = epco.loc[index1].values[1]
    min_val = epco.loc[index1].values[1]
    
    for i in range (index1,index2+1):
        for j in range (1,5):
            val = epco.loc[i].values[j]
            if val > max_val:
               max_val = val
            if val < min_val:
               min_val = val
    columns = ['Date','Close', 'High', 'Low', 'Open']
    

    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,0,10);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,0,10);
        epco1['Low'][i] = epco1['Low'][i] - get_random_val(max_val, min_val,0,10);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,0,10);

        #save data
    name1 = name + "_wider_10"
    save_one_related_data(epco1,name1,variation_text_path)


    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 20% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,0,20);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,0,20);
        epco1['Low'][i] = epco1['Low'][i] -get_random_val(max_val, min_val,0,20);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,0,20);

        #save data
    name1 = name + "_wider_20"
    save_one_related_data(epco1,name1,variation_text_path)

#change data randomly
def r_change(epco,index1, index2,name,variation_text_path):
    size = int((3600 / period) * 6.5 * window_size)
    #find max and min value in this area
    max_val = epco.loc[index1].values[1]
    min_val = epco.loc[index1].values[1]
    
    for i in range (index1,index2+1):
        for j in range (1,5):
            val = epco.loc[i].values[j]
            if val > max_val:
               max_val = val
            if val < min_val:
               min_val = val
    columns = ['Date','Close', 'High', 'Low', 'Open']

    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['Low'][i] = epco1['Low'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,-5,5);

        #save data
    name1 = name + "_r_5_0"
    save_one_related_data(epco1,name1,variation_text_path)    

    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['Low'][i] = epco1['Low'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,-10,10);

        #save data
    name1 = name + "_r_10_0"
    save_one_related_data(epco1,name1,variation_text_path)


    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['Low'][i] = epco1['Low'][i] - get_random_val(max_val, min_val,-5,5);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,-5,5);

        #save data
    name1 = name + "_r_5_1"
    save_one_related_data(epco1,name1,variation_text_path)    

    epco1 = []
    rows = []
    for i in range (0,size): 
        row = []
        for j in range (0,5):
            row.append(epco.loc[i].values[j])
        rows.append(row)
    epco1 = pd.DataFrame(rows, columns=columns)
         
    #for all values decreas at most 10% of max-min
    for i in range (index1,index2+1):
        epco1['Close'][i] = epco1['Close'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['High'][i] = epco1['High'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['Low'][i] = epco1['Low'][i] - get_random_val(max_val, min_val,-10,10);
        epco1['Open'][i] = epco1['Open'][i] - get_random_val(max_val, min_val,-10,10);

        #save data
    name1 = name + "_r_10_1"
    save_one_related_data(epco1,name1,variation_text_path)


#change data randomly, this function dont need you to change you label by hand, it can adapt previous label and reuse it.
def r_change_auto(epco,beg, end,valley1,valley2,name,variation_text_path,label_information1):
    labels = []
    size = int((3600 / period) * 6.5 * window_size)
    #max and min vlaue in whole picture
    max_val_whole = epco.loc[0].values[1]
    min_val_whole = epco.loc[0].values[1]
    for i in range (0,size):
        for j in range (1,5):
            val = epco.loc[i].values[j]
            if val > max_val_whole:
               max_val_whole = val
            if val < min_val_whole:
               min_val_whole = val    
    #compute rate between value and coordinate
    rate = (max_val_whole - min_val_whole) / (430-50)

    #find max and min value in this area
    max_val = epco.loc[beg].values[1]
    min_val = epco.loc[beg].values[1]
    max_vals =  [max_val,max_val,max_val,max_val]
    min_vals =  [max_val,max_val,max_val,max_val]

    columns = ['Date','Close', 'High', 'Low', 'Open']
    for i in range (beg,end+1):
        for j in range (1,5):
            #max close
            if epco.loc[i].values[j] > max_vals[j-1]:
               max_vals[j-1] = epco.loc[i].values[j]
            if epco.loc[i].values[j] < min_vals[j-1]:
               min_vals[j-1] = epco.loc[i].values[j]

            val = epco.loc[i].values[j]
            if val > max_val:
               max_val = val
            if val < min_val:
               min_val = val


    for scale in [0.05]:  
        #each scale would save num new data
        repeat = 0
        total_repeat = 0
        num = 0
        saved = 0
        label_information = label_information1        
        while(num < 10 and repeat < 10 and total_repeat  < 20):
            if(repeat > 4):
              total_repeat = total_repeat + 1
            repeat = repeat + 1
            num = num + 1 
            epco1 = []
            rows = []
            for i in range (0,size): 
                row = []
                for j in range (0,5):
                    row.append(epco.loc[i].values[j])
                rows.append(row)
            epco1 = pd.DataFrame(rows, columns=columns) 
            
           
            for i in range (beg,end+1):
                #change differently
                #epco1['Close'][i] = epco1['Close'][i] + np.random.normal(scale = scale)  * (max_val - min_val)
                #epco1['High'][i] = epco1['High'][i] + np.random.normal(scale = scale)  * (max_val - min_val)
                #epco1['Low'][i] = epco1['Low'][i] + np.random.normal(scale = scale)   * (max_val - min_val)
                #epco1['Open'][i] = epco1['Open'][i] + np.random.normal(scale = scale)  * (max_val - min_val)
                
                #change together 
                change = np.random.normal(scale = scale)  * (max_val - min_val)
                epco1['Close'][i] = epco1['Close'][i] + change + np.random.normal(scale = 0.025)  * (max_vals[0] - min_vals[0])
                epco1['High'][i] = epco1['High'][i] + change + np.random.normal(scale = 0.025)  * (max_vals[1] - min_vals[1])
                epco1['Low'][i] = epco1['Low'][i] + change + np.random.normal(scale = 0.025)  * (max_vals[2] - min_vals[2])
                epco1['Open'][i] = epco1['Open'][i] + change + np.random.normal(scale = 0.025)  * (max_vals[3] - min_vals[3])
           

            #<beg,valley1>   first peak
            max_val_all = epco1.loc[beg].values[1]
            max_val_co = epco1.loc[beg].values[1]
            min_val_all = epco1.loc[beg].values[1]
            for i in range (beg,valley1+1):
                for j in range (1,5):
                    val = epco1.loc[i].values[j]
                    if val > max_val_all:
                       max_val_all = val
                    if val < min_val_all:
                       min_val_all = val
                    if j == 1 or j == 4:
                       if val > max_val_co:
                          max_val_co = val
            #<valley2,end>   third peak
            for i in range (valley2,end+1):
               for j in range (1,5):
                    val = epco1.loc[i].values[j]
                    if val > max_val_all:
                        max_val_all = val
                    if val < min_val_all:
                        min_val_all = val
                    if j == 1 or j == 4:
                        if val > max_val_co:
                           max_val_co = val
                #<valley1,valley2>   second peak
            vals_all = []
            vals_co = []
            for i in range (valley1,valley2+1):
                for j in range (1,5):
                    vals_all.append(epco1.loc[i].values[j])
                if j == 1 or j == 4:
                    vals_co.append(epco1.loc[i].values[j])
            vals_all.sort()
            vals_co.sort()
            #only save (1)top 2 of all values (low, high, open, close) in 2nd peak is great than the 1st and 3rd peak, (2) top 2 of all values (open, close) in 2nd peak is great than (open, close) in the 1st and 3rd peak,
            print("generating for....",name,beg,valley1,valley2,end)   
            if vals_all[-2] >  max_val_all  or vals_co[-2] >  max_val_co:
                   #adapt orginal positio
                   max_val_whole_new = epco1.loc[0].values[1]
                   min_val_whole_new = epco1.loc[0].values[1] 
                   for i in range (0,size):
                       for j in range (1,5):
                           val = epco1.loc[i].values[j]
                           if val > max_val_whole_new:
                               max_val_whole_new = val
                           if val < min_val_whole_new:
                               min_val_whole_new = val  

                   outed = 0
                   if max_val_whole_new > max_val_whole:
                       outed = max_val_whole_new - max_val_whole
                       for i in range (beg,end+1):
                           epco1['Close'][i] = epco1['Close'][i] - outed
                           epco1['High'][i] = epco1['High'][i] - outed
                           epco1['Low'][i] = epco1['Low'][i] - outed
                           epco1['Open'][i] = epco1['Open'][i] - outed
                   elif max_val_whole_new < max_val_whole:
                       outed = max_val_whole - max_val_whole_new
                       for i in range (beg,end+1):
                           epco1['Close'][i] = epco1['Close'][i] + outed
                           epco1['High'][i] = epco1['High'][i] + outed
                           epco1['Low'][i] = epco1['Low'][i] + outed
                           epco1['Open'][i] = epco1['Open'][i] + outed

                   
                   #check bot is out of original scale
                   max_val_whole_new = epco1.loc[0].values[1]
                   min_val_whole_new = epco1.loc[0].values[1] 
                   for i in range (0,size):
                       for j in range (1,5):
                           val = epco1.loc[i].values[j]
                           if val > max_val_whole_new:
                               max_val_whole_new = val
                           if val < min_val_whole_new:
                               min_val_whole_new = val  

                   bot_out = 0

                   if min_val_whole_new < min_val_whole:
                      bot_out = min_val_whole - min_val_whole_new
                      for i in range (beg,end+1):
                          epco1['Close'][i] = epco1['Close'][i] + bot_out
                          epco1['High'][i] = epco1['High'][i] + bot_out
                          epco1['Low'][i] = epco1['Low'][i] + bot_out
                          epco1['Open'][i] = epco1['Open'][i] + bot_out 
                   elif min_val_whole_new > min_val_whole:
                      bot_out = min_val_whole_new - min_val_whole
                      for i in range (beg,end+1):
                          epco1['Close'][i] = epco1['Close'][i] - bot_out
                          epco1['High'][i] = epco1['High'][i] - bot_out
                          epco1['Low'][i] = epco1['Low'][i] - bot_out
                          epco1['Open'][i] = epco1['Open'][i] - bot_out 

                   max_val_whole_new = epco1.loc[0].values[1]
                   min_val_whole_new = epco1.loc[0].values[1] 
                   for i in range (0,size):
                       for j in range (1,5):
                           val = epco1.loc[i].values[j]
                           if val > max_val_whole_new:
                               max_val_whole_new = val
                           if val < min_val_whole_new:
                               min_val_whole_new = val  

                   moved_down = 0
                   if max_val_whole_new < max_val_whole:
                       moved_down = max_val_whole - max_val_whole_new
                       for i in range (beg,end+1):
                           epco1['Close'][i] = epco1['Close'][i] + moved_down
                           epco1['High'][i] = epco1['High'][i] + moved_down
                           epco1['Low'][i] = epco1['Low'][i] + moved_down
                           epco1['Open'][i] = epco1['Open'][i] + moved_down 


                   moved_up = 0
                   if min_val_whole_new > min_val_whole:
                       moved_up = min_val_whole_new - min_val_whole
                       for i in range (beg,end+1):
                           epco1['Close'][i] = epco1['Close'][i] - moved_up
                           epco1['High'][i] = epco1['High'][i] - moved_up
                           epco1['Low'][i] = epco1['Low'][i] - moved_up
                           epco1['Open'][i] = epco1['Open'][i] - moved_up 

                   #remove gap
                   b = beg
                   if b == 0:
                      b = b + 1
                    
                   for i in range (b,end+1):
                              if epco1['Low'][i] > epco1['High'][i-1]:
                                  if epco1['Open'][i] < epco1['Close'][i]:
                                      gap = epco1['Open'][i] - epco1['High'][i-1]
                                      epco1['Open'][i] = epco1['Open'][i] - gap / 2
                                      epco1['Low'][i] = epco1['Low'][i] - gap/2
                                      epco1['High'][i-1] = epco1['High'][i-1] + gap/2
                                      if epco1['Open'][i-1] > epco1['Close'][i-1]:
                                          epco1['Open'][i-1] = epco1['Open'][i-1] + gap/2
                                      else:
                                          epco1['Close'][i-1] = epco1['Close'][i-1] + gap/2
                              elif epco1['Low'][i-1] > epco1['High'][i]:
                                  if epco1['Open'][i] > epco1['Close'][i]:
                                      gap = epco1['Low'][i-1] - epco1['Open'][i]
                                      epco1['Open'][i] = epco1['Open'][i] + gap / 2
                                      epco1['High'][i] = epco1['High'][i] + gap/2
                                      epco1['Low'][i-1] = epco1['Low'][i-1] - gap/2
                                      if epco1['Open'][i-1] < epco1['Close'][i-1]:
                                          epco1['Open'][i-1] = epco1['Open'][i-1] - gap/2
                                      else:
                                          epco1['Close'][i-1] = epco1['Close'][i-1] - gap/2


                   name1 = name + "_auto_" + str(scale) + "_" + str(saved)
                   print("saving file.....",name1)                        
                   save_one_related_data(epco1,name1,variation_text_path)
                   saved = saved + 1
                   repeat = 0 

                   #adapt label
                   file_name = name1+'.jpg'
                   wideth = label_information[1]
                   hight = label_information[2]
                   _class = label_information[3]
                   xmin =  label_information[4] 
                   xmax =  label_information[6]  
                        
                   #new coordinate of ymax is (new max value - old max) * rate + old ymax
                   ymin =  int(round(((min_val_all - outed + bot_out + moved_down - moved_up) - min_val) * rate + int(label_information[5]))) 
                   ymax =  int(round(((vals_all[-1] - outed+ bot_out + moved_down - moved_up) - max_val) * rate + int(label_information[7])))
                   label_information = [file_name,wideth,hight,_class,xmin,ymin,xmax,ymax,valley1,valley2] 
                   labels.append(label_information)

    return labels                        

#change data in x direction randomly, this function dont need you to change you label by hand, it can adapt previous label and reuse it.
def r_change_auto_x(epco,_beg, _end,_valley1,_valley2,name,variation_text_path,label_information1):
    labels = []
    size = int((3600 / period) * 6.5 * window_size)
    #max and min vlaue in whole picture
    max_val_whole = epco.loc[0].values[1]
    min_val_whole = epco.loc[0].values[1]
    for i in range (0,size):
        for j in range (1,5):
            val = epco.loc[i].values[j]
            if val > max_val_whole:
               max_val_whole = val
            if val < min_val_whole:
               min_val_whole = val    
    #compute rate between value and coordinate
    rate = (max_val_whole - min_val_whole) / (430-50)

    #find max and min value in this area
    max_val = epco.loc[_beg].values[1]
    min_val = epco.loc[_beg].values[1]
    max_vals =  [max_val,max_val,max_val,max_val]
    min_vals =  [max_val,max_val,max_val,max_val]

    columns = ['Date','Close', 'High', 'Low', 'Open']
    for i in range (_beg,_end+1):
        for j in range (1,5):
            #max close
            if epco.loc[i].values[j] > max_vals[j-1]:
               max_vals[j-1] = epco.loc[i].values[j]
            if epco.loc[i].values[j] < min_vals[j-1]:
               min_vals[j-1] = epco.loc[i].values[j]

            val = epco.loc[i].values[j]
            if val > max_val:
               max_val = val
            if val < min_val:
               min_val = val


    for scale in [0.5]:  
        #each scale would save num new data
        repeat = 0
        total_repeat = 0
        num = 0
        saved = 0
        label_information = label_information1        
        while(num < 31 and repeat < 10 and total_repeat  < 20):
     
            if(repeat > 4):
              total_repeat = total_repeat + 1
            repeat = repeat + 1
            num = num + 1 
            
            
            #find the change rate for 1st and 3rd peak, scale = 0.12, the range is (-60% -- 60%) scale = 0.15, the range is (-75% -- 75%)

            #keep change in 75%
            rate1 = np.random.normal(scale = scale)
            while( rate1 > 1 or rate1 < -0.7 ):
                 rate1 = np.random.normal(scale = scale)

            rate3 = np.random.normal(scale = scale)
            while( rate3 > 1 or rate3 < -0.7 ):
                 rate3 = np.random.normal(scale = scale)

            valley1 = _valley1
            valley2 = _valley2
            end = _end
            beg = _beg
            len1 = valley1 - beg
            len2 = valley2 - valley1
            len3 = end - valley2 
            
            #actual change for each part
            change1 = int(rate1 * len1);
            change3 = int(rate3 * len3);
            change2 = -(change1 + change3);
            #print("generating for....",name,beg,valley1,valley2,end,len1,len2,len3,change1,change2,change3,rate1,rate3)
            failure = 0;
            #check whether change2 is too much
            if change2 < (-len2 * 0.7) or change2 > len2 :
               failure = 1
            #nothing changed
            if change1 == 0 and change2==0 and change3 == 0 :
               failure = 1
            if (failure == 0):
               epco1 = []
               rows = [] 
               
               for i in range (0,size): 
                    row = []
                    for j in range (0,5):
                        row.append(epco.loc[i].values[j])
                    rows.append(row)
               

               
               #change the 1st peak
               #remove
               if change1 < 0:
                    step = abs(int(len1 / change1))
                     
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(beg,valley1-1)
                    for i in range(0,abs(change1)):
                         index = i * step + r
                         if index > valley1-1:
                             index = index - len1
                         need_change.append(index)
                    #delete
                    deleted = 0
                    need_change.sort()
                    for i in need_change:
                           del rows[i-deleted]
                           deleted = deleted + 1;
               elif change1 > 0:
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(beg,valley1-1)
                    r_area = random.randint(change1,len1)                        #this decide area we change
                    step = abs(int(r_area / change1))

                    for i in range(0,abs(change1)):
                         index = i * step + r
                         if index > valley1-1:
                             index = index - len1
                         need_change.append(index)
                    #delete
                    added = 0
                    need_change.sort()
                    for i in need_change:
                           row = rows[i+added]
                           rows.insert(i+added,row)
                           added = added + 1
               valley1 = valley1 + change1
               valley2 = valley2 + change1
               end = end +change1
               #change the 3rd peak
               #remove
               if change3 < 0:
                    step = abs(int(len3 / change3))
                     
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(valley2,end-1)
                    for i in range(0,abs(change3)):
                         index = i * step + r
                         if index > end-1:
                             index = index - len3
                         need_change.append(index)
                    #delete
                    deleted = 0
                    need_change.sort()
                    for i in need_change:
                           del rows[i-deleted]
                           deleted = deleted + 1;
                           
               elif change3 > 0:
                     
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(valley2,end-1)
                    r_area = random.randint(change3,len3)                        #this decide area we change
                    step = abs(int(r_area / change3))

                    for i in range(0,abs(change3)):
                         index = i * step + r
                         if index > end-1:
                             index = index - len3
                         need_change.append(index)
                    #delete
                    added = 0
                    for i in need_change:
                           row = rows[i+added]
                           rows.insert(i+added,row)
                           added = added + 1;
                 
               #change the 2nd peak
               end = end + change3
               #remove
               if change2 < 0:
                    step = abs(int(len2 / change2))           
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(valley1,valley2-1)
                    for i in range(0,abs(change2)):
                         index = i * step + r
                         if index > valley2-1:
                             index = index - len2
                         need_change.append(index)
                    #delete
                    deleted = 0
                    need_change.sort()
                    for i in need_change:
                           del rows[i-deleted]
                           deleted = deleted + 1;
               elif change2 > 0:
                    #find those need to be deleted
                    need_change = []
                    r = random.randint(valley1,valley2-1)                      #this decide where we begin to change         
                    r_area = random.randint(change2,len2)                        #this decide area we change
                    step = abs(int(r_area / change2))

                    for i in range(0,abs(change2)):
                         index = i * step + r
                         if index > valley2-1:
                             index = index - len2
                         need_change.append(index)
                    #delete
                    added = 0
                    need_change.sort()
                    for i in need_change:
                           row = rows[i+added]
                           rows.insert(i+added,row)
                           added = added + 1;
               
               epco1 = pd.DataFrame(rows, columns=columns)
 
               valley2 = valley2 + change2
               end = end +change2
               #print(".......",name,beg,valley1,valley2,end)
               #<beg,valley1>   first peak
               max_val_all = epco1.loc[beg].values[1]
               max_val_co = epco1.loc[beg].values[1]
               min_val_all = epco1.loc[beg].values[1]
               for i in range (beg,valley1+1):
                   for j in range (1,5):
                       val = epco1.loc[i].values[j]
                       if val > max_val_all:
                          max_val_all = val
                       if val < min_val_all:
                          min_val_all = val
                       if j == 1 or j == 4:
                          if val > max_val_co:
                             max_val_co = val
               #<valley2,end>   third peak
               for i in range (valley2,end+1):
                  for j in range (1,5):
                       val = epco1.loc[i].values[j]
                       if val > max_val_all:
                           max_val_all = val
                       if val < min_val_all:
                           min_val_all = val
                       if j == 1 or j == 4:
                           if val > max_val_co:
                              max_val_co = val
                   #<va   lley1_new,valley2>   second peak
               vals_all = []
               vals_co = []
               for i in range (valley1,valley2+1):
                   for j in range (1,5):
                       vals_all.append(epco1.loc[i].values[j])
                   if j == 1 or j == 4:
                       vals_co.append(epco1.loc[i].values[j])
               vals_all.sort()
               vals_co.sort()
               #only save (1)top 2 of all values (low, high, open, close) in 2nd peak is great than the 1st and 3rd peak, (2) top 2 of all values (open, close) in 2nd peak is great than (open, close) in the 1st and 3rd peak,
               if vals_all[-2] >  max_val_all  or vals_co[-2] >  max_val_co:
                      #adapt orginal positio
                      max_val_whole_new = epco1.loc[0].values[1]
                      min_val_whole_new = epco1.loc[0].values[1] 
                      for i in range (0,size):
                          for j in range (1,5):
                              val = epco1.loc[i].values[j]
                              if val > max_val_whole_new:
                                  max_val_whole_new = val
                              if val < min_val_whole_new:
                                  min_val_whole_new = val  
                      outed = 0
                      if max_val_whole_new > max_val_whole:
                          outed = max_val_whole_new - max_val_whole
                          for i in range (beg,end+1):
                              epco1['Close'][i] = epco1['Close'][i] - outed
                              epco1['High'][i] = epco1['High'][i] - outed
                              epco1['Low'][i] = epco1['Low'][i] - outed
                              epco1['Open'][i] = epco1['Open'][i] - outed
                      elif max_val_whole_new < max_val_whole:
                          outed = max_val_whole - max_val_whole_new
                          for i in range (beg,end+1):
                              epco1['Close'][i] = epco1['Close'][i] + outed
                              epco1['High'][i] = epco1['High'][i] + outed
                              epco1['Low'][i] = epco1['Low'][i] + outed
                              epco1['Open'][i] = epco1['Open'][i] + outed

                   
                      #check bot is out of original scale
                      max_val_whole_new = epco1.loc[0].values[1]
                      min_val_whole_new = epco1.loc[0].values[1] 
                      for i in range (0,size):
                          for j in range (1,5):
                              val = epco1.loc[i].values[j]
                              if val > max_val_whole_new:
                                  max_val_whole_new = val
                              if val < min_val_whole_new:
                                  min_val_whole_new = val  

                      bot_out = 0

                      if min_val_whole_new < min_val_whole:
                         bot_out = min_val_whole - min_val_whole_new
                         for i in range (beg,end+1):
                             epco1['Close'][i] = epco1['Close'][i] + bot_out
                             epco1['High'][i] = epco1['High'][i] + bot_out
                             epco1['Low'][i] = epco1['Low'][i] + bot_out
                             epco1['Open'][i] = epco1['Open'][i] + bot_out 
                      elif min_val_whole_new > min_val_whole:
                         bot_out = min_val_whole_new - min_val_whole
                         for i in range (beg,end+1):
                             epco1['Close'][i] = epco1['Close'][i] - bot_out
                             epco1['High'][i] = epco1['High'][i] - bot_out
                             epco1['Low'][i] = epco1['Low'][i] - bot_out
                             epco1['Open'][i] = epco1['Open'][i] - bot_out 

                         max_val_whole_new = epco1.loc[0].values[1]
                         min_val_whole_new = epco1.loc[0].values[1] 
                         for i in range (0,size):
                             for j in range (1,5):
                                 val = epco1.loc[i].values[j]
                                 if val > max_val_whole_new:
                                     max_val_whole_new = val
                                 if val < min_val_whole_new:
                                     min_val_whole_new = val  

                      moved_down = 0
                      if max_val_whole_new < max_val_whole:
                          moved_down = max_val_whole - max_val_whole_new
                          for i in range (beg,end+1):
                              epco1['Close'][i] = epco1['Close'][i] + moved_down
                              epco1['High'][i] = epco1['High'][i] + moved_down
                              epco1['Low'][i] = epco1['Low'][i] + moved_down
                              epco1['Open'][i] = epco1['Open'][i] + moved_down 
   

                      moved_up = 0
                      if min_val_whole_new > min_val_whole:
                          moved_up = min_val_whole_new - min_val_whole
                          for i in range (beg,end+1):
                              epco1['Close'][i] = epco1['Close'][i] - moved_up
                              epco1['High'][i] = epco1['High'][i] - moved_up
                              epco1['Low'][i] = epco1['Low'][i] - moved_up
                              epco1['Open'][i] = epco1['Open'][i] - moved_up 
                    
                      #remove gap
                      b = beg
                      if b == 0:
                         b = b + 1
                    
                      for i in range (b,end+1):
                              if epco1['Low'][i] > epco1['High'][i-1]:
                                  if epco1['Open'][i] < epco1['Close'][i]:
                                      gap = epco1['Open'][i] - epco1['High'][i-1]
                                      epco1['Open'][i] = epco1['Open'][i] - gap / 2
                                      epco1['Low'][i] = epco1['Low'][i] - gap/2
                                      epco1['High'][i-1] = epco1['High'][i-1] + gap/2
                                      if epco1['Open'][i-1] > epco1['Close'][i-1]:
                                          epco1['Open'][i-1] = epco1['Open'][i-1] + gap/2
                                      else:
                                          epco1['Close'][i-1] = epco1['Close'][i-1] + gap/2
                              elif epco1['Low'][i-1] > epco1['High'][i]:
                                  if epco1['Open'][i] > epco1['Close'][i]:
                                      gap = epco1['Low'][i-1] - epco1['Open'][i]
                                      epco1['Open'][i] = epco1['Open'][i] + gap / 2
                                      epco1['High'][i] = epco1['High'][i] + gap/2
                                      epco1['Low'][i-1] = epco1['Low'][i-1] - gap/2
                                      if epco1['Open'][i-1] < epco1['Close'][i-1]:
                                          epco1['Open'][i-1] = epco1['Open'][i-1] - gap/2
                                      else:
                                          epco1['Close'][i-1] = epco1['Close'][i-1] - gap/2




                      name1 = name + "_auto_" + str(scale) + "_" + str(saved)
                      print("saving file.....",name1,len(epco1))                        
                      save_one_related_data(epco1,name1,variation_text_path)
                      saved = saved + 1
                      repeat = 0 

                      #adapt label
                      file_name = name1+'.jpg'
                      wideth = label_information[1]
                      hight = label_information[2]
                      _class = label_information[3]
                      xmin =  label_information[4] 
                      xmax =  label_information[6]  
                        
                      #new coordinate of ymax is (new max value - old max) * rate + old ymax
                      ymin =  int(round(((min_val_all - outed + bot_out + moved_down - moved_up) - min_val) * rate + int(label_information[5]))) 
                      ymax =  int(round(((vals_all[-1] - outed+ bot_out + moved_down - moved_up) - max_val) * rate + int(label_information[7])))

                      label_information = [file_name,wideth,hight,_class,xmin,ymin,xmax,ymax,valley1,valley2] 
                      labels.append(label_information)

    return labels   
                          
#make variation data
def make_variation_data(orginal_text_path,variation_text_path,train_label,period,window_size):
    files = os.listdir(orginal_text_path)
    for file_name in files:
        name = file_name[0:file_name.index('.csv')]
        label_information = []
        for label in train_label:
            if label[0] == name + ".jpg":
               label_information = label
               break
        index1, index2 = find_pattern_data(label_information,period,window_size)
        file_full_name = os.path.join(orginal_text_path,file_name)
        #pic_name = file_name[0:file_name.index('.csv')]    
        with open(file_full_name) as f:
             data = csv.reader(f)
             columns = ['Date','Close', 'High', 'Low', 'Open']
             rows = []
             times = []
             for row in data:
                 rows.append(list(map(float,row)))
             epco = pd.DataFrame(rows, columns=columns)
  
             # 3 ways to general more data
             make_taller(epco,index1, index2,name,variation_text_path)
             make_wider(epco,index1, index2,name,variation_text_path)
             r_change(epco,index1, index2,name,variation_text_path)

#make variation data automatically, with this function you dont need to re-adapt the labels. 
def make_variation_data_auto(orginal_text_path,variation_text_path,train_label,period,window_size):
    new_labels = []
    files = os.listdir(orginal_text_path)
    for file_name in files:
        name = file_name[0:file_name.index('.csv')]
        label_information = []
        for label in train_label:
            if label[0] == name + ".jpg":
               label_information = label
               valley1 = int(label_information[8])
               valley2 = int(label_information[9])
               beg, end = find_pattern_data(label_information,period,window_size)
               file_full_name = os.path.join(orginal_text_path,file_name)
               #pic_name = file_name[0:file_name.index('.csv')]    
               with open(file_full_name) as f:
                    data = csv.reader(f)
                    columns = ['Date','Close', 'High', 'Low', 'Open']
                    rows = []
                    times = []
                    for row in data:
                        rows.append(list(map(float,row)))
                    epco = pd.DataFrame(rows, columns=columns)
                    labels = r_change_auto(epco,beg, end,valley1,valley2,name,variation_text_path,label_information)
                    #labels = r_change_auto_x(epco,beg, end,valley1,valley2,name,variation_text_path,label_information)
                    new_labels = new_labels + labels
    return new_labels

def write_labels(labels,path):
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax','valley1','valley2']
    labels_csv = pd.DataFrame(labels, columns=column_name)
    labels_csv.to_csv(path+'/raccoon_labels.csv', index=None)
    print('Successfully converted test xml to csv.')



if __name__ == "__main__":

    period = 600;
 
    #total history data time, 1 year
    time = 2;
    #windows size, days
    window_size = 7;
    text_path = "text"
    original_text_path = 'variation_data/text/original_text_auto'; #path to save original text which exists the data of labled image
    variation_text_path = 'variation_data/text/variation_text_auto'; #path to save variation text

    train_label_csv_path = "variation_data/text/valley_points.csv"
    train_label = read_labels(train_label_csv_path)
       
    #find_related_data(train_label, period, time,window_size,original_text_path)
    
    #general variation data
    print("general data ...")
    #make_variation_data(original_text_path,variation_text_path,train_label,period,window_size)
    new_labels = make_variation_data_auto(original_text_path,variation_text_path,train_label,period,window_size)
    
    #save new labels
    new_label_path = 'variation_data/new_labels_auto'
    write_labels(new_labels,new_label_path)
     

    #draw figures with variation data
    variation_images = 'variation_data/images_generaled_auto'
    print("drawing figs ...")
    draw_figures(variation_text_path,variation_images)
    
