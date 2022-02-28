import requests
import csv

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
    headers = {"Authorization": "Bearer **Add Token Here**"}

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


if __name__ == "__main__":
  get_repos_by_stars()



