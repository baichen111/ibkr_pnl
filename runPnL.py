from ib_insync import *
import pandas as pd
import time
from accountInfo import acc  # load account info
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=2)

account = acc
portItems = ib.portfolio(account)  # get portfolio information
#print(portItems)


def getDailyPnL(account: str):
    for port in portItems:
        ib.reqPnLSingle(account, "", port.contract.conId)
    ib.sleep(2)  #must use ib.sleep rather than time.sleep
    daily_pnl = [pnl.dailyPnL for pnl in ib.pnlSingle(account)]
    # print(daily_pnl)
    print("Total daily profit & loss: ", sum(daily_pnl))
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
    df.to_csv("C:\ibkrPnL\\" + file_name)
