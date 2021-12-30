"""Analysis for our paper on CfgNet."""

import multiprocessing
import os
import os.path
import subprocess
import sys
import time

from git import Repo
from joblib import Parallel, delayed
from pathlib import Path


# The folder where we store our results.
EVALUATION_FOLDER = "out"

# Every item is a tuple which consists of:
#
#   * An URL to the repository that should be analyzed.
#   * A list of files that should be ignored during the analysis. The files we
#     added to the ignore list are from test runs and are large files that are
#     not configuration but other data.
#
# If you change the number of repositories (e.g. the length of this list), you
# have to adjust the array range in `array.sbatch`.

TEST_REPOS = [
    "https://github.com/kamranahmedse/developer-roadmap",
    "https://github.com/CyC2018/CS-Notes",
    "https://github.com/ohmyzsh/ohmyzsh",
    "https://github.com/github/gitignore",
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


def process_repo(url):
    """
    Analyze a repository with CfgNet.
    :param url: URL to the repository
    :param commit: Hash of the lastest commit that should be analyzed
    :param ignorelist: List of file paths to ignore in the analysis
    """
    repo_name = get_repo_name_from_url(url)
    repo_folder = EVALUATION_FOLDER + "/" + repo_name
    results_folder = EVALUATION_FOLDER + "/results/" + repo_name
    abs_repo_path = os.path.abspath(repo_folder)

    # Cloning repository
    Repo.clone_from(url, repo_folder)

    # Create ignore file
    # create_ignore_file(ignorelist, repo_folder)
    subprocess.run(
        f"cfgnet analyze  {abs_repo_path}", shell=True, cwd=repo_folder, executable="/bin/bash"
    )

    # Clean up log file
    # clean_up_log(repo_name, repo_folder)

    # Copy results into result folder
    subprocess.run(["cp", "-r", repo_folder + "/.cfgnet", results_folder])

    # Remove repo folder
    remove_repo_folder(repo_folder)


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


def remove_repo_folder(repo_name):
    """Remove the cloned repository."""
    if os.path.exists(repo_name):
        subprocess.run(["rm", "-rf", repo_name ])


def main():
    """Run the analysis."""

    #root_dir = Path(__file__).parent.parent.parent
    #repo_path = os.path.join(root_dir, "data/commit_analysis/final_repos.csv")

    #repos = []
    #with open(repo_path, "r") as file:
    #    for line in file:
    #        repos.append(line.split(",")[3])
            
    # create evaluation folder
    if os.path.exists(EVALUATION_FOLDER):
         subprocess.run(["rm", "-rf", EVALUATION_FOLDER])
    subprocess.run(["mkdir", "-p", EVALUATION_FOLDER + "/results"])
    
    start = time.time()

    # analyze all repositories in parallel
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(
        delayed(process_repo)(url)
        for url in TEST_REPOS
    )

    completion_time = round((time.time() - start), 2)

    print(f"Done in {completion_time}s")

if __name__ == "__main__":
    main()
