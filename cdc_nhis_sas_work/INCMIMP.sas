*********************************************************************
 July 20, 2019

 THIS IS AN EXAMPLE OF A SAS PROGRAM THAT CREATES A SAS
 FILE FROM THE PUBLIC USE IMPUTED INCOME ASCII FILES

 THIS IS STORED IN INCMIMP.SAS
*********************************************************************;

* USER NOTE: REPLACE CORRECT PATH AND PARAMETERS BEFORE EXECUTING THE SAS PROGRAM;

%LET YEAR = 2018;       *** provide survey year ***;

  *** path to store the imputed income SAS datasets ***;
LIBNAME  NHIS   "/home/u59443028/nhis_sas";
LIBNAME  LIBRARY   "/home/u59443028/nhis_sas";
* DEFINE VARIABLE VALUES FOR REPORTS;

*  USE THE STATEMENT "PROC FORMAT LIBRARY=LIBRARY"
     TO PERMANENTLY STORE THE FORMAT DEFINITIONS;

*  USE THE STATEMENT "PROC FORMAT" IF YOU DO NOT WISH
      TO PERMANENTLY STORE THE FORMATS.;

**PROC FORMAT LIBRARY=LIBRARY;
PROC FORMAT;

   VALUE INC000X
      25				= "25 Income Imputation"
   ;

   VALUE INC001X
   	  0					 = "0 Reported"
	  1					 = "1 Imputed; no information"
	  2					 = "2 Imputed; reported in categories"
   ;

   VALUE INC002X
      0					= "0 Not top-coded"
	  1					= "1 Top-coded"
   ;

   VALUE INC003X
      0					= "0 Not imputed"
	  1					= "1 Imputed"
   ;

   VALUE INC004X
      1					= "1 Employed"
	  2					= "2 Not employed"
   ;

   VALUE INC005X
      0                  = "0 Reported"
      1                  = "1 Imputed"
   ;
RUN;

%macro allimp;
%do IMPNUM = 1 %to 1;

  *** path to the imputed income ASCII datasets ***;
FILENAME  ASCIIDAT  "/home/u59443028/nhis_sas/incmimp&IMPNUM..dat";

DATA NHIS.INCMIMP&IMPNUM;   *** CREATE A SAS DATA SET ***;

   INFILE ASCIIDAT PAD LRECL=44;

   * DEFINE LENGTH OF ALL VARIABLES;

   LENGTH
		RECTYPE 3		SRVY_YR 4		HHX $6			FMX $2
		FPX $2			IMPNUM 3		FAMINCF2 3		TCINCM_F 3
		FAMINCI2 8		POVRATI3 8		EMPLOY_F 3		EMPLOY_I 3
		ERNYR_F 3		TCEARN_F 3		ERNYR_I2 8
		;

   * INPUT ALL VARIABLES;
   * IMPLIED DECIMAL IS FORMALLY PLACED IN THE APPROPRIATE LOCATION FOR THE VARIABLE POVRATI3;

   INPUT
		RECTYPE 	1-2			SRVY_YR 	3-6		
		HHX 		7-12		FMX 		13-14
		FPX 		15-16		IMPNUM 		17 		
		FAMINCF2	18			TCINCM_F 	19
		FAMINCI2 	20-25		POVRATI3 	26-34 .3
		EMPLOY_F 	35 			EMPLOY_I 	36 			
		ERNYR_F 	37 			TCEARN_F 	38
		ERNYR_I2 	39-44
		;

   * DEFINE VARIABLE LABELS;

   LABEL
		RECTYPE		= "File identifier type"
		SRVY_YR		= "Year of National Health Interview Survey"
		HHX			= "HH identifier"
		FMX			= "Family identifier"
		FPX			= "Person number identifier"
		IMPNUM		= "Imputation number"
		FAMINCF2	= "Family income imputation flag"
		TCINCM_F	= "Family income/poverty ratio top-coded flag"
		FAMINCI2	= "Top-coded family income"
		POVRATI3	= "Ratio of family income to poverty threshold"
		EMPLOY_F	= "Employment status imputation flag"
		EMPLOY_I	= "Person's employment status"
		ERNYR_F		= "Person's earnings imputation flag"
		TCEARN_F	= "Person's earnings top-coded flag"
		ERNYR_I2	= "Person's total earnings last year (top-coded)"
		;

   * ASSOCIATE VARIABLES WITH FORMAT VALUES;
   FORMAT
		RECTYPE		INC000X.
		FAMINCF2	INC001X.
		TCINCM_F	INC002X.
		EMPLOY_F	INC003X.
		EMPLOY_I	INC004X.
		ERNYR_F		INC005X.
		TCEARN_F	INC002X.
		;
RUN;

PROC CONTENTS DATA=NHIS.INCMIMP&IMPNUM;
   TITLE1 "CONTENTS OF THE &YEAR NHIS IMPUTED INCOME FILE, DATASET &IMPNUM";
RUN;
PROC FREQ DATA=NHIS.INCMIMP&IMPNUM;

   TABLES   RECTYPE		SRVY_YR		IMPNUM		FAMINCF2
			TCINCM_F	EMPLOY_F	EMPLOY_I	ERNYR_F
			TCEARN_F
			;
   TITLE1 "FREQUENCY REPORT FOR &YEAR NHIS IMPUTED INCOME FILE, DATASET &IMPNUM";
   TITLE2 '(UNWEIGHTED)';
PROC MEANS DATA=NHIS.INCMIMP&IMPNUM;

	VAR		FAMINCI2	POVRATI3	ERNYR_I2
			;
   TITLE1 "MEANS FOR &YEAR NHIS IMPUTED INCOME FILE, DATASET &IMPNUM";
   TITLE2 '(UNWEIGHTED)';

* USER NOTE: TO SEE UNFORMATTED VALUES IN PROCEDURES, ADD THE
             STATEMENT: FORMAT _ALL_;
RUN;
%end;
%mend allimp;
%allimp;