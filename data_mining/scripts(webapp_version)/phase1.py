import requests
import csv
import sys

# Put your access token here
access_token = '71315f773eb1fb42260dc84712bee0ac7c844e73'   # put your github authentication token here
per_page = 100  # repositories that we can fetch per request
limit = 1000  # maximum number of repositories

output_name = "phase1_output.csv"
fields = ["id", "name", "html_url", "forks", "stargazers_count", "size", "language", "url", "created_at"]


class GithubAPI(object):
    prefix_url = 'https://api.github.com'

    def __init__(self):
        self.access_token = access_token
        self.per_page = per_page
        self.limit = limit

    def get_request(self, path, params={}):
        params['access_token'] = self.access_token
        url = self.prefix_url + path
        r = requests.get(url, params=params)
        return r.json()

    def get_repositories(self, keywords, pagenum):
        path = '/search/repositories?q=' + keywords + '&page=' + str(pagenum) + '&per_page=' + str(self.per_page)
        r = self.get_request(path, {})
        return r['items']

    def get_all_repositories(self, keywords):
        page = 1
        repositories = []
        total_items = 0
        while total_items < self.limit:
            r = self.get_repositories(keywords, page)
            if not r:
                break
            repositories += r
            total_items += len(r)
            page += 1
        print "We get " + str(total_items) + " items."
        return repositories

    def get_num_of_repositories(self, keywords):
        path = '/search/repositories?q=' + keywords
        r = self.get_request(path, {})
        return r['total_count']



def main():
    repo_name = sys.argv[1]
    github_api = GithubAPI()

    with open(output_name, "wb") as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow([github_api.get_num_of_repositories(repo_name)])
        writer.writerow(fields)
        for repo in github_api.get_all_repositories(repo_name):
            res = [repo[i] for i in fields]
            writer.writerow(res)


if __name__ == '__main__':
    main()
