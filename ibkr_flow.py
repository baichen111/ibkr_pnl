# airflow schedule shell commands

from  datetime import datetime,timedelta
import time
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

defaul_args = {
    'owner':'baichen', # owner is user airflow
    'start_date':datetime(2024,7,1), # DAT start time first time
    'retries':10,  #retry times if failed
    'retry_delay':timedelta(minutes=5), # retry interval
}

dag = DAG(
    dag_id='ibkr_trade', #displays in webUI
    default_args=defaul_args,
    # schedule_interval=timedelta(days=1) , # can be days, weeks,hours, minutes
    # schedule_interval='@daily',
    schedule_interval="0 4 * * 2-6",   #crontab  style 
    # schedule_interval="* * * * *",
    catchup=False  # False : will not backfill previous data
)


#create tasks
start = BashOperator(
    task_id = 'start',
    bash_command='echo "daily pnl starts"',
    dag = dag
)

daily_pnl = BashOperator(
    task_id = 'daily_pnl',
    bash_command='/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/runPnL.py',
    dag = dag
)

daily_pnl_sensor = FileSensor(
    task_id = 'daily_pnl_file_sensor',
    filepath = '/home/baichen/ibkr_daily_pnl/'+time.strftime("%d_%m_%Y")+'_DailyPnL.csv',
    poke_interval = 10,
    dag = dag
    )

daily_assets_pnl = BashOperator(
    task_id = 'daily_load_assets',
    bash_command='/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/load_assets.py',
    dag = dag
)

daily_pnl_plot = BashOperator(
    task_id = 'daily_pnl_plot',
    bash_command='/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/plot_pnl.py',
    dag = dag
)

end = BashOperator(
    task_id = 'end',
    bash_command='echo "daily pnl ends"',
    dag = dag
)

#load daily pnl with kdb
daily_pnl_hdb_Q = BashOperator(
    task_id = 'daily_pnl_hdb_Q',
    bash_command='/home/baichen/q/l64/q /home/baichen/ibkr_pnl/load_today.q',
    dag = dag
)

#send daily report
daily_report_email = BashOperator(
    task_id = 'daily_report_email',
    bash_command='/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/send_report.py',
    dag = dag
)

#generate watch list css file
generate_watch_list = BashOperator(
    task_id = 'generate_watch_list',
    bash_command = '/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/watchlist.py',
    dag = dag
)

#send watch list email
send_watchlist = BashOperator(
    task_id = 'send_watchlist',
    bash_command = '/home/baichen/anaconda3/bin/python /home/baichen/ibkr_pnl/send_watchlist.py',
    dag = dag
)
#tasks dependencies
start >> daily_pnl  >> daily_pnl_sensor >> [daily_assets_pnl,daily_pnl_plot,daily_pnl_hdb_Q,daily_report_email] >> end 
start >> generate_watch_list >> send_watchlist >> end