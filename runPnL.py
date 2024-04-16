from ib_insync import *
import pandas as pd
import time, os
from datetime import date, timedelta

from accountInfo import acc  # load account info

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=2)

account = acc
portItems = ib.portfolio(account)  # get portfolio information
print(portItems)

con_id = {port.contract.conId: port.contract.symbol for port in portItems}  #map contract id to symbol
print(con_id)


def get_positions():
    for port in portItems:
        ib.reqPnLSingle(account, "", port.contract.conId)
        ib.sleep(1)


def getDailyPnL(account: str):
    get_positions()
    daily_pnl = {con_id[pnl.conId]: pnl.dailyPnL for pnl in ib.pnlSingle(account)}
    print(daily_pnl)
    print(f"{date.today() - timedelta(days=1)} total daily profit & loss: {sum(list(daily_pnl.values()))}")
    return daily_pnl


def pnl_df():
    df = util.df(portItems,
                 ['position', 'marketPrice', 'marketValue', 'averageCost', 'unrealizedPNL', 'realizedPNL', 'account'])
    df['symbols'] = [port.contract.symbol for port in portItems]
    df['currency'] = [port.contract.currency for port in portItems]
    df['dailyPnL'] = list(getDailyPnL(account).values())
    df['secTypes'] = [port.contract.secType for port in portItems]
    df['rights'] = [port.contract.right for port in portItems]
    df['strikes'] = [port.contract.strike for port in portItems]
    df = df[
        ['symbols', 'secTypes', 'rights', 'strikes', 'currency', 'position', 'marketPrice', 'marketValue',
         'averageCost', 'unrealizedPNL', 'realizedPNL',
         'dailyPnL', 'account']]
    df.loc['Total'] = df[['marketValue', 'unrealizedPNL', 'realizedPNL', 'dailyPnL']].sum()
    df['date'] = pd.Timestamp.today()
    df.set_index('date', inplace=True)
    df.fillna('', inplace=True)
    return df


def on_pnlSingle(entry: PnLSingle):
    print(entry)


def on_disconnected():  #callback after disconnected from TWS
    print("You are disconnected !")


if __name__ == "__main__":
    ib.pnlSingleEvent += on_pnlSingle
    ib.disconnectedEvent += on_disconnected
    df = pnl_df()
    TodayDate = time.strftime("%d_%m_%Y")
    file_name = TodayDate + "_DailyPnLtest.csv"
    path = "ibkr_daily_pnl/"
    os.makedirs(path, exist_ok=True)
    df.to_csv(path + file_name)
