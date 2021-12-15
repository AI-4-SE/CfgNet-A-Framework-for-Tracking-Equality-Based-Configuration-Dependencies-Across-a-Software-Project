#!/bin/env/python3
"""Analysis for our paper on CfgNet."""

import os
import os.path
import subprocess

from git import Repo

EVALUATION_FOLDER = "out"

# Every item is a tuple which consists of:
#
#   * An URL to the repository that should be analyzed.
#   * A commit hash of the latest commit of the repository to analyzed to
#     ensure reproducability.
#   * A list of files that should be ignored during the analysis. The files we
#     added to the ignore list are from test runs and are large files that are
#     not configuration but other data.
#   * A list of changes. Each change is a tuple consisting of
#       * The file name
#       * The line number to be changed
#       * The new value of the line
TEST_REPOS = [
    (
        "https://github.com/msk41/taskManagement",
        "a476761baea430bed325fc1e4e6b0473aae96a57",
        [],
        [
            (
                "Dockerfile",
                "2",
                "COPY /target/taskManager-0.0.1-SNAPSHOT.jar taskManager.jar",
            ),
            ("pom.xml", "13", "<version>0.0.2-SNAPSHOT</version>"),
            (
                "src/main/resources/application-dev.yml",
                "4",
                "\ \ \ \ username: prod_user",
            ),
        ],
    ),
    (
        "https://github.com/B-Software/Ward",
        "f9848747933bf2910ae163da9808bf7ea092796e",
        [],
        [("Dockerfile", "21", "COPY --from=builder app/pom.xml /pom.xml")],
    ),
    (
        "https://github.com/sqshq/piggymetrics",
        "fd5ee3c555ea9cd6067eacf3f2a3e8b85fe4fe77",
        [],
        [
            ("config/Dockerfile", "9", "EXPOSE 8080"),
            (
                "config/pom.xml",
                "6",
                "<artifactId>configuration</artifactId>",
            ),
        ],
    ),
    (
        "https://github.com/reljicd/spring-boot-blog",
        "ad754f162b0140cc1f81bea8c8cc9e8a35ce4001",
        [],
        [
            ("pom.xml", "8", "<version>0.0.2</version>"),
            (
                "src/main/resources/application.properties",
                "5",
                "server.port=8000",
            ),
        ],
    ),
    (
        "https://github.com/tayfurunal/mentorship-platform",
        "9b0ab62f28c71c57575bdb2caac153e0201dbacd",
        ["mentorship-client/package-lock.json"],
        [
            (
                "mentorship-backend/src/main/resources/application.properties",
                "4",
                "spring.datasource.password=1234567",
            ),
            ("mentorship-backend/Dockerfile", "10", "EXPOSE 8000"),
            (
                "mentorship-backend/Dockerfile",
                "9",
                "COPY --from=build /workspace/target/*.jar backend.jar",
            ),
        ],
    ),
]


def get_repo_name_from_url(url):
    """
    Return the repository name from the URL.

    :param url: URL to the repository
    :return: Repository name
    """
    repo_name = url.split("/")[-1]
    repo_name = repo_name.split(".")[0]
    return repo_name


def create_ignore_file(ignorelist, repo_folder):
    """
    Create a CfgNet ignore file.

    :param ignorelist: List of file paths to be added to the ignore list.
    :param repo_folder: Target folder of the evaluation.
    """
    os.mkdir(repo_folder + "/.cfgnet")
    file = open(repo_folder + "/.cfgnet/ignore", "w")
    for item in ignorelist:
        print("$ echo " + item + "> " + ".cfgnet/ignore")
        file.write(item + "\n")
    file.close()


def inject_dependency_violation(violation, repo_folder):
    """
    Inject the dependency violation in a repository.
    """
    filename = violation[0]
    linenumber = violation[1]
    newline = violation[2]
    print('$ sed -i "' + linenumber + " c " + newline + '" ' + filename)
    subprocess.run(
        ['sed -i "' + linenumber + " c " + newline + '" ' + filename],
        shell=True,
        cwd=repo_folder,
        executable="/bin/bash",
        check=True,
    )


def process_repo(url, commit, ignorelist, violations):
    """
    Analyze a repository with CfgNet.

    We run `cfgnet validate` after every violation.

    :param url: URL to the repository
    :param commit: Hash of the lastest commit that should be analyzed
    :param ignorelist: List of file paths to ignore in the analysis
    :param violations: Dependency violations to be introduced. Since we run
        cfgnet after every violation the order of the violations matters.
    """
    repo_name = get_repo_name_from_url(url)
    repo_folder = EVALUATION_FOLDER + "/" + repo_name
    results_folder = EVALUATION_FOLDER + "/results/" + repo_name

    print("$ git clone", url, repo_folder)
    print("$ cd", repo_folder)
    repo = Repo.clone_from(url, repo_folder)

    print("$ git checkout", commit)
    repo.git.checkout(commit)

    create_ignore_file(ignorelist, repo_folder)

    print("$ cfgnet init .")
    subprocess.run("cfgnet init .", shell=True, cwd=repo_folder, check=True)

    for index, violation in enumerate(violations):
        inject_dependency_violation(violation, repo_folder)

        print("$ cfgnet validate .")
        with open(results_folder + ".result" + str(index), "w") as outfile:
            subprocess.run(
                "cfgnet validate . ",
                shell=True,
                stdout=outfile,
                cwd=repo_folder,
                check=False,
            )

    subprocess.run(
        ["cp", "-r", repo_folder + "/.cfgnet", results_folder], check=True
    )

    print("Finished evaluation for", url)
    print()


def main():
    """
    Run the analysis.
    """
    # create evaluation folder
    # if os.path.exists(EVALUATION_FOLDER):
    #     subprocess.run(["rm", "-rf", EVALUATION_FOLDER])
    subprocess.run(["mkdir", "-p", EVALUATION_FOLDER + "/results"], check=True)

    print()
    print("+------------+")
    print("| EVALUATION |")
    print("+------------+")
    print()
    for repo in TEST_REPOS:
        process_repo(repo[0], repo[1], repo[2], repo[3])


if __name__ == "__main__":
    main()
