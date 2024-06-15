import os
import time
from collections import defaultdict
from datetime import date, timedelta

import pandas as pd
from ib_insync import *

from accountInfo import acc  # load account info

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=2)

account = acc
portItems = ib.portfolio(account)  # get portfolio information
con_id = {port.contract.conId: port.contract.symbol for port in portItems}  #map contract id to symbol


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
    print(f"{date.today() - timedelta(days=1)} total daily profit & loss: {sum(list(daily_pnl.values()))}")
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
    cashRow = cash_row(df.columns)
    df = pd.concat([df, pd.DataFrame(cashRow)], ignore_index=True)  # append a row for cash value
    df = df[
        ['symbols', 'secTypes', 'rights', 'strikes', 'currency', 'position', 'marketPrice', 'marketValue',
         'averageCost', 'unrealizedPNL', 'realizedPNL',
         'dailyPnL', 'account']]
    df = df.round(2)
    df.loc['Total'] = df[['marketValue', 'unrealizedPNL', 'realizedPNL', 'dailyPnL']].sum()
    df['date'] = pd.Timestamp.today()
    df.set_index('date', inplace=True)
    df = df.round(2)
    return df


def save_df(df: pd.DataFrame, path: str = "ibkr_daily_pnl/"):
    """
    save daily pnl to disk
    :param df: dataframe
    :param path: directory path
    :return: None
    """
    TodayDate = time.strftime("%d_%m_%Y")
    file_name = "/" + TodayDate + "_DailyPnLtest.csv"
    os.makedirs(path, exist_ok=True)
    df.to_csv(path + file_name)


def on_pnlSingle(entry: PnLSingle):
    print(entry)


def on_disconnected():  #callback after disconnected from TWS
    print("You are disconnected !")


if __name__ == "__main__":
    ib.pnlSingleEvent += on_pnlSingle
    ib.disconnectedEvent += on_disconnected
    df = pnl_df()
    save_df(df)
