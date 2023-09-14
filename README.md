# nm_underrepresentation
Reproducibility aid for publication (DOI:_todo_). Some code removed along AoURP guidelines.

- Ethos:
    - This code should allow technical users to digest the exact logic behind the following contributions for this paper:
        - Scientific data visualizations. Although strucutred data is owned by the AoURP and private to the participants, these helper functions/function calls produced our figures.
        - Feature engineering. This includes inclusion/exclusion logic, and a handfull of computed features like povety status from survey data on household size and income.

## Filesystem

- visualization.py: functions and example function calls to produce figure components from structured data (AoURP data not provided)
- cdc_nhis_dataset.py: code to create a python dataframe from cdc_data
- cdc_nhis_sas_work/contents:
    - sas code, sas data, and public helper data requried to begin working with CDC-NHIS data
- flat_condition_lists/contents:
    - our clinician reviewed SNOMED "standard concept name" lists for 4 cohorts. The "middle" cohorts are utilized in the publication, while the "_2" cohorts represent complete bilateral blindness and deafness.
