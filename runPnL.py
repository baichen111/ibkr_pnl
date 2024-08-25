import os,time
from collections import defaultdict
from datetime import date, timedelta

import pandas as pd
from ib_insync import *

from accountInfo import acc  # load account info

util.startLoop()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)  #gateway port 4001; TWS UI 7496

account = acc
portItems = ib.portfolio(account)  # get portfolio information
con_id = {port.contract.conId: (port.contract.symbol + "_Option" if port.contract.secType == "OPT" else port.contract.symbol) for port in portItems}   #map contract id to symbol

def calculate_drawdown():
    '''
    calculate draw down in percentage from peak over last 1 year to current price for all holding stocks
    '''
    syms = [port.contract.symbol for port in portItems if isinstance(port.contract,Stock)]
    dd = defaultdict(str)
    for sym in syms:
        contract = Stock(symbol=sym, exchange="SMART", currency="USD",primaryExchange = "NASDAQ")
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='12 M',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=True,
            keepUpToDate=False,
            formatDate=1)

        df = util.df(bars)
        lastPrice = df.loc[len(df)-1,'close']
        maxClose = df['close'].cummax().iloc[-1]
        dd[sym] = str(round(100 * (lastPrice/maxClose - 1),2)) +"%"
    df = pd.DataFrame(dd,index=['draw_down']).T
    df['symbols'] = df.index
    df.reset_index(inplace=True)
    df = df[['symbols','draw_down']]    
    return df

def get_positions():
    """
    retrieve each open position in my account
    """
    for port in portItems:
        ib.reqPnLSingle(account, "", port.contract.conId)
        ib.sleep(1)


def getDailyPnL(account: str):
    """
    put all open positions to a dict
    :param account:  my account number
    :return: dict with  contract id and daily pnl
    """
    get_positions()
    daily_pnl = {con_id[pnl.conId]: pnl.dailyPnL for pnl in ib.pnlSingle(account)}
    print(f"{date.today() - timedelta(days=1)} total daily profit & loss: {round(sum(list(daily_pnl.values())),2)}")
    return daily_pnl


def cash_row(cols):
    """
    build a cash row
    :param cols: dataframe columns
    :return: cash dict
    """
    cashValue = float(ib.accountSummary(account)[-1].value)  # get cash value in the account
    cashDict = defaultdict(None)
    for c in cols:
        if c == "secTypes":
            cashDict[c] = ['Cash']
        elif c == 'marketValue':
            cashDict[c] = [cashValue]
        elif c == 'symbols':
            cashDict[c] = ['CASH']
        elif c == 'currency':
            cashDict[c] = ['USD']
        elif c == 'account':
            cashDict[c] = [account]
        else:
            cashDict[c] = 0
    return cashDict


def pnl_df():
    """
    consolidate all information in df
    :return: daily pnl dataframe
    """
    df = util.df(portItems,
                 ['position', 'marketPrice', 'marketValue', 'averageCost', 'unrealizedPNL', 'realizedPNL', 'account'])
    df['symbols'] = [port.contract.symbol for port in portItems]
    df['currency'] = [port.contract.currency for port in portItems]
    df['dailyPnL'] = list(getDailyPnL(account).values())
    df['secTypes'] = [port.contract.secType for port in portItems]
    df['rights'] = [port.contract.right for port in portItems]
    df['strikes'] = [port.contract.strike for port in portItems]
    df['total_return'] = ((df['marketPrice'] / df['averageCost']) - 1).apply(lambda x: str(round(x * 100,2))+"%")
    cashRow = cash_row(df.columns)
    df = pd.concat([df, pd.DataFrame(cashRow)], ignore_index=True)  # append a row for cash value
    df = df[
        ['symbols', 'secTypes', 'rights', 'strikes', 'currency', 'position', 'marketPrice', 'marketValue',
         'averageCost', 'unrealizedPNL', 'realizedPNL',
         'dailyPnL', 'total_return','account']]
    df = df.round(2)
    df.loc['Total'] = df[['marketValue', 'unrealizedPNL', 'realizedPNL', 'dailyPnL']].sum()
    df.iloc[-1,df.columns.get_loc("total_return")]= str(round(100 * df.iloc[-1]['unrealizedPNL']/(df.iloc[-1]['marketValue'] - df.iloc[-1]['unrealizedPNL']),2))+"%" 
    df = df.round(2)
    return df


def save_df(df: pd.DataFrame, path: str = "/home/baichen/ibkr_daily_pnl/"):
    """
    save daily pnl to disk
    :param df: dataframe
    :param path: directory path
    :return: None
    """
    TodayDate = time.strftime("%d_%m_%Y")
    file_name = "/" + TodayDate + "_DailyPnL.csv"
    os.makedirs(path, exist_ok=True)
    print("Saving down csv file to ",path+file_name)
    df.to_csv(path + file_name)


def on_pnlSingle(entry: PnLSingle):
    #print(f"Symbol: {con_id[entry.conId]}\tDailyPnL: {round(entry.dailyPnL,2)}\tUnrealizedPnL: {round(entry.unrealizedPnL,2)}\tPosition: {entry.position}\tMarket Value: {round(entry.value,2)}")
    ...

def on_disconnected():  #callback after disconnected from TWS
    print("You are disconnected !")


if __name__ == "__main__":
    ib.pnlSingleEvent += on_pnlSingle
    ib.disconnectedEvent += on_disconnected
    df = pnl_df()
    dd_df = calculate_drawdown()
    df = pd.merge(df,dd_df,on='symbols',how="outer") #join pnl table and drawdown table
    df['date'] = pd.Timestamp.today()
    df.set_index('date', inplace=True)
    print(df)
    save_df(df)
