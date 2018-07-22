#this one is to draw the smoothed pics
from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D
import segment
import fit
import os
import csv
import re
import pandas as pd
import datetime		
from datetime import timezone
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def draw_plot(data,plot_title):
    fig = plt.figure(figsize=(8, 6))
    ax = plt.subplot2grid((1,1), (0,0))
    
    plot(range(len(data['High'])),data['High'],alpha=0.8,color='white')
    plot(range(len(data['Low'])),data['Low'],alpha=0.8,color='white')
    plot(range(len(data['Close'])),data['Close'],alpha=0.8,color='white')
    #plot(range(len(data2)),data2,alpha=0.8,color='red')
    plot(range(len(data['Open'])),data['Open'],alpha=0.8,color='blue')

    xdate = [datetime.datetime.fromtimestamp(i) for i in data['Date']]
    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''  
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(mydate))    
    ax.xaxis.set_major_locator(mticker.MaxNLocator(10))

    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(plot_title)
    #xlim((0,len(data1)-1))
    #plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    

def draw_segments(segments1,segments2):
    ax = gca()
    #for segment in segments1:
    #    line = Line2D((segment[0],segment[2]),(segment[1],segment[3]), color = 'red')
    #    ax.add_line(line)
    for segment in segments2:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]),color = 'blue')
        ax.add_line(line)

def draw_one_fitted_picture(data,name,epco_num,time): 
    Close = data['Close']
    Open = data['Open']
    max_error = 0.01

    max_val = Close[1]
    min_val = Close[1]
    #adapt the max_error
    for val in Close:
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val
    for val in Open:
        if val > max_val:
            max_val = val
        if val < min_val:
            min_val = val    	
    adapted_error = max_error * (max_val - min_val) * (max_val - min_val) 
    #bottom-up with  simple interpolation
    segments = segment.topdownsegment(Close, fit.interpolate, fit.sumsquared_error, adapted_error)
    segments1 = segment.topdownsegment(Open, fit.interpolate, fit.sumsquared_error, adapted_error)
    draw_plot(data,name)
    draw_segments(segments,segments1)

    #save figure
    file_name = r'../fitted_figures/'+name+'/'+name+'_'+str(time)+'Y_'+str(epco_num)+'.jpg';
    plt.savefig(file_name,bbox_inches='tight')
    #plt.show()
    plt.close()
    

#read the data from csv files
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


def draw_fitted_pictures(ticker,name,time,period,window_size):
    if os.path.exists(r'../fitted_figures/'+name) == False:
       os.mkdir(r'../fitted_figures/'+name)

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
               draw_one_fitted_picture(epco,name,epco_num,time)
               
               #reset the index
               index = step_size * epco_num
               epco_num = epco_num + 1
               rows = []
               current_size = 0
               #check whther left data is enough to draw another picture  


def main():
    period = 600;
 
    #total history data time, 1 year
    time = 2;
    #windows size, days
    window_size = 7;
    text_path = "../text/"
    files = os.listdir(text_path)
    if os.path.exists("../fitted_figures/") == False:
       os.mkdir("../fitted_figures/")
    for file_name in files:
        strs = file_name.split('_')
        ticker = strs[0]
        file_full_name = text_path+file_name;
        data_timestamp, data  = read_data(file_full_name,period,time)
    
        #visual data
        draw_fitted_pictures(data_timestamp,ticker,time,period,window_size)
main()

