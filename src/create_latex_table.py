import pandas as pd
import json


def get_n_repos(n):
    df = pd.read_csv("two_technologies.csv")
    df = df.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1)
    df_50 = df[:n]
    df_50.to_csv("final_repos.csv") 


def get_languages():
    with open("repos_page1.json", "r", encoding="utf-8") as src:
        data_page_one = json.load(src)
    
    with open("repos_page2.json", "r", encoding="utf-8") as src:
        data_page_two = json.load(src)

    with open("repos_page3.json", "r", encoding="utf-8") as src:
        data_page_three = json.load(src)

    repos_page_one = data_page_one["items"]
    repos_page_two = data_page_two["items"]
    repos_page_three = data_page_three["items"]

    df = pd.read_csv("final_repos.csv")

    languages = []

    for _, item in df.iterrows():
        name = item["name"]

        for repo in repos_page_one:
            if repo["name"] == name:
                if not repo["language"]:
                    languages.append("Unknown")
                else:
                    languages.append(repo["language"])

        for repo in repos_page_two:
            if repo["name"] == name:
                if not repo["language"]:
                    languages.append("Unknown")
                else:
                    languages.append(repo["language"])

        for repo in repos_page_three:
            if repo["name"] == name:
                if not repo["language"]:
                    languages.append("Unknown")
                else:
                    languages.append(repo["language"])

    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    
    df["language"] = languages

    df.to_csv("final_repos.csv")


def main():
    df = pd.read_csv("final_repos.csv")

    #df = df.drop(df.columns[df.columns.str.contains('unnamed',case = False)], axis = 1, inplace = True)
    #df = df.drop(df.columns["url", "technology_counter"], axis=1)

    # print(df.to_latex(columns=["name", "stars", "technologies_seen", "language"], index=False))
    
    urls = []

    for _, item in df.iterrows():
        urls.append(item["url"])

    print(urls)

if __name__ == "__main__":
    main()