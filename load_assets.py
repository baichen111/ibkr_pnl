import pandas as pd
import glob,os

def load(load_path = '/home/baichen/ibkr_daily_pnl/'):
    csv_files = glob.glob(load_path +'*.csv')
    dfs = [pd.read_csv(f)[:-1] for f in csv_files]
    df = pd.concat(dfs)
    df['date']=pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    df =df.sort_index()
    df.index = df.index.date
    return df

def save(df:pd.DataFrame,to_save = '/home/baichen/ibkr_assets_pnl/'):
    cols = set(df.symbols)
    os.makedirs(to_save, exist_ok=True)
    
    #stock asset
    for col in cols:
        asset = df[(df['symbols'] == col) & (df['secTypes'] == 'STK')]
        if len(asset) != 0:
            asset = asset.round(2)
            asset.index.name = 'date'
            asset.to_csv(to_save + '/'+col+'_'+asset['secTypes'][0]+'.csv')
        
    #non-stock asset
    for col in cols:
        asset = df[(df['symbols'] == col) & (df['secTypes'] != 'STK')]
        if len(asset) !=0:
            asset = asset.round(2)
            asset.index.name = 'date'
            asset.to_csv(to_save + '/'+col+'_'+asset['secTypes'][0]+'.csv')

if __name__ == '__main__':
    df = load()
    save(df)