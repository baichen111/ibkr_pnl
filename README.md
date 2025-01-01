## A data workflow to capture daily post-trade profit and loss in US stock market using Airflow and IBKR api
![image](https://github.com/user-attachments/assets/bd9fd484-e51b-40c6-9569-56b384e7a95f)






## Portfolio Daily PnL as of 2024.12.31:
![image](https://github.com/user-attachments/assets/faddd047-42ab-4103-9222-ebf6ac5270d0)



![image](https://github.com/user-attachments/assets/51da6713-a4e3-4af7-8ee8-8c7fb6efcf7e)






## Start airflow with command:
```
airflow webserver --port 8080
airflow scheduler
```



## Start streamlit with command:
```
streamlit run /home/baichen/ibkr_pnl/dashboards/dashboards_st.py --client.showErrorDetails=false
```






























