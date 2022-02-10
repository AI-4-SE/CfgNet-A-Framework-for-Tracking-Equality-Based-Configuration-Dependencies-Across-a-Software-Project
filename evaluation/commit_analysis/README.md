# Analyze Commit History of Software Systems

## Selection of Software Repositories
- Top 100 Repositories (Decemeber 2021) with the most stars that can be analyzed with CfgNet
- dropped 9 repositories as they caused errors, such as errors caused by third part libraries

## Conflict Inspection

1. Selection of repositories and conflicts
    - only repositories are considered for which conflicts have been detected
    - only Modified Option Conflicts will be inspected, since for the remaining conflicts we have no way of telling if the change was intentional or not
    - MissingArtifact/MissingOption/MultiValueConflict will be removed from the csv files
    - 50 randomly selected Modified Option Conflicts for each repository
    - if there were less than 500, we will be inspected all of them

2. Rating
    - yes - broken link between configuration options possibly leads to a potential dependency conflict
    - no - broken link obviously does not lead to a dependency conflict


## Statistics