# CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies

Additional material for our paper *CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies*.
You can find the pre-print of the paper here.

Please cite our paper when using the data set:
Nicolai Ruckel, Sebastian Simon, and Norbert Siegmund. CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies. In *Proceedings of the ...*

## Stack Overflow Analysis

We analyzed Stack Overflow (SO) posts to extract typical real-world configuration dependency.
To this end, we downloaded the SO dataset from the Stack Exchange Data Dump on June 7, 2021.
To find relateded SO posts about cross-technology configuration dependencies, we followed previous SO analyses by creating a vocabulary using technology-specific plugin names and other popular technologies that cover common areas of software development.

- technology-specific plugins: maven, docker, docker-compose, travis
- popular technologies: spring-boot, database angular
You can find the tag pairs [here](data/).

We filtered the data set using each tag pair from our vocabulary, sorted the resulting posts in descending order, and extracted the first hundred posts.
In total, we obtained 21 tag pairs with up to 100 posts.
You can find the tag pairs in [`data/`](data/).

To focus on the most relevant tag pair combinations, we calculated for each tag pair a total score value by summing the score value of its posts.
The table shows the top five tag pair combinations and their total score value.

| Tag Pair               | Total Score |
|------------------------|-------------|
| docker, docker-compose |        16632|
| maven, spring-boot     |         4403|
| docker, spring boot    |          861|
| maven, docker          |          859|
| docker, database       |          824|

We selected the top five tag pairs with the highest total score value, and manually inspected their posts.

In total, we manually inspected 500 SO posts and extracted five meaningful cross-technology configuration dependencies. 
The extracted configuration dependencies appeared in several SO posts, indicating that we have extracted typical real-world configuration dependency examples that developers indeed encounter in practice.
The five extracted configuration dependencies and exemplary SO identifiers can be found [here](dependencies.pdf).

## Evaluation

**Important**: Our evaluation script assumes that it's run on our Slurm cluster if the hostname is `tesla` or starts with `brown`.

You can find our evaluation script in [`evaluation/`](evaluation).

You can start the evaluation by running `run.sh`.
It takes an optional parameter which is a Git tree-ish (e.g. `master`) that can be used to get a certain version of CfgNet. 
The result files will be in `results/`.
You can find the modified repositories in `out/`.
