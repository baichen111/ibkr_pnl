from ib_insync import *
import pandas as pd
import time
from accountInfo import acc  # load account info

#pd.set_option('display.max_columns', None)
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=2)

account = acc
portItems = ib.portfolio(account)  # get portfolio information


def getDailyPnL(account: str):
    for port in portItems:
        ib.reqPnLSingle(account, "", port.contract.conId)
    ib.sleep(3)  #must use ib.sleep rather than time.sleep
    daily_pnl = [pnl.dailyPnL for pnl in ib.pnlSingle(account)]
    return daily_pnl


def pnl_df():
    symbols = [port.contract.symbol for port in portItems]
    currency = [port.contract.currency for port in portItems]
    sec_types = [port.contract.secType for port in portItems]
    rights = [port.contract.right for port in portItems]
    strikes = [port.contract.strike for port in portItems]
    df = util.df(portItems,
                 ['position', 'marketPrice', 'marketValue', 'averageCost', 'unrealizedPNL', 'realizedPNL', 'account'])
    df['symbols'] = symbols
    df['currency'] = currency
    df['dailyPnL'] = getDailyPnL(account)
    df['secTypes'] = sec_types
    df['rights'] = rights
    df['strikes'] = strikes
    df = df[
        ['symbols', 'secTypes', 'rights', 'strikes', 'currency', 'position', 'marketPrice', 'marketValue',
         'averageCost', 'unrealizedPNL', 'realizedPNL',
         'dailyPnL', 'account']]
    df['date'] = pd.Timestamp.today()
    df.set_index('date', inplace=True)
    return df
def onDisconnected():         #callback after disconnected from TWS
    print("You are disconnected !")

if __name__ == "__main__":
    ib.disconnectedEvent += onDisconnected
    df = pnl_df()
    TodayDate = time.strftime("%d_%m_%Y")
    file_name = TodayDate + "_DailyPnL.csv"
    df.to_csv("C:\ibkrPnL\\" + file_name)

