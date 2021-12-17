"""Analysis for our paper on CfgNet."""

import multiprocessing
import os
import os.path
import subprocess
import sys

from git import Repo
from joblib import Parallel, delayed

# The folder where we store our results.
EVALUATION_FOLDER = "out"

# Every item is a tuple which consists of:
#
#   * An URL to the repository that should be analyzed.
#   * A commit hash of the latest commit of the repository to analyzed to
#     ensure reproducability.
#   * A list of files that should be ignored during the analysis. The files we
#     added to the ignore list are from test runs and are large files that are
#     not configuration but other data.
#
# If you change the number of repositories (e.g. the length of this list), you
# have to adjust the array range in `array.sbatch`.
TEST_REPOS = [
    (
        "https://github.com/simisimon/maven_repo",
        "e1a4febe400099e155635e1ef2d63ede746c38ab",
        [],
    ),
]


def get_repo_name_from_url(url):
    """
    Analyze a repository with CfgNet.
    :param url: URL to the repository
    :return: Repository name
    """
    repo_name = url.split("/")[-1]
    repo_name = repo_name.split(".")[0]
    return repo_name


def process_repo(url, commit, ignorelist):
    """
    Analyze a repository with CfgNet.
    :param url: URL to the repository
    :param commit: Hash of the lastest commit that should be analyzed
    :param ignorelist: List of file paths to ignore in the analysis
    """
    repo_name = get_repo_name_from_url(url)
    repo_folder = EVALUATION_FOLDER + "/" + repo_name
    results_folder = EVALUATION_FOLDER + "/results/" + repo_name

    print("Cloning repository", repo_name)
    repo = Repo.clone_from(url, repo_folder)

    print("Checkout commit", commit)
    repo.git.checkout(commit)

    print("Create ignore file")
    create_ignore_file(ignorelist, repo_folder)

    print("Starting evaluation for", url)
    subprocess.run(
        "cfgnet analyze .", shell=True, cwd=repo_folder, executable="/bin/bash"
    )

    print("Clean up log file")
    clean_up_log(repo_name, repo_folder)

    subprocess.run(["cp", "-r", repo_folder + "/.cfgnet", results_folder])
    print("Finished evaluation for", url)


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


def clean_up_log(repo_name, repo_folder):
    """Remove DEBUG statements from log file."""
    log_file = repo_folder + "/.cfgnet/logs/" + repo_name + ".log"
    subprocess.run(["sed", "-i.bak", "'/DEBUG/d'", log_file])


def main():
    """
    Run the analysis.
    There are two ways to run this. Either, you pass an integer and then the
    corresponding repository of `TEST_REPOS` will be analyzed or you don't pass
    anything which will analyze all the repositories.
    """
    # create evaluation folder
    # if os.path.exists(EVALUATION_FOLDER):
    #     subprocess.run(["rm", "-rf", EVALUATION_FOLDER])
    subprocess.run(["mkdir", "-p", EVALUATION_FOLDER + "/results"])

    # If only one argument is provided we run the evaluation for all
    # repositories. This is done in parallel.
    # Otherwise we just run the n-th job, where n is passed as an argument.
    if len(sys.argv) == 1:
        num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(
            delayed(process_repo)(url, commit, ignorelist)
            for url, commit, ignorelist in TEST_REPOS
        )
    else:
        index = int(sys.argv[1])
        process_repo(
            TEST_REPOS[index][0], TEST_REPOS[index][1], TEST_REPOS[index][2]
        )


if __name__ == "__main__":
    main()