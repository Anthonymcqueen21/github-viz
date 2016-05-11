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
from sklearn.preprocessing import PolynomialFeatures

# global variables
created_days = []			# days since date created
created_day_bins = {}       # dict of (K,V) = (bin index, [stars])
all_lang = {}

def load_file(file_path):
    stars = []
    features = []
    with open(file_path + '_with_scraping.csv', 'r') as file_reader:
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

def calculate_avg_stars(input):
    dates = []
    avg = []
    for k in input:
        vals = input[k]
        avg.append(numpy.mean(vals))
        date_split = k.split('/')
        #print k,numpy.mean(vals)
        dates.append(date_split[1] + "/" + "1" + "/" + date_split[0]);
        #dates.append(datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=1))
    return (dates,avg)

def output_csv(input,project):
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

    # generate charts of popularity
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
    poly = PolynomialFeatures(degree=7)
    training_features = poly.fit_transform(training_features)

    # Initialize the corresponding type of the classifier and train it (using 'fit')
    classifier = LogisticRegression()

    # train the classifier
    classifier.fit(training_features, training_labels)

    # print training mean accuracy using 'score'
    #print('Coefficients: \n', classifier.coef_)
    #print "training mean accuracy = " + str(classifier.score(training_features, training_labels))

    # group projects based on the month created, output to csv and visualize the plot
    output_csv(created_day_bins, opts.training)

    # calculate average stars over time
    (time_created, avg_stars_created) = calculate_avg_stars(created_day_bins)
    print time_created
    print avg_stars_created
    plt.bar(time_created, avg_stars_created, width=15, color="blue")
    plt.ylim(ymin=0)
    plt.ylabel('Average stars')
    plt.xlabel('Time created')
    plt.title('Average stars since day created, for project ' + opts.training)

    # best fit line to determine the star potential rating
    numdate = mdates.date2num(time_created)
    z = numpy.polyfit(numdate, avg_stars_created, 1)
    p = numpy.poly1d(z)
    trendline = plt.plot(numdate, p(numdate))
    plt.setp(trendline, color='r', linewidth=2.0)
    plt.ylim(ymin=0)
    plt.show()
    print "best fit line for star potential = {0}x + {1}".format(*z)

if __name__ == '__main__':
    main()
