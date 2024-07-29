import pandas as pd
import glob,time
import seaborn as sns
import matplotlib.pyplot as plt


csv_files = glob.glob('/home/baichen/ibkr_daily_pnl/*.csv')
totals = [pd.read_csv(f).tail(1) for f in csv_files]

port_df = pd.concat(totals)
port_df['date']=pd.to_datetime(port_df['date'])
port_df.set_index('date',inplace=True)
port_df =port_df.sort_index()
port_df.index = port_df.index.date

sns.set(rc = {'figure.figsize':(18,8)})
ax=sns.histplot(x='dailyPnL',data=port_df,binwidth=2500,binrange=(-20000,20000),kde=True,stat="percent")
for i in ax.containers:
    ax.bar_label(i,)
    
TodayDate = time.strftime("%d_%m_%Y")
plt.savefig('/home/baichen/ibkr_plot_pnl/' + TodayDate + '_daily_pnl.png',dpi=300)