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