# Analyze Commit History of Software Systems

## Selection of Software Repositories
- Top 100 Repositories with the most stars
- no further criteria
- script automatically identifies the top 100 repositories (December 2021)

## Results

- if the analysis between two commits takes longer than 20 seconds, we throw a TimeoutError
- Timeout: 20 second

1. First Analysis Run
    - out of 100 repositories, 85 could be analyzed without errors
    - for 15 repositories, different errors occurred such as IndexError, yaml.ComposeError, TypeError, TimeoutError etc.
    - errors will be fixed for second run, except the TimeoutError
    - for the TimeOutError, we will try some profiling, but we are not sure if this can reduce the time needed for the analysis
    - we can not fix third-party library errors 
2. Second Analysis Run
    - most errors could be fixed
    - TimeoutErrors still exist
3. Third Analysis Run
    - all repositories with a TimeoutError will be analyzed again
    - Timeout block will be removed for this run


## Conflict Inspection

1. Selection of repositories and conflicts
    - only repositories are considered for which conflicts have been detected
    - only ModifiedOptionConflicts will be inspected, since for the remaining conflicts we have no way of telling if the change was intentional or not
    - MissingArtifact/MissingOption/MultiValueConflict will be removed from the csv files
    - at the most 100 ModifiedOptionConflicts for each repository
    - if number of detected ModifiedOptionConflicts is lower than 100, all of the detected ModifiedOptionConflicts will be inspected
    - if number of detected ModifiedOptionConflicts is higher than 100, we randomly select 100 ModifiedOptionConflicts for inspection

2. Rating
    - yes - we believe that the conflict is a real issue
    - no - we believe that the conflict is not a real issue
    - maybe - we are not sure if the conflict really leads to a configuration conflict

## How to get final results/conflicts to inspect
- copy csv from `evaluation/commit_analysis/results/*` to `evaluation/commit_analysis/conflict_inspection/all`
- run `select_conflicts_randomly.py` to get the conflicts to inspect
- the script automatically identifies the repositories for which ModifiedOptionConflicts have been detected and selects randomly 100 of them (if more were detected) or just copies the csv file to `evaluation/commit_analysis/conflict_inspection/final` (if less than 100 were detected)