import pandas as pd
import streamlit as st
import glob
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

wl_df = pd.read_csv("/home/baichen/watchlist/watchlist.csv",index_col="symbols")  # read watch list data
portfolio_df = pd.read_csv("/home/baichen/ibkr_daily_pnl/DailyPnL.csv",index_col="symbols") # read portfolio data

#sidebar setup
st.sidebar.title('Stock Market Data')
options = st.sidebar.radio('Select what you want to display:', ['Watch List', 'Portfolio', 'Plot'])

cols_1 = st.columns(2)
cols_2 = st.columns(2)
cols_3 = st.columns(2)

if options == 'Watch List':
    st.title("Stock Watchlist")
    st.dataframe(wl_df,width=4000,height=800)
elif options == "Portfolio":
    st.title("Portfolio Data")
    st.dataframe(portfolio_df,width=4000,height=500)
elif options == 'Plot':
    csv_files = glob.glob('/home/baichen/ibkr_daily_pnl/*_DailyPnL.csv')
    totals = [pd.read_csv(f).tail(1) for f in csv_files]
    port_df = pd.concat(totals)
    port_df['date']=pd.to_datetime(port_df['date'])
    port_df.set_index('date',inplace=True)
    port_df =port_df.sort_index()
    port_df.index = port_df.index.date
    # st.dataframe(port_df[['marketValue','unrealizedPNL','dailyPnL']])
    
    #plot line chars
    line_fig = px.line(port_df[['marketValue']],title="Portfolio Market Value",labels={"value":'Market Value','index':'Date'})
    cols_2[0].plotly_chart(line_fig)
    
    #plot distribution
    dist_fig = px.histogram(port_df,x='dailyPnL',histnorm='percent',opacity=1,marginal='violin',text_auto='.2f',nbins=20,title="Daily Profit & Loss")
    dist_fig.update_traces(marker_line_width=1,marker_line_color="white") # add white gap between each hist
    mean = port_df['dailyPnL'].mean()
    std = port_df['dailyPnL'].std()
    dist_fig.add_shape(type='line',x0 = mean,x1 = mean, # add mean line
                       y0 =0, y1=40 ,
                       line = dict(color = 'red', dash = 'dash'))
    dist_fig.add_shape(type='line',x0 = std,x1 = std, # add positive std line
                       y0=0,y1=40,
                       line = dict(color = 'blue', dash = 'dash'))
    dist_fig.add_shape(type='line',x0 = std *-1,x1= std *-1, # add negative std line
                       y0=0,y1=40,
                       line = dict(color = 'blue', dash = 'dash'))
    cols_1[0].plotly_chart(dist_fig,use_container_width=True)

    
    #plot pie charts
    pie_df = portfolio_df[:-2]
    pie_fig = px.pie(pie_df,values='marketValue',names=pie_df.index,title="Portfolio Weights")
    cols_1[1].plotly_chart(pie_fig)
    
    #plot total daily win and loss
    total_win_value = port_df[port_df['dailyPnL']>0]['dailyPnL'].sum()
    total_loss_value = port_df[port_df['dailyPnL']<0]['dailyPnL'].sum()
    g = pd.DataFrame({'Win':[total_win_value],'Loss':[total_loss_value]}).T
    bar_win_loss = px.bar(g,color=g.index,
                          color_discrete_map={
                            "Win": 'green',
                            "Loss": 'red'
                        },template='seaborn',text_auto='.2f',title="Win & Loss")
    cols_2[1].plotly_chart(bar_win_loss)
    
    #plot return for each asset
    return_df = portfolio_df[['total_return']][:-2]
    return_df['positive_negative'] = return_df["total_return"].apply(lambda x:float(x[:-1])) > 0
    bar_assets_return = px.bar(return_df,x=return_df.index,y='total_return',text_auto=True,
                        color='positive_negative',
                        color_discrete_map={True: "green", False: "red"},
                        title='Assets Total Return %',
                        labels={'total_return':'Total return %'})
    bar_assets_return.layout.showlegend = False
    st.plotly_chart(bar_assets_return)
    
    #plot assets value 
    value_df = portfolio_df[['unrealizedPNL']][:-2]
    bar_assets_value = px.bar(value_df,x=value_df.index,y='unrealizedPNL',text_auto=True,
                        color='unrealizedPNL',
                        # color_discrete_map={True: "green", False: "red"},
                        color_continuous_scale=px.colors.sequential.Viridis,
                        # color_continuous_scale='Inferno',
                        # color_continuous_scale='Bluered_r',
                        # color_continuous_scale=px.colors.sequential.Cividis_r,
                        # color_continuous_scale=["red", "green", "blue"],
                        # color_continuous_scale=px.colors.diverging.BrBG,
                        labels={
                     "unrealizedPNL": "Asset Profit $ ",

                 },
                        
                        title='Assets Profit in USD')
    bar_assets_value.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, texttemplate='%{y:.2f}')
    st.plotly_chart(bar_assets_value)