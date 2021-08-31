# CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies

Additional material for our paper *CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies*.
You can find the pre-print of the paper here.

Please cite our paper when using the data set:
Nicolai Ruckel, Sebastian Simon, and Norbert Siegmund. CfgNet: A Technology-agnostic Framework for Tracking Configuration Dependencies. In *Proceedings of the ...*

## Stack Overflow Analysis

We analyzed Stack Overflow (SO) posts to extract typical real-world configuration dependencies across various technologies.
To this end, we downloaded the SO dataset from the [Stack Exchange Data Dump](https://archive.org/details/stackexchange) on June 7, 2021.
To find related SO posts about cross-technology configuration dependencies, we followed previous SO analyses by creating a vocabulary using technology-specific plugin names and other popular technologies that cover common areas of software development.

- technology-specific plugins: maven, docker, docker-compose, travis
- popular technologies: spring-boot, database angular

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

## Dependency Violation

To evaluate CfgNet's ability to model the configuration landscape of a software project and detect dependency conflicts in it, we followed state of the art practice by violating the extracted [configuration dependencies](dependencies.pdf) in five software projects. The following table shows the software projects, their configuration dependencies, and the changes (i.e., the file, line number, old value, and new value) we made to inject the dependency violations.

### spring-boot-blog

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |   8  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2                   |
|  3  | src/main/resources/application.properties                    |   3  | server.port                | 8090                           | 8000                    |

### Ward

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  5  | Dockerfile                                                   |  21  | COPY                       | pom.xml                        | app/pom.xml             |

### piggymetrics

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | config/pom.xml                                               |   6  | artifactID                 | config                         | configuration           |
|  3  | docker-compose.dev.yml                                       |  10  | config:ports               | 8888:8888                      | 8080:888                |

### mentorship-platform

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  2  | mentorship-backend/Dockerfile                                |   9  | COPY                       | app.jar                        | backend.jar             |
|  3  | mentorship-backend/Dockerfile                                |  10  | EXPOSE                     | 8080                           | 8000                    |
|  4  | mentorship-backend/src/main/resources/application.properties |   4  | spring.datasource.password | password                       | 1234567                 |

### taskManagement

| ID  | Configuration Artifact                                       | Line| Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |  13  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2-SNAPSHOT          |
|  2  | Dockerfile                                                   |   2  | COPY                       | taskManager-0.0.1-SNAPSHOT.jar | taskManager.jar         |
|  4  | src/main/resources/application-dev.yml                       |   4  | spring.datasource.username | dev_user                       | prod_user               |

## Evaluation Script

**Important**: Our evaluation script assumes that it's run on our Slurm cluster if the hostname is `tesla` or starts with `brown`.

You can find our evaluation script in [`evaluation/`](evaluation).

You can start the evaluation by running `run.sh`.
It takes an optional parameter which is a Git tree-ish (e.g. `master`) that can be used to get a certain version of CfgNet.
The result files will be in `results/`.
You can find the modified repositories in `out/`.
