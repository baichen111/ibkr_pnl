import pandas as pd
import glob,time
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


csv_files = glob.glob('/home/baichen/ibkr_daily_pnl/*.csv')
totals = [pd.read_csv(f).tail(1) for f in csv_files]

port_df = pd.concat(totals)
port_df['date']=pd.to_datetime(port_df['date'])
port_df.set_index('date',inplace=True)
port_df =port_df.sort_index()
port_df.index = port_df.index.date

kurtosis = port_df['dailyPnL'].kurtosis()
skewness = port_df['dailyPnL'].skew()
mean = round(port_df['dailyPnL'].mean(),2)
median = round(port_df['dailyPnL'].median(),2)
std = round(port_df['dailyPnL'].std(),2)

sns.set(rc = {'figure.figsize':(25,8)})
ax=sns.histplot(x='dailyPnL',data=port_df,binwidth=2500,binrange=(-30000,30000),kde=True,stat="percent")
ax.text(25000, 20, f'kurtosis: {round(kurtosis,2)} \nskewness: {round(skewness,2)} \nmean: USD{mean} \nmedian = USD{median} \nvolatility = USD{std}', size=10, color='purple')
fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(tick) 
for i in ax.containers:
    ax.bar_label(i,)
    
TodayDate = time.strftime("%d_%m_%Y")
plt.savefig('/home/baichen/ibkr_plot_pnl/' + TodayDate + '_daily_pnl.png',dpi=500)