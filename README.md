## A data workflow to capture daily post-trade profit and loss in US stock market using Airflow and IBKR api
![image](https://github.com/user-attachments/assets/bd9fd484-e51b-40c6-9569-56b384e7a95f)






## Portfolio Daily PnL as of 2025.01.03:
![image](https://github.com/user-attachments/assets/2e993fe8-0b2c-4f0b-9daa-198b2b943fb2)




![image](https://github.com/user-attachments/assets/0ce05721-1e53-4dcd-b412-37d63feb3feb)








## Start airflow with command:
```
airflow webserver --port 8080
airflow scheduler
```



## Start streamlit with command:
```
streamlit run /home/baichen/ibkr_pnl/dashboards/dashboards_st.py --client.showErrorDetails=false
```






























