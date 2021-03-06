from __future__ import division
import csv
import argparse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

import numpy
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression

# global variables
created_days = []			# days since date created
created_day_bins = {}       # dict of (K,V) = (bin index, [stars])
all_lang = {}

def load_file(file_path):
    stars = []
    features = []
    with open(file_path, 'r') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            star = int(row[4])
            created_day = find_days_elapsed(format_time(row[8]))
            created_mo = get_month(format_time(row[8]))
            if created_mo in created_day_bins:
                created_day_bins[created_mo].append(star)
            else:
                created_day_bins[created_mo] = [star]
            created_days.append(created_day)
            entry = [created_day]
            features.append(entry)
            stars.append(star)
    return [stars, features]

def get_month(date):
    return ''.join([str(date.year), "/", str(date.month)])

def normalize_stars(stars):
    n = len(stars)
    ret = []
    maxVal = max(stars)
    minVal = min(stars)
    for i in range(0,n):
        ret.append((stars[i]-minVal)/(maxVal-minVal)*100)
    return ret

def format_time(commit):
    c_time = commit.split('T')[0].split('-')
    c_day = int(c_time[2])
    c_mo = int(c_time[1])
    c_yr = int(c_time[0])
    d = datetime.date(c_yr, c_mo, c_day)
    return d

def find_days_elapsed(d0):
    d1 = datetime.date.today()
    delta = d1 - d0
    return -delta.days

def output_avg_stars_csv(input,project):
    output = {}
    dates = []
    avg_stars = []

    for k in input:
        vals = input[k]
        output[k] = (numpy.mean(vals))

    with open(project + '_avg_stars.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['time', 'avg_stars']);
        for k in sorted(output, key=lambda x: datetime.datetime.strptime(x, '%Y/%m')):
            w.writerow([str(k), output[k]])
            date_split = k.split('/')
            avg_stars.append(output[k])
            dates.append(datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=1))

    # generate chart of average stars
    plt.bar(dates, avg_stars, width=15, color="blue")
    plt.ylim(ymin=0)
    plt.ylabel('Average stars')
    plt.xlabel('Time created')
    plt.title('Average stars since day created, for project ' + project)

    # best fit line to determine the star potential rating
    numdate = mdates.date2num(dates)
    z = numpy.polyfit(numdate, avg_stars, 1)
    p = numpy.poly1d(z)
    trendline = plt.plot(numdate, p(numdate))
    plt.setp(trendline, color='r', linewidth=2.0)
    plt.ylim(ymin=0)
    plt.show()
    print "best fit line for star potential = {0}x + {1}".format(*z)

    # return the value of best fit line for recommendation purpose
    print z[0]

def output_dates_csv(input,project):
    output = {}
    for k in input:
        num_project = len(input[k])
        output[k] = num_project

    dates = []
    num_project = []
    with open(project + '_day_created.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['time', 'quantity']);
        for k in sorted(output, key=lambda x: datetime.datetime.strptime(x, '%Y/%m')):
            w.writerow([str(k), output[k]])
            date_split = k.split('/')
            num_project.append(output[k])
            dates.append(datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=1))

    # generate chart of popularity
    plt.bar(dates, num_project, width=15, color="blue")
    plt.xlabel('Time created')
    plt.ylabel('Number of Project')
    plt.title('Popularity Trend for ' + project)
    numdate = mdates.date2num(dates)
    z = numpy.polyfit(numdate, num_project, 1)
    p = numpy.poly1d(z)
    trendline = plt.plot(numdate, p(numdate))
    plt.setp(trendline, color='r', linewidth=2.0)
    plt.ylim(ymin=0)
    plt.show()
    print "best fit line for project popularity = {0}x + {1}".format(*z)

    # return the value of best fit line for recommendation purpose
    print z[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-training', required=True, help='Path to training data')
    parser.add_argument('-test', help='Path to test data')
    parser.add_argument('-c', '--classifier', default='log', help='nb | log | svm')
    parser.add_argument('-top', type=int, help='Number of top features to show')
    parser.add_argument('-p', type=bool, default='', help='If true, prints out information')
    opts = parser.parse_args()
    # Note: anytime the print flag is set to '', you should not print anything out!

    # Load training text and training labels
    train_data = load_file(opts.training)
    training_labels = train_data[0]
    training_features = train_data[1]

    # group projects based on the month created, output to csv and visualize the plot
    output_dates_csv(created_day_bins, opts.training)

    # calculate average stars over time and output the files as csv
    output_avg_stars_csv(created_day_bins, opts.training)

if __name__ == '__main__':
    main()