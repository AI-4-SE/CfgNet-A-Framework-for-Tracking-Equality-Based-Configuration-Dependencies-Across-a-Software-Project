# CfgNet: A Framework for Tracking Configuration Dependencies Across a Software Project

Additional material for our paper *CfgNet: A Framework for Tracking Configuration Dependencies Across a Software Project*.

## Evaluation: Dependency Violation

To evaluate CfgNet's ability to model the configuration landscape of a software project and detect dependency conflicts in it, we followed state of the art practice by violating configuration dependencies in five software projects. You can find the results of the dependency violations [here](data/violation_injection/results/).

Since there was no readily available data set of cross-technology configuration dependencies, we first analyzed Stack Overflow (SO) posts and extracted [ten reoccurring configuration dependencies](data/violation_injection/all_dependencies.pdf).
For the dependency violation injection, we selected the four most common cross-technology configuration dependencies and the top most common internal configuration dependencies.
The selected configuration dependencies can be found [here](data/violation_injection/selected_dependencies.pdf)

In the following, we present the subject systems and the changes (i.e., the file, line number, old value, and new value) that we made to violate the dependencies.

### **spring-boot-blog**
This blogging application uses Maven, Docker, a database, and many Spring Technologies, such as Spring Boot, Spring Security, and Spring Data.
These technologies introduce two of the extracted configuration dependencies into the software project.
We injected two dependency conflicts by changing one value of the configuration dependencies, respectively.
Specifically, we injected the first dependency conflict by increasing the version number in the pom.xml, leading to a dependency conflict with Docker's COPY command.
The second dependency conflict was introduced by changing the port in the application.properties, causing a dependency conflict with the port specified in the Dockerfile.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |   8  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2                   |
|  3  | src/main/resources/application.properties                    |   3  | server.port                | 8090                           | 8000                    |

### **Ward**
Ward is a monitoring tool that uses Docker and Maven as well as JSON and XML files for additional configuration.
In this software project, we found one of the extracted configuration dependencies, as Docker copies the pom.xml to the container, so that the application can be built and run in the container.
We violated the configuration dependency by changing the first argument of Docker's COPY command, which copied the pom.xml to the container.
Here, we replaced the configuration artifact with a file path pointing towards a new directory of the configuration artifact to simulate Docker copying the artifact from another local directory to the container's file system.

| ID  | Configuration Artifact                                       | Line | Option                     | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  5  | Dockerfile                                                   |  21  | COPY                       | pom.xml                        | app/pom.xml             |

#### **piggymetrics**
Piggy Metrics is a project that demonstrates how to use Spring Boot, Spring Cloud, and Docker for a microservice architecture.
Due to the nature of the microservices, Piggy Metrics consists of multiple services that come with their own configuration artifacts.
Among these configuration artifacts, we found two of the extracted configuration dependencies and introduced four dependency conflicts into this software project.
The first three dependency conflicts were injected by changing the port of a specific service in its Dockerfile.
This caused two dependency conflicts with Docker Compose and one with the application.yml of the service.
The fourth dependency conflict was caused by renaming the artifactId in the pom.xml of a specific service.
This changed the name of the executable of the service and led to a dependency conflict with the Dockerfile where the old executable is still copied to the container.
However, this change also caused an unexpected conflict with the parent pom.xml, because the parent pom.xml also specified the service name. 
We believe that this a real dependency conflict, because when if name of a service is changed, all other configuration options that refer to the service name should change as well.

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
Similary to piggymetrics, the change of the artifactId caused an unexpected conflict with the parent pom.xml.
Again, we believe that this a real dependency conflict.

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
However, we expected to detect only one dependency conflict.
The problem here is that the project incorporates different Spring environment configurations file, since we found configuration files for the dev environment. Currently, we do not distinguish different Spring environments, however, we believe that when the credentials of a database are changed, the current environment does not matter.


| ID  | Configuration Artifact                                       | Line| Option                      | Old Value                      | New Value               |
|:----|:-------------------------------------------------------------|-----:|:---------------------------|:-------------------------------|:------------------------|
|  1  | pom.xml                                                      |  13  | version                    | 0.0.1-SNAPSHOT                 | 0.0.2-SNAPSHOT          |
|  2  | Dockerfile                                                   |   2  | COPY                       | taskManager-0.0.1-SNAPSHOT.jar | taskManager.jar         |
|  4  | src/main/resources/application-dev.yml                       |   4  | spring.datasource.username | dev_user                       | prod_user               |


In total, we injected 15 known dependency violations into five subject systems selected from GitHub. 
We found all injected dependency conflicts and even four more. 
Those conflicts were caused by changing a certain service name and database credentials.
With this evaluation, we demonstrated CfgNet's main application scenario and its potential for daily use.
We also showed how CfgNet helps to prevent possible configuration dependency conflicts during software development and maintenance.


## Evaluation: Commit History

To demonstrate the need to efficiently track cross-technology configuration dependencies, we analyzed the commit history of the top [50 software repositories](data/commit_analysis/repositories.csv) with the most stars from GitHub (June 2022) that incoporated at least two technologies that we cover with our implementation.
We replaced repositories that could not be analyzed due to errors caused by third-party libraries and that did not represent real software systems, such as collections of best practices, link hubs, or frameworks.
We analyzed the commit history of the subject systems in an automated manner and tracked all detected dependency conflicts for each commit.
The results of applying CfgNet to the commit history of 50 software repositories can be found [here](data/commit_analysis/analysis_statistics.csv).

We found dependency conflicts in 39 of these repositories, whereas 32 repositories contained Modified Option Conflicts.
From each of the 32 repositories, we sampled 50 Modified Option Conflicts and reviewed them. 
If there were less than 50 conflicts, we reviewed all of them.
In total, we manually inspected [883 Modified Option Conflicts](data/commit_analysis/conflict_inspection/reviewed/), annotated 785 (89 %) conflicts with yes (i.e., true positives), 98 (11 %) with no, and classified the conflicts into different categories based on their ratings and the involved configuration types.

Our results demonstrate our current implementation, which includes nine technology plugins and a general linker, can find hundreds of potential configuration conflicts in software projects, showing that configuration dependencies occur and matter in practice.
Especially, the high number of affected software projects and the manual analysis with about 89~% true positives indicate not only the relevance of our approach for real-world software projects, but also its applicability already in its current state.
In addition, we found that the false positives can be mainly traced back to the implementation of plugins due to a lack of domain knowledge and tracking of unnecessary options. 
This confirms that plugins are the key success factor for our approach, as they not only determine how much information a network contain, but also support the linking process by providing type information for configuration options.

### Evaluation Scripts

We ran our evaluation scripts on a cluster that uses multiple compute nodes with 256~GB RAM, 2 x AMD EPYC 7302 á 16 x 3.0~GHz CPU, running Debian GNU/Linux 10 (buster).
You can find the corresponding evaluation scripts either in [evaluation/violation_injection](evaluation/violation_injection/) or in [evaluation/commit_analysis](evaluation/commit_analysis/).
You can start a evaluation by running `run.sh`.
It takes an optional parameter which is a Git tree-ish (e.g. `main` or `eval`) that can be used to get a certain version of CfgNet.
The result files will be in `results/`.
You can find the modified repositories in `out/`.

**Important**: Our evaluation scripts assume that they are run on our Slurm cluster if the hostname is `tesla` or starts with `brown`.

