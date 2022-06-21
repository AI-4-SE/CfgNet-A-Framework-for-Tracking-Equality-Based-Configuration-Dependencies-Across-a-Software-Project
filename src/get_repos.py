import json
import pandas as pd
import git
import os
import glob
import subprocess

pages = ["repos_page1.json", "repos_page2.json", "repos_page3.json"]

github_repos = []

technology_files = [
    "Dockerfile", "docker-compose.yml", "docker-compose.dev.yml", "docker-compose.prod.yml", 
    "pom.xml", "cypress.json", "package.json", "tsconfig.json", "application.properties", 
    "application.yml", ".travis.yml", "pyproject.toml", "application-dev.yml","application-prod.yml",
    "application-dev.properties", "application-prod.properties", "application.dev.yml", 
    "application.prod.yml", "application.dev.properties", "application.prod.properties",
    "docker-compose-prod.yml", "docker-compose-dev.yml"
    ]

target_dir = "/home/simisimon/GitHub/AI-4-SE/github_repos"



def query_repos():
    for page in pages:
        with open(page, "r", encoding="utf-8") as src:
            data = json.load(src)

            repos = data["items"]

            for repo in repos:
                github_repos.append((repo["name"],repo["html_url"], repo["stargazers_count"]))


    
    repo_names = [elem[0] for elem in github_repos]
    repo_urls = [elem[1] for elem in github_repos]
    repo_star_count = [elem[2] for elem in github_repos]

    df = pd.DataFrame()
    df["name"] = repo_names
    df["url"] = repo_urls
    df["stars"] = repo_star_count

    df.to_csv("github_repos.csv")

    print(df.head())


def get_tech_count():
    try:   
        repo_data = []

        df = pd.read_csv("github_repos.csv")
        
        for _, item in df.iterrows():
            technology_counter = 0
            technologies_seen = []

            dir_name = os.path.join(target_dir, item["name"])
            repo = git.Repo.clone_from(item["url"], dir_name )


            for subdir, dirs, files in os.walk(dir_name):
                for filename in files:
                    if filename in technology_files:
                        if filename not in technologies_seen:
                            technology_counter += 1
                            technologies_seen.append(filename)

            repo_data.append((item["name"], item["url"], item["stars"], technology_counter, technologies_seen))

            print("Done with Repo: ",  item["name"], technology_counter, technologies_seen)
        
        tech_counter = [elem[2] for elem in repo_data]
        tech_seen = [elem[3] for elem in repo_data]

        df["technology_counter"] = tech_counter
        df["technologies_seen"] = tech_seen

        df.to_csv("github_repos_tech_count.csv")

        print(df.head())
    except:
        
        repo_names = [elem[0] for elem in repo_data]
        repo_urls = [elem[1] for elem in repo_data]
        repo_star_count = [elem[2] for elem in repo_data]
        tech_counter = [elem[3] for elem in repo_data]
        tech_seen = [elem[4] for elem in repo_data]

        df_new = pd.DataFrame()
        df_new["name"] = repo_names
        df_new["url"] = repo_urls
        df_new["stars"] = repo_star_count
        df_new["technology_counter"] = tech_counter
        df_new["technologies_seen"] = tech_seen

        df_new.to_csv("github_repos_tech_count.csv")

        print(df_new.head())

def main():
    df = pd.read_csv("github_repos_tech_count.csv")

    res_df = df[df['technology_counter'] >= 3]

    res_df.to_csv("three_technologies.csv")


if __name__ == "__main__":
    main()