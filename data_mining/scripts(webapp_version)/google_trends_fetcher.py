from collections import defaultdict
import sys
from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import csv
import os

google_username = "githubviz0@gmail.com"
google_password = "githubvizcs1951"

def main():

    name = sys.argv[1]
    if len(sys.argv) >= 2:
        for argument in sys.argv[2:]:
            name += " " + argument

    newpath = "GoogleTrendsData/" + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    path = "GoogleTrendsData/"
    path += name + "/"
    csv_name = name + "_trend"
    cleaned_csv_name = name + "_trend_cleaned.csv"

    # connect to Google
    connector = pyGTrends(google_username, google_password)

    # make request
    connector.request_report(name)

    # wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))

    # download file
    connector.save_csv(path, csv_name)

    with open("GoogleTrendsData/" + name + "/" + csv_name + ".csv") as in_file:
        csv_reader = csv.reader(in_file)

        for i in range(5):
            next(csv_reader)
        dates_mapping = defaultdict(int)
        for line in csv_reader:
            if not line:
                break
            dateString = line[0]
            dates = dateString.split(' - ')
            start_dates = dates[0].split('-')
            start_year = start_dates[0]
            start_month = start_dates[1]
            dates_mapping[start_year + "/" + start_month] += int(line[1])

        with open("GoogleTrendsData/" + name + "/" + cleaned_csv_name, "w") as out_file:
            csv_writer = csv.writer(out_file)
            for item in sorted(dates_mapping.items()):
                csv_writer.writerow([item[0], item[1]])

if __name__ == '__main__':
    main()
