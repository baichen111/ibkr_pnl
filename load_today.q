d:"_" sv reverse "." vs string .z.d;
files:key sf:`:/home/baichen/ibkr_daily_pnl/ ;
f:` sv sf,c:first files where files like d,"*" ;

hdbdir:`:/home/baichen/ibkr_hdb/ ; 
if[not c=`;
    t:("PSSSFSFFFFFFFS";enlist",")0: f; 
    (` sv hdbdir,(`$string[.z.d]),`pnl`) set .Q.en[hdbdir;t]
    ];
exit 0;