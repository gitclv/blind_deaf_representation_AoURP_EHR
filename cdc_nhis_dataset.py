## Get intersectional values:
# needed for table 2 [age_group, education_group, sex, race_eth, poverty]

# Source age-adjusted data
raw_df = pd.read_csv('flat_lists/samadult.csv')

lite_df = raw_df[['FPX', "HHX", "FMX", "RCS_AFD", "WTFA_SA", 'AGE_P', 'SEX', 'RACERPI2', 'HISPAN_I', 'AHEARST1', 'ABLIND', 'AVISION']].copy()
del raw_df
#print(lite_df.dtypes)

print("Sum of Weights... average of the civilian, noninstitutionalized U.S. population estimates for persons aged 18 and above for February, May, August, and November")
print(sum(lite_df["WTFA_SA"]))

#Respondents were asked, "These next questions are about your hearing without the use of hearing aids or other listening devices. Is your hearing
#excellent, good, [do you have] a little trouble hearing, moderate trouble, a lot of trouble, or are you deaf?" For this table, "a little trouble hearing,"
#"moderate trouble," "a lot of trouble," and "deaf" are combined into one category. Estimates of hearing trouble for 2018 may not be comparable with
#estimates from 2006 and earlier. Regarding their vision, respondents were asked, "Do you have any trouble seeing, even when wearing glasses or
#contact lenses?" Respondents were also asked, "Are you blind or unable to see at all?" For this table, "any trouble seeing" and "blind" are combined
#into one category.

## code id
def pid_recode(fp, hh, fm):
    return str(int(fp))+"_"+str(int(hh))+"_"+str(int(fm))
lite_df['pid'] = lite_df.apply(lambda x: pid_recode(x.FPX, x.HHX, x.FMX), axis=1)

## code sex
def sex_recode(sex):
    if sex == 2:
        return "Female"
    elif sex == 1:
        return "Male"
    else:
        return None
lite_df['sex_clean'] = lite_df['SEX'].apply(sex_recode)

## code age
def age_recode(age):
    if (18 <= age) and (age < 45):
        return "18_44"
    elif age < 65:
        return "45_64"
    elif age < 75:
        return "65_74"
    elif (75 <= age) and (age < 130):
        return "75_plus"
    else:
        return None
lite_df['age_clean'] = lite_df['AGE_P'].apply(age_recode)

## code race
def race_eth_recode(race, eth):
    if eth in np.arange(0, 12):
        return "Hispanic"
    elif race == 1:
        return "White"
    elif race == 2:
        return "Black/African American"
    elif race == 4:
        return "Asian"
    elif race == 6:
        return "Multiracial"
    else:
        return None
lite_df['race_eth_clean'] = lite_df.apply(lambda x: race_eth_recode(x.RACERPI2, x.HISPAN_I), axis=1)

## code hearing disability
def hearing_recode(resp):
    if resp in [1, 2]:
        return "No"
    elif resp in [3, 4, 5, 6]:
        return "Yes"
    else:
        return None
lite_df['hearing_disability'] = lite_df['AHEARST1'].apply(hearing_recode)

## code vision disability
def vision_recode(ablind, avision):
    if (avision == 1) or (ablind == 1): #(vis_ss2 in [2, 3, 4])
        return "Yes"
    elif (avision == 2)  or (ablind == 2): #(vis_ss2 == 1)
        return "No"
    else:
        return None
lite_df['vision_disability'] = lite_df.apply(lambda x: vision_recode(x.ABLIND, x.AVISION), axis=1)

nihis_df = lite_df[["pid", "WTFA_SA", "sex_clean", "age_clean", "race_eth_clean", "hearing_disability", "vision_disability"]]

# TEST if the age number (non-age adjusted in https://ftp.cdc.gov/pub/Health_Statistics/NCHS/NHIS/SHS/2018_SHS_Table_A-6.pdf)
#   come with the application of WTFA_SA to raw data
age_eight_groups = nihis_df.groupby(['age_clean', 'vision_disability'])['WTFA_SA'].sum()
denominators = [sum(age_eight_groups[0:2]),
               sum(age_eight_groups[0:2]),
               sum(age_eight_groups[2:4]),
               sum(age_eight_groups[2:4]),
               sum(age_eight_groups[4:6]),
               sum(age_eight_groups[4:6]),
               sum(age_eight_groups[6:]),
               sum(age_eight_groups[6:])]

# TEST SUCCESSFULL
age_eight_groups / denominators

# POVERTY
# load supplementary file
incmip_raw_df = pd.read_csv('flat_lists/incmimp1.csv')
incmip_raw_df['pid'] = incmip_raw_df.apply(lambda x: pid_recode(x.FPX, x.HHX, x.FMX), axis=1)

nihis_df = nihis_df.merge(incmip_raw_df[['pid', 'POVRATI3']],
                          how='left',
                          on='pid')
del incmip_raw_df

def pov_recode(pov):
    if pov <= 1:
        return "Poor"
    elif pov <= 2:
        return "Near Poor"
    else:
        return "Not Poor"
nihis_df['pov_clean'] = nihis_df['POVRATI3'].apply(pov_recode)

# EDICATON
person_raw_df = pd.read_csv('flat_lists/personsx.csv')
person_lite_df = person_raw_df[['FPX', "HHX", "AGE_P", "FMX", "EDUC1"]].copy()
del person_raw_df
person_lite_df = person_lite_df[person_lite_df['AGE_P'].astype(int) >= 18]
person_lite_df['pid'] = person_lite_df.apply(lambda x: pid_recode(x.FPX, x.HHX, x.FMX), axis=1)

nihis_df = nihis_df.merge(person_lite_df[['pid', 'EDUC1']],
                          how='left',
                          on='pid')

## POVERTY
def edu_recode(edu):
    if edu in np.arange(0,13):
        return 'Less than a high school degree or equivalent'
    elif edu in [13, 14]:
        return 'Highest Grade: Twelve Or GED'
    elif edu in [15, 16, 17]:
        return 'Highest Grade: College One to Three'
    elif edu in [21, 20, 19, 18]:
        return 'College graduate or advanced degree'
    else:
        return None
nihis_df['edu_clean'] = nihis_df['EDUC1'].apply(edu_recode)
