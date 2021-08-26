#!/bin/env/python3
"""Analysis for our paper on CfgNet."""

import multiprocessing
import os
import os.path
import subprocess

from git import Repo
from joblib import Parallel, delayed

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
            ("pom.xml", "13", "<version>0.0.2-SNAPSHOT</version>"),
            (
                "Dockerfile",
                "2",
                "COPY /target/taskManager.jar taskManager.jar",
            ),
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
            ("docker-compose.dev.yml", "10", "\ \ \ \ \ \ - 8080:8888"),
            (
                "account-service/pom.xml",
                "6",
                "<artifactId>acc-service</artifactId>",
            ),
        ],
    ),
    (
        "https://github.com/Emmanuelraj/inventory-system",
        "3c36dbe416fc824d4a41c0db3887d1d6416447cf",
        [],
        [
            ("pom.xml", "13", "<version>0.0.2</version>"),
            (
                "Dockerfile",
                "2",
                "ADD target/inventory-system-0.0.1-SNAPSHOT.jar inventory-system.jar",
            ),
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
        file.write(item + "\n")
    file.close()


def inject_dependency_violation(violation, repo_folder):
    filename = violation[0]
    linenumber = violation[1]
    newline = violation[2]
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

    :param url: URL to the repository
    :param commit: Hash of the lastest commit that should be analyzed
    :param ignorelist: List of file paths to ignore in the analysis
    """
    repo_name = get_repo_name_from_url(url)
    repo_folder = EVALUATION_FOLDER + "/" + repo_name
    results_folder = EVALUATION_FOLDER + "/results/" + repo_name

    repo = Repo.clone_from(url, repo_folder)

    repo.git.checkout(commit)

    create_ignore_file(ignorelist, repo_folder)

    with open(results_folder + ".init", "w") as outfile:
        subprocess.run(
            "cfgnet init .",
            shell=True,
            cwd=repo_folder,
            check=True,
            stdout=outfile,
            stderr=subprocess.STDOUT,
        )

    for violation in violations:
        inject_dependency_violation(violation, repo_folder)

    with open(results_folder + ".result", "w") as outfile:
        subprocess.run(
            "cfgnet validate . ",
            shell=True,
            stdout=outfile,
            stderr=subprocess.STDOUT,
            cwd=repo_folder,
            check=False,
        )

    subprocess.run(
        ["cp", "-r", repo_folder + "/.cfgnet", results_folder], check=True
    )


def main():
    """
    Run the analysis.
    """
    # create evaluation folder
    # if os.path.exists(EVALUATION_FOLDER):
    #     subprocess.run(["rm", "-rf", EVALUATION_FOLDER])
    subprocess.run(["mkdir", "-p", EVALUATION_FOLDER + "/results"], check=True)

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(
        delayed(process_repo)(url, commit, ignorelist, violations)
        for url, commit, ignorelist, violations in TEST_REPOS
    )


if __name__ == "__main__":
    main()
