d:"_" sv reverse "." vs string .z.D;
files:key sf:`:/home/baichen/ibkr_daily_pnl/ ;
f:` sv sf,c:first files where files like d,"*" ;

hdbdir:`:/home/baichen/ibkr_hdb/ ; 
if[not c=`;
    t:("PSSSFSFFFFFFFSSS";enlist",")0: f; 
    (` sv hdbdir,(`$string[.z.D]),`pnl`) set .Q.en[hdbdir;t];
    -1 "Saved ",string[.z.D]," to hdb ",string hdbdir;
    ];
exit 0;