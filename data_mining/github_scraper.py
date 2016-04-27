# We need Python 3 to run this
import urllib.request
from re import findall


def scraping_page(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    html_str = html.decode()
    num_watchers = int(\
        findall(r'<a\sclass="[a-zA-z]+.*" href="/[a-zA-z-]+./[a-aA-z]*.watchers">[\s]*([0-9]+)[\s]*</a>', html_str)[0])
    num_pull_requests = int(\
        findall(r'<span\sitemprop="name">Pull requests</span>\s*<span class="counter">([0-9]+)</span>', html_str)[0])

    num_commits = int(\
        findall(r'<a\sdata-pjax href="[A-za-z]*.*\s*<svg\s.*>\s*<[a-z]*.+>\s*([0-9]+)\s*</span>\s*commits\s*</a>', html_str)[0])

    num_contributors = int(\
        findall(r'<a href="[A-za-z]*.*\s*<svg\s.*>\s*<[a-z]*.+>\s*([0-9]+)\s*</span>\s*contributors\s*</a>', html_str)[0])
    print(num_watchers)
    print(num_pull_requests)
    print(num_commits)
    print(num_contributors)


def main():
    scraping_page("https://github.com/A-limon/pacman")


if __name__ == '__main__':
    main()
