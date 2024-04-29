from ib_insync import *
import pandas as pd
from datetime import date, timedelta
import warnings
from accountInfo import acc

warnings.filterwarnings('ignore')

util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=3)  #gateway port is 4001

portItems = ib.portfolio(acc)  # get portfolio information
con_id = {port.contract.conId: port.contract.symbol for port in portItems}  #map contract id to symbol


def get_positions():
    for port in portItems:
        ib.reqPnLSingle(acc, "", port.contract.conId)
        ib.sleep(1)


def getDailyPnL(acc: str):
    get_positions()
    daily_pnl = {con_id[pnl.conId]: pnl.dailyPnL for pnl in ib.pnlSingle(acc)}
    return daily_pnl


def pnl_df():
    df = util.df(portItems,
                 ['position', 'marketPrice', 'marketValue', 'averageCost', 'unrealizedPNL', 'realizedPNL'])
    df['symbols'] = [port.contract.symbol for port in portItems]
    # df['currency'] = [port.contract.currency for port in portItems]
    df['dailyPnL'] = list(getDailyPnL(acc).values())
    df['secTypes'] = [port.contract.secType for port in portItems]
    df['rights'] = [port.contract.right for port in portItems]
    df['strikes'] = [port.contract.strike for port in portItems]
    df = df[
        ['symbols', 'secTypes', 'rights', 'strikes', 'position', 'marketPrice', 'marketValue',
         'averageCost', 'unrealizedPNL', 'realizedPNL',
         'dailyPnL']]
    df.loc['Total'] = df[['marketValue', 'unrealizedPNL', 'realizedPNL', 'dailyPnL']].sum()
    df['date'] = pd.Timestamp.today()
    df.set_index('date', inplace=True)
    df.fillna('', inplace=True)
    return df


def on_pnlSingle(entry: PnLSingle):
    ...


def on_disconnected():  #callback after disconnected from TWS
    print("You are disconnected !")


if __name__ == "__main__":
    ib.pnlSingleEvent += on_pnlSingle
    ib.disconnectedEvent += on_disconnected
    while True:
        df = pnl_df()
        print(df)
        for c ,_ in con_id.items():
            ib.cancelPnLSingle(acc,"",c)
        print("="*302)
        ib.sleep(60)
