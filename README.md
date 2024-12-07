## A data workflow to capture daily post-trade profit and loss in US stock market using Airflow and IBKR api
![image](https://github.com/user-attachments/assets/bd9fd484-e51b-40c6-9569-56b384e7a95f)






## Portfolio Daily PnL as of 2024.12.07:
![image](https://github.com/user-attachments/assets/c4cd778c-b591-47e9-89cc-53da27570229)

![image](https://github.com/user-attachments/assets/2dfeae99-747e-438a-8a87-114d48aaf567)

## Start airflow with command:
```
airflow webserver --port 8080
airflow scheduler
```



## Start streamlit with command:
```
streamlit run /home/baichen/ibkr_pnl/dashboards/dashboards_st.py --client.showErrorDetails=false
```






























