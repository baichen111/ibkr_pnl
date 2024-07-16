csv_files:fs where (fs:key sf:`:/home/baichen/ibkr_daily_pnl/) like "*.csv";
fp_files:(` sv sf,) @/: csv_files ; // full-path csv files

{
    hdbdir:`:/home/baichen/ibkr_hdb/ ;
    t:("PSSSFSFFFFFFFS";enlist",")0: x;
    d:`$string first `date$exec distinct date from t;
    savedir: ` sv hdbdir,d,`pnl` ;
    savedir set .Q.en[hdbdir;t];
    -1 "Saved ",string[d]," to hdb ",string hdbdir;
 }'[fp_files];
 exit 0;





