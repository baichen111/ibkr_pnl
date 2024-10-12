from functools import reduce
import yfinance as yf
from collections import defaultdict
import pandas as pd
import time,os
from stocklist import syms,fields

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class watchlist:
    def __init__(self) -> None:     
        self.syms = syms
        self.fields = fields
        self.tickers = yf.Tickers(self.syms)
        self.fundamentals = defaultdict(list)
        self.close = defaultdict(list)
        
    def get_fundamentlas(self) -> pd.DataFrame:
        print("pulling fundamental data: ",self.syms)
        for sym in self.syms:
            for field in self.fields:
                self.fundamentals[sym].append(self.tickers.tickers[sym].info.get(field))
        return round(pd.DataFrame(self.fundamentals,index=self.fields).T,2)

    def pull_close_data(self) :
        print("pulling historical close data :",self.syms)
        for sym in self.syms:
            self.close[sym] = self.tickers.tickers[sym].history(period = '1y')['Close'] #dict where k is sym and value is close price in pd series
        close_path = '/home/baichen/historical_data/'
        os.makedirs(close_path,exist_ok=True)
        pd.DataFrame(self.close).to_csv(close_path+'stock_close.csv')
        
    def correlation(self):
        cor_df = pd.DataFrame(self.close).corr()
        cor_path = '/home/baichen/correlation/'
        os.makedirs(cor_path,exist_ok=True)
        cor_df.to_csv(cor_path + 'correlation.csv')
        
    def draw_down(self)->pd.DataFrame: #calculate max draw down, current draw down
        dd_data = defaultdict(list)
        # self.pull_close_data()
        
        for sym,close in self.close.items(): # close is pd series data
            current_close = round(close[-1],2)
            peak = close.cummax()
            peak_price = round(peak[-1],2)
            dd = (close - peak) / peak
            max_dd = str(round(100 * abs(min(dd)),2))+"%"
            
            current_dd = str(round(100 * abs((close[-1] - peak[-1]) / peak[-1]),2))+"%"
            dd_data[sym].extend([max_dd,current_dd,peak_price,current_close])
        return pd.DataFrame(dd_data,index=['max_draw_down','current_draw_down','peak_price','current_price']).T
    
    def merge(self,*dfs):  # merge tables into one based on symbols
        return reduce(lambda left,right:pd.merge(left,right,left_index=True,right_index=True),dfs)
    
    def save_df(self,df,path = "/home/baichen/watchlist/"):
        df.index.name = 'symbols'
        print(df)
        file_name = "/watchlist.csv"
        os.makedirs(path, exist_ok=True)
        print("Saving down csv file to ",path+file_name)
        df.to_csv(path + file_name)
        
        TodayDate = time.strftime("%d_%m_%Y")
        print("Saving down csv file to ",path + TodayDate + "_watchlist.csv")
        df.to_csv(path + TodayDate + "_watchlist.csv")


if __name__ == '__main__':
    w = watchlist()
    f_df = w.get_fundamentlas()
    w.pull_close_data()
    
    dd_df = w.draw_down()
    merged_df = w.merge(f_df,dd_df)
    w.save_df(merged_df)
    w.correlation()