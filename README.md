# Breadcrumbsblind_deaf_representation_AoURP_EHR
Reproducibility aid for publication (DOI:_todo_). Some code removed along AoURP guidelines.

- Ethos:
    - This code should allow technical users to digest the exact logic behind the following contributions for this paper:
        - Scientific data visualizations. Although strucutred data is owned by the AoURP and private to the participants, these helper functions/function calls produced our figures.
        - Feature engineering. This includes inclusion/exclusion logic, and a handfull of computed features like povety status from survey data on household size and income.
    - Because the **All of Us Research Program** manages all participant data (and the python+SQL code to create cohorts from it) under the *Researcher Workbench*, no participant data or database query/manipulation code is included in this repository.
        - The functions shared here will assist those seeking to reproduce our work after they have ingested the cohort.
        - To utilizes these functions, a researcher first needs to reference the online supplement which includes the SNOMED "standard concept name" of each condition for inclusion in our primary cohorts, then create their own cohort by entering those into the *AoURP Researcher Workbench -- Cohort Builder*.
        - After those steps, the *Researcher Workbench* will generate SQL code compliant with the current data model of the AoURP. It is likely some minor grouping/transformations be performed to pass the data into the functions included here.

## Filesystem

- visualization.py: functions and example function calls to produce figure components from structured data (AoURP data not provided)
- cdc_nhis_dataset.py: code to create a python dataframe from cdc_data
- feature_engineering: code that does initial processing of dataframes created by AoURP generated SQL (AoURP generated code not provided in this repo)
- cdc_nhis_sas_work/contents:
    - sas code, sas data, and public helper data requried to begin working with CDC-NHIS data
- flat_condition_lists/contents:
    - our clinician reviewed SNOMED "standard concept name" lists for 4 cohorts. The "middle" cohorts are utilized in the publication, while the "_2" cohorts represent complete bilateral blindness and deafness.
