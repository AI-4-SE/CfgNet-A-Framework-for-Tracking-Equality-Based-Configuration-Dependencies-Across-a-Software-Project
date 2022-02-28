# CfgNet: A Framework for Tracking Configuration Dependencies Across a Software Project

Additional material for our paper *CfgNet: A Framework for Tracking Configuration Dependencies Across a Software Projects*.

## Evaluation: Dependency Violation

To evaluate CfgNet's ability to model the configuration landscape of a software project and detect dependency conflicts in it, we followed state of the art practice by violating [configuration dependencies](data/violation_injection/dependencies/dependencies.pdf) in five software projects. You can find the results of the dependency violations [here](data/violation_injection/results/).

Since there was no readily available data set of cross-technology configuration dependencies, we first analyzed Stack Overflow (SO) posts and extracted five reoccurring configuration dependencies.

In the following, we present the SO Analysis and its results as well as the software projects, their configuration dependencies, and the changes (i.e., the file, line number, old value, and new value) we made to violate the dependencies.

### Stack Overflow Analysis

We analyzed Stack Overflow (SO) posts to extract typical real-world configuration dependencies across various technologies.
To this end, we downloaded the SO dataset from the [Stack Exchange Data Dump](https://archive.org/details/stackexchange) on November 12, 2021.
To find relevant SO posts about cross-technology configuration dependencies, we followed previous SO analyses by creating a vocabulary using our currently supported technology-specific plugin names.

- technology-specific plugins: maven, docker, docker-compose, travis, node.js

We filtered the data set using each tag pair from our vocabulary, sorted the resulting posts in descending order, and extracted the first hundred posts. 
In total, we obtained 905 posts for 10 different tag pairs, which we manually reviewed.
You can find the posts for each tag pair in [`data/violation_injection/stackoverflow`](data/violation_injection/stackoverflow/).

The five extracted configuration dependencies and exemplary SO identifiers can be found [here](data/violation_injection/dependencies/dependencies.pdf).

### Results

#### **spring-boot-blog**
This blogging application uses Maven, Docker, a database, and many Spring Technologies, such as Spring Boot, Spring Security, and Spring Data.
These technologies introduce two of the extracted configuration dependencies into the software project.
We injected two dependency conflicts by changing one value of the configuration dependencies, respectively.
Specifically, we injected the first dependency conflict by increasing the version number in the pom.xml, leading to a dependency conflict with Docker's COPY command.
The second dependency conflict was introduced by changing the port in the application.properties, causing a dependency conflict with the port specified in the Dockerfile.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |   8  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2                   |
|  3  | src/main/resources/application.properties                    |   3  | server.port                | 8090                           | 8000                    |

#### **Ward**
Ward is a monitoring tool that uses Docker and Maven as well as JSON and XML files for additional configuration.
In this software project, we found one of the extracted configuration dependencies, as Docker copies the pom.xml to the container, so that the application can be built and run in the container.
We violated the configuration dependency by changing the first argument of Docker's COPY command, which copied the pom.xml to the container.
Here, we replaced the configuration artifact with a file path pointing towards a new directory of the configuration artifact to simulate Docker copying the artifact from another local directory to the container's file system.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  5  | Dockerfile                                                   |  21  | COPY                       | pom.xml                        | app/pom.xml             |

#### **piggymetrics**
Piggy Metrics is a project that demonstrates how to use Spring Boot, Spring Cloud, and Docker for a microservice architecture.
Due to the nature of the microservices, Piggy Metrics consists of multiple services that come with their own configurations.
Among these configurations, we found two of the extracted configuration dependencies and introduced four dependency conflicts into this software project.
The first three dependency conflicts were injected by changing the port of a specific service in its Dockerfile.
This caused two dependency conflicts with Docker Compose and one with the application.yml of the service.
The fourth dependency conflict was caused by renaming the artifactId in the pom.xml of a specific service.
This changed the name of the executable of the service and led to a dependency conflict with the Dockerfile where the old executable is still copied to the container.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | config/pom.xml                                               |   6  | artifactID                 | config                         | configuration           |
|  3  | docker-compose.dev.yml                                       |  10  | config:ports               | 8888:8888                      | 8080:888                |

#### **netflix-oss-example**
The authors of the Netflix OSS Example project aim at demonstrating the spring cloud ecosystem and microservice architecture, showing how different technologies are used such as Spring Cloud, Maven, Docker-Compose, and RabbitMQ.
Here, we violated three configuration dependencies, intentionally injecting five dependency conflicts.
First, we renamed the artifactId in the config-service/pom.xml, causing a conflict with the ADD command in config-service/Dockerfile, since the old executable name is still copied into the container.
Then, we reproduced the internal Docker conflict by changing the destination parameter of the ADD command in eureka-server/Dockerfile, leading to an internal dependency conflict with the Docker's CMD command.
Lastly, we changed the port in the hystrix-dashboard/Dockerfile, which caused one conflict with the application.yml of the hystrix-dashboard and two more with the docker-compose.yml.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | config-service/pom.xml                                       |   8  | artifactId                 | config-service                 | config                  |
|  2  | eureka-server/Dockerfile                                     |  16  | ADD                        | eureka-service.jar             | eureka.jar              |
|  3  | hystrix-dashboard/Dockerfile                                 |  20  | EXPOSE                     | 7979                           | 7777                    |

#### **taskManagement**
Task Management is an application to manage tasks and uses various technologies, such as Maven, Docker, Docker Compose, Spring Boot, and MySQL.
Here, we found three configuration dependency and injected five dependency conflicts.
Specifically, we first changed the version number in the pom.xml, which introduced the first conflict with the Dockerfile.
Next, we renamed the second argument of Docker's COPY command, simulating that the destination of executable has been changed.
This caused the second dependency conflict, since Docker's ENTRYPOINT still used the old destination of the executable in the container.
Finally, we changed the username in the application-dev.yml that is used to access the database, leading to the three conflicts.

| ID  | Configuration Artifact                                       | Line| Option                      | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |  13  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2-SNAPSHOT          |
|  2  | Dockerfile                                                   |   2  | COPY                       | taskManager-0.0.1-SNAPSHOT.jar | taskManager.jar         |
|  4  | src/main/resources/application-dev.yml                       |   4  | spring.datasource.username | dev_user                       | prod_user               |


## Evaluation: Commit History

To demonstrate that cross-technology configuration dependencies are of practical relevance, we analyze the commit history of [top 100 repositories with the most stars from GitHub](data/commit_analysis/repositories.csv) (December 2021) that can be analyzed with CfgNet.
We replaced 9 repositories in our analysis, as they caused errors by third-party libraries during the analysis with CfgNet.
We analyzed the commit history of the subject systems in an automated manner and tracked all detected dependency conflicts for each commit.
The results of applying CfgNet to the commit history of 100 software repositories can be found [here](data/commit_analysis/analysis_statistics.csv).

We found dependency conflicts only for 66 of these repositories, whereas only 56 repositories contained Modified Option Conflicts.
From each of the 56 repositories where we discovered Modified Option Conflicts, we manually analyzed 50 randomly selected conflicts.
In total, we manually inspected [1403 Modified Option Conflicts](data/commit_analysis/results/final_reviewed_conflicts/), annotated 667 (48 %) conflicts with yes, 736 (52 %) with no, and classified the conflicts into five different categories.

Our results demonstrate that even a trivial implementation that does not fully exploit the main advantages of ur approach (e.g., domain knowledge or type information) can find hundreds of potential configuration dependency conflicts in software projects. 
Moreover, the false positives we have found can be mainly traced to a lack of type information and tracking of unnecessary options, which both can be avoided by technology-specific plugins that incorporate that information.

### Evaluation Script

**Important**: Our evaluation scripts assume that they are run on our Slurm cluster if the hostname is `tesla` or starts with `brown`.

You can find the corresponding evaluation scripts either in [`evaluation/violation_injection`](evaluation/violation_injection/) or in [`evaluation/commit_analysis`](evaluation/commit_analysis/).

You can start a evaluation by running `run.sh`.
It takes an optional parameter which is a Git tree-ish (e.g. `master`) that can be used to get a certain version of CfgNet.
The result files will be in `results/`.
You can find the modified repositories in `out/`.
