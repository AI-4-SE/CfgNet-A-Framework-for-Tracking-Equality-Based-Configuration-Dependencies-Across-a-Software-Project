"""Analysis for our paper on CfgNet."""

import multiprocessing
import os
import os.path
import subprocess
import sys
import time
from pathlib import Path

from git import Repo
from joblib import Parallel, delayed

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
    "https://github.com/sveltejs/svelte",
    "https://github.com/shadowsocks/shadowsocks-windows",
    "https://github.com/keras-team/keras",
    "https://github.com/httpie/httpie",
    "https://github.com/redis/redis",
    "https://github.com/protocolbuffers/protobuf",
    "https://github.com/josephmisiti/awesome-machine-learning",
    "https://github.com/fatedier/frp",
    "https://github.com/tailwindlabs/tailwindcss",
    "https://github.com/chrislgarry/Apollo-11",
    "https://github.com/30-seconds/30-seconds-of-code",
    "https://github.com/996icu/996.ICU",
    "https://github.com/doocs/advanced-java",
    "https://github.com/angular/angular",
    "https://github.com/angular/angular.js",
    "https://github.com/animate-css/animate.css",
    "https://github.com/ant-design/ant-design",
    "https://github.com/xingshaocheng/architect-awesome",
    "https://github.com/atom/atom",
    "https://github.com/sindresorhus/awesome",
    "https://github.com/avelino/awesome-go",
    "https://github.com/vinta/awesome-python",
    "https://github.com/awesome-selfhosted/awesome-selfhosted",
    "https://github.com/vuejs/awesome-vue",
    "https://github.com/axios/axios",
    "https://github.com/bitcoin/bitcoin",
    "https://github.com/twbs/bootstrap",
    "https://github.com/danistefanovic/build-your-own-x",
    "https://github.com/chartjs/Chart.js",
    "https://github.com/ryanmcdermott/clean-code-javascript",
    "https://github.com/jwasham/coding-interview-university",
    "https://github.com/ossu/computer-science",
    "https://github.com/facebook/create-react-app",
    "https://github.com/CyC2018/CS-Notes",
    "https://github.com/d3/d3",
    "https://github.com/denoland/deno",
    "https://github.com/kamranahmedse/developer-roadmap",
    "https://github.com/django/django",
    "https://github.com/electron/electron",
    "https://github.com/expressjs/express",
    "https://github.com/tonsky/FiraCode",
    "https://github.com/pallets/flask",
    "https://github.com/EbookFoundation/free-programming-books",
    "https://github.com/justjavac/free-programming-books-zh_CN",
    "https://github.com/freeCodeCamp/freeCodeCamp",
    "https://github.com/thedaviddias/Front-End-Checklist",
    "https://github.com/labuladong/fucking-algorithm",
    "https://github.com/gin-gonic/gin",
    "https://github.com/github/gitignore",
    "https://github.com/golang/go",
    "https://github.com/gohugoio/hugo",
    "https://github.com/kdn251/interviews",
    "https://github.com/iluwatar/java-design-patterns",
    "https://github.com/Snailclimb/JavaGuide",
    "https://github.com/airbnb/javascript",
    "https://github.com/trekhleb/javascript-algorithms",
    "https://github.com/jquery/jquery",
    "https://github.com/typicode/json-server",
    "https://github.com/laravel/laravel",
    "https://github.com/MisterBooo/LeetCodeAnimation",
    "https://github.com/macrozheng/mall",
    "https://github.com/adam-p/markdown-here",
    "https://github.com/mui-org/material-ui",
    "https://github.com/moby/moby",
    "https://github.com/tensorflow/models", 
    "https://github.com/netdata/netdata", 
    "https://github.com/goldbergyoni/nodebestpractices",
    "https://github.com/nvm-sh/nvm",
    "https://github.com/ohmyzsh/ohmyzsh",
    "https://github.com/opencv/opencv",
    "https://github.com/microsoft/PowerToys",
    "https://github.com/practical-tutorials/project-based-learning",
    "https://github.com/public-apis/public-apis",
    "https://github.com/puppeteer/puppeteer",
    "https://github.com/TheAlgorithms/Python",
    "https://github.com/jackfrued/Python-100-Days",
    "https://github.com/facebook/react",
    "https://github.com/facebook/react-native",
    "https://github.com/gothinkster/realworld",
    "https://github.com/reduxjs/redux",
    "https://github.com/hakimel/reveal.js",
    "https://github.com/Genymobile/scrcpy",
    "https://github.com/socketio/socket.io",
    "https://github.com/storybookjs/storybook",
    "https://github.com/donnemartin/system-design-primer",
    "https://github.com/yangshun/tech-interview-handbook",
    "https://github.com/tensorflow/tensorflow",
    "https://github.com/microsoft/terminal",
    "https://github.com/jlevy/the-art-of-command-line",
    "https://github.com/trimstray/the-book-of-secret-knowledge",
    "https://github.com/nvbn/thefuck",
    "https://github.com/mrdoob/three.js",
    "https://github.com/huggingface/transformers",
    "https://github.com/microsoft/TypeScript",
    "https://github.com/vuejs/vue",
    "https://github.com/PanJiaChen/vue-element-admin",
    "https://github.com/webpack/webpack",
    "https://github.com/getify/You-Dont-Know-JS",
    "https://github.com/ytdl-org/youtube-dl",
    "https://github.com/FortAwesome/Font-Awesome",
    "https://github.com/flutter/flutter",
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

    # linearize commit history
    # see https://stackoverflow.com/a/17994534
    subprocess.run(
        "git filter-branch --parent-filter 'cut -f 2,3 -d " "'", shell=True,
        cwd=repo_folder, executable="/bin/bash", env=dict(os.environ, FILTER_BRANCH_SQUELCH_WARNING="1")
    )

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
    # create evaluation folder
    if os.path.exists(EVALUATION_FOLDER):
         subprocess.run(["rm", "-rf", EVALUATION_FOLDER])
    subprocess.run(["mkdir", "-p", EVALUATION_FOLDER + "/results"])

    index = int(sys.argv[1])
    process_repo(TEST_REPOS[index])

if __name__ == "__main__":
    main()
