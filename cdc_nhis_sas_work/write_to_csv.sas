/*export data to file called data.csv*/
DATA my_bdat; 
  set '/home/u59443028/nhis_sas/incmimp1.sas7bdat'; 
 
proc export data=my_bdat
    outfile="/home/u59443028/nhis_sas/incmimp1.csv"
    dbms=csv
    replace;
run;