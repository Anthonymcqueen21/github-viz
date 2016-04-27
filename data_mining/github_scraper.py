# We need Python 3 to run this
# This should take about 10 minutes to run it
import urllib.request
from re import findall
import csv


def scraping_page(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    html_str = html.decode()

    regex = findall(r'<a\s*class="[^ ]*" href="[^ ]*watcher[s]*">[\s]*([0-9]+)[\s]*</a>', html_str)
    if len(regex) > 0:
        num_watchers = int(regex[0])
    else:
        num_watchers = -1

    regex = findall(r'<span\s*itemprop="name">Pull requests</span>\s*<span class="counter">([0-9]+)</span>', html_str)
    if len(regex) > 0:
        num_pull_requests = int(regex[0])
    else:
        num_pull_requests = -1

    regex = findall(r'<li class="commits">\s*<a.*>\s*<svg.*\s*<span.*\s*([0-9]+)', html_str)
    if len(regex) > 0:
        num_commits = int(regex[0])
    else:
        num_commits = -1

    regex = findall(r'<a\s*href="[A-za-z]*.*\s*<svg\s.*>\s*<[a-z]*.+>\s*([0-9]+)', html_str)
    if len(regex) > 0:
        num_contributors = int(regex[0])
    else:
        num_contributors = -1

    return [num_watchers, num_pull_requests, num_contributors, num_commits]


def main():
    with open("repo.csv") as in_file:
        with open("repo_with_scraping.csv", "w") as out_file:
            csv_writer = csv.writer(out_file)
            csv_reader = csv.reader(in_file)
            first_line = True
            for line in csv_reader:
                if first_line:
                    first_line = False
                    csv_writer.writerow(line + ['watchers', 'pull_requests', 'contributors', 'commits'])
                else:
                    scrape_result = scraping_page(line[2])
                    csv_writer.writerow(line + scrape_result)



if __name__ == '__main__':
    main()
