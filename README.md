## A data workflow to capture daily post-trade profit and loss in US stock market using Airflow and IBKR api
![image](https://github.com/user-attachments/assets/bd9fd484-e51b-40c6-9569-56b384e7a95f)






## Portfolio Daily PnL as of 2024.12.07:
![image](https://github.com/user-attachments/assets/c2746613-7902-46f6-8423-79c7d96d91bb)


![image](https://github.com/user-attachments/assets/3c99ab80-0dde-4dc4-a43a-8c49f9ac7600)




## Start airflow with command:
```
airflow webserver --port 8080
airflow scheduler
```



## Start streamlit with command:
```
streamlit run /home/baichen/ibkr_pnl/dashboards/dashboards_st.py --client.showErrorDetails=false
```






























