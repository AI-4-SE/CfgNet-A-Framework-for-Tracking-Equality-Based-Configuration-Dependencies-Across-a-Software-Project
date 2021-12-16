import os
import requests
import csv
import pandas as pd
import glob
import git

query = """
{{
   search(query: "{queryString}", type: REPOSITORY, first: {maxItems}) {{
     repositoryCount
     edges {{
       node {{
         ... on Repository {{
           name
           url
           stargazers {{ totalCount }}
           description
           primaryLanguage {{ name }}
         }}
       }}
    }}
  }}
}}
"""
variables = {
   'queryString' : 'is:public stars:>1000 sort:stars',
   'maxItems' : '100'
}

def parse_gql_results(result):

    print(len(result["data"]["search"]["edges"]))

    res = []
    for repo in result["data"]["search"]["edges"]:
        repo_data = repo['node']
        res.append({
            'name': repo_data['name'],
            'stargazers_count': repo_data['stargazers']['totalCount'],
            'language': repo_data['primaryLanguage']['name'] if repo_data['primaryLanguage'] is not None else None,
            'html_url': repo_data['url'],
            'description': repo_data['description'],
            })
    return res


def run_query(query):
    headers = {"Authorization": "Bearer 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"}

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def get_repos_by_stars(): 
  # Github GraphQL API v4 https://docs.github.com/en/graphql 
  repo_stars = run_query(query.format(**variables))
  repo_stars_parsed = parse_gql_results(repo_stars)

  first_repo = repo_stars_parsed[0]
  keys = first_repo.keys()

  with open('././data/commit_analysis/repos_stars.csv', 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      for repo in repo_stars_parsed:
          dict_writer.writerow(repo)


def get_tracked_files(repo):
    tree = repo.tree()
    files = []
    iter_tree([tree], files)
    return files

def iter_tree(trees, files):
    for tree in trees:
        for blob in tree.blobs:
            files.append(blob.path)
        if tree.trees:
            iter_tree(tree.trees, files)

def clone_repos(urls, target_dir):
    for url in urls:
        git.Git(target_dir).clone(url + ".git")


def are_technologies_supported(repos):
    technologies = ["pom.xml", "Dockerfile", "docker-compose", ".travis.yml", ".ini", ".properties", ".yaml", ".yml", ".toml", ".xml", ".json"]
    result = []

    for repo in repos:
        repo_name = repo.split("/")[-1]
        supported = set()
        for _, _, files in os.walk(repo):
            for file in files:
                for x in technologies:
                    if x in file:
                        supported.add(x)
        if len(supported) >= 2:
            result.append({"repo": repo_name, "technologies": " ".join(supported) })       
    return result


def check_for_technologies():
    target_dir = "/home/simisimon/GitHub/AI-4-SE/CfgNet-A-Framework-for-Tracking-Configuration-Dependencies-Across-a-Software-Project/data/repos"
    df = pd.read_csv("././data/commit_analysis/repos_stars.csv")
    urls = df["html_url"]
    
    #clone_repos(urls, target_dir)

    all_repos = glob.glob(target_dir + "/*")

    relevant_repos = are_technologies_supported(all_repos)
    keys = relevant_repos[0].keys()

    with open('././data/commit_analysis/repos_technologies_relevant.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for repo in relevant_repos:
            dict_writer.writerow(repo)


def filter_repos():

    df_relevant_repos = pd.read_csv("././data/commit_analysis/repos_technologies_relevant.csv")

    relevant_repos = df_relevant_repos["repo"].values.tolist()

    with open("././data/commit_analysis/repos_stars.csv", "r") as infile:
        with open("././data/commit_analysis/final_repos.csv", "w") as outfile:
            outfile.write("name,stargazers_count,language,html_url,description\n")
            for line in infile.readlines():
                if line.split(",")[0] in relevant_repos:
                    outfile.write(line)


if __name__ == "__main__":
  get_repos_by_stars()

  check_for_technologies()

  filter_repos()


