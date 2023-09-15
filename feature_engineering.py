# bring in cohort definition codes
v2_list = pd.read_csv("flat_lists/vision_2.csv", header=None).iloc[:,0].values
v1_list = pd.read_csv("flat_lists/vision_middle_cohort.csv", header=None).iloc[:,0].values

h2_list = pd.read_csv("flat_lists/hearing_2.csv", header=None).iloc[:,0].values
h1_list = pd.read_csv("flat_lists/hearing_middle_cohort.csv", header=None).iloc[:,0].values


def cohort_include_excluder(snomed_stand_str, round_num):
  """
  Simple tracking of multiple cohorts from initial AoURP SQL code dataframe (not provided in this repo).
  """
    if round_num == 2:
        if snomed_stand_str in v2_list:
            return "vision"
        elif snomed_stand_str in h2_list:
            return "hearing"
        else:
            return "excluded"
    elif round_num == 1:
        if snomed_stand_str in v1_list:
            return "vision"
        elif snomed_stand_str in h1_list:
            return "hearing"
        else:
            return "excluded"

eye_ear_conditions['Cond_Category_R1'] = eye_ear_conditions.apply(
        lambda x: cohort_include_excluder(x['standard_concept_name'], 1), axis = 1)
print("Done r1!")

eye_ear_conditions['Cond_Category_R2'] = eye_ear_conditions.apply(
        lambda x: cohort_include_excluder(x['standard_concept_name'], 2), axis = 1)
print("Done r2!")


#####################################################################################################
# Use survey question dataframe created using AoURP generate SQL (not included in this repo).

# impute to median within given brackets
household_to_inc_d = {"0":12140,
                "1":16460,
                "2":20780,
                "3":25100,
                "4":29420,
                "5":33740,
                "6":38060,
                "7":42380,
                "8":46700,
                "9":51020,
                "10":55340}
answer_dict = {"Annual Income: 100k 150k":(125000),
    "Annual Income: 10k 25k":17500,
    "Annual Income: 150k 200k":175000,
    "Annual Income: 25k 35k":30000,
    "Annual Income: 35k 50k":42500,
    "Annual Income: 50k 75k":62500,
    "Annual Income: 75k 100k":87500,
    "Annual Income: less 10k":5000,
    "Annual Income: more 200k":200000}

def status(row):
    inc, need = row[0], row[1]
    if inc <= need:
        return "Poor"
    if inc <= need*2:
        return "Near poor"
    else:
        return "Not poor"

# Relevant survey questions in AoURP concept id
household_survey_df = all_survey_df[all_survey_df['question_concept_id'].isin([1585375, 1585889])]
fam_squared = pd.merge(household_survey_df, household_survey_df, on='person_id')
valid_x = [str(r) for r in range(11)]

fam_real = fam_squared[fam_squared['answer_x'].isin(valid_x)]
fam_real = fam_real[["Annual Income" in f for f in fam_real['answer_y']]]
fam_three_col = fam_real[["person_id", "answer_x", "answer_y"]]
fam_three_col.head(5)

fam_three_col["trans_y"] = fam_three_col['answer_y'].map(answer_dict)

fam_three_col["need"] = fam_three_col['answer_x'].map(household_to_inc_d)
fam_three_col = fam_three_col.dropna()

fam_three_col['status'] = fam_three_col[['trans_y', 'need']].apply(status, axis=1)
