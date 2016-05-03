import csv
import requests

csv_name = 'Data_Science.csv'
output_name = 'Data_Science_commits.csv'
# access_token = '71315f773eb1fb42260dc84712bee0ac7c844e73'
# access_token = '8c380dbb7d70b25bb1f68cdbe1c5e60608f0067d'
access_token = 'e7e67562b71e8688df01065a9cb1ed01df41fae9'
num_trash = 0


def get_commit_dates(url, page):
    global num_trash
    final_url = url + "/commits" + "?&page=" + str(page)
    r = requests.get(final_url, {'access_token': access_token})
    if r.status_code == 200:
        dates_arr = []
        for commit in r.json():
            dates_arr.append(commit["commit"]["author"]["date"])
        return dates_arr
    else:
        num_trash += 1
        return []


def get_all_commit_dates(url):
    page = 1
    commit_dates_arr = []
    total_commits = 0
    while True:
        r = get_commit_dates(url, page)
        if not r:
            break
        commit_dates_arr += r
        total_commits += len(r)
        page += 1

    print "We get " + str(total_commits) + " commits."
    return commit_dates_arr


def main():
    with open(csv_name) as in_file:
        with open(output_name, "w") as out_file:
            csv_writer = csv.writer(out_file)
            csv_reader = csv.reader(in_file)
            next(csv_reader)
            first_line = True
            for line in csv_reader:
                if first_line:
                    first_line = False
                    csv_writer.writerow(['id', 'commit_time'])
                else:
                    dates = get_all_commit_dates(line[7])
                    for date in dates:
                        csv_writer.writerow([line[0], date])

            print str(num_trash) + " trash repos."

if __name__ == '__main__':
    main()
