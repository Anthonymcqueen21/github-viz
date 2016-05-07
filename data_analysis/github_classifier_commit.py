from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt
import datetime
from datetime import date

import numpy
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import cross_validation
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from sklearn.preprocessing import PolynomialFeatures

# global variables
created_days = []			# days since date created
median_commit_days = []     # median commit day of a given project
num_bins = 27               # number of bins if we group the projects per month
created_day_bins = {}       # dict of (K,V) = (bin index, [stars])
median_commit_bins = {}     # dict of (K,V) = (bin index, [stars])
all_lang = {}

def load_file(file_path):
    stars = []
    features = []
    commit_list = get_commit_times(file_path + '_commits.csv')
    with open(file_path + '_with_scraping.csv', 'r') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            if int(row[0]) not in commit_list: # disregard inactive repositories with no commit history
                continue

            star = int(row[4])
            created_day = find_days_elapsed(format_commit_time(row[8]))
            created_mo = get_commit_month(format_commit_time(row[8]))
            if created_mo in created_day_bins:
                created_day_bins[created_mo].append(star)
            else:
                created_day_bins[created_mo] = [star]

            all_commit_times = commit_list[int(row[0])]
            median_cday = find_days_elapsed(get_median_time(all_commit_times))
            median_cmo = get_commit_month(get_median_time(all_commit_times))
            if median_cmo in median_commit_bins:
                median_commit_bins[median_cmo].append(star)
            else:
                median_commit_bins[median_cmo] = [star]

            created_days.append(created_day)
            median_commit_days.append(median_cday)

            entry = [created_day, median_cday]
            features.append(entry)
            stars.append(star)
    return [stars, features]

def get_commit_times(file_path):
    commit_list = {}
    with open(file_path, 'r') as f:
        r = csv.reader(f, delimiter=',')
        next(r)
        for row in r:
            c_id = int(row[0])
            c_time = format_commit_time(row[9])
            if c_id in commit_list:
                commit_list[c_id].append(c_time)
            else:
                commit_list[c_id] = [c_time]
    return commit_list

def get_commit_month(date):
    return ''.join([str(date.year), "/", str(date.month)])

def normalize_stars(stars):
    n = len(stars)
    ret = []
    maxVal = max(stars)
    minVal = min(stars)
    for i in range(0,n):
        ret.append((stars[i]-minVal)/(maxVal-minVal)*100)
    return ret

def normalize(X):
    n = len(X)
    numFeatures = len(X[0])
    ret = []
    for i in range(0,n):
        ret.append([])
    for j in range(0,numFeatures):
        norm = []
        for i in range(0,n):
            norm.append(X[i][j])
        minVal = min(norm)
        maxVal = max(norm)
        for i in range(0,n):
            ret[i].append((X[i][j]-minVal)/(maxVal-minVal))
    return ret

def get_median_time(commit_list):
    c_len = float(len(commit_list))
    mid_pt = int(round(c_len/2)-1)
    commit_list.sort()
    return commit_list[mid_pt]

def format_commit_time(commit):
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

def diff_month(d1,d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month

def calculate_avg_stars(input):
    time = []
    avg = []
    for k in input:
        vals = input[k]
        avg.append(numpy.mean(vals))
        time.append(k)
    return (time,avg)

def output_csv(input,project):
    output = {}
    for k in input:
        num_project = len(input[k])
        output[k] = num_project
    with open(project + '_day_created.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['time', 'quantity']);
        for k in sorted(output, key=lambda x: datetime.datetime.strptime(x, '%Y/%m')):
            w.writerow([str(k), output[k]])
        print "called!"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-training', required=True, help='Path to training data')
    parser.add_argument('-test', help='Path to test data')
    parser.add_argument('-c', '--classifier', default='lin', help='nb | log | svm')
    parser.add_argument('-top', type=int, help='Number of top features to show')
    parser.add_argument('-p', type=bool, default='', help='If true, prints out information')
    opts = parser.parse_args()
    # Note: anytime the print flag is set to '', you should not print anything out!

    # Load training text and training labels
    train_data = load_file(opts.training)
    training_labels = train_data[0]
    training_features = normalize(train_data[1])
    print "dimension of training features = " + str(len(training_features)) + "," + str(len(training_features[0]))
    poly = PolynomialFeatures(degree=7)
    training_features = poly.fit_transform(training_features)

    # Initialize the corresponding type of the classifier and train it (using 'fit')
    if opts.classifier == 'nb':
        classifier = BernoulliNB(binarize=None)
    elif opts.classifier == 'log':
        classifier = LogisticRegression()
    elif opts.classifier == 'svm':
        classifier = LinearSVC()
    elif opts.classifier == 'lin':
        classifier = LinearRegression()
    else:
        raise Exception('Unrecognized classifier!')

    # train the classifier
    classifier.fit(training_features, training_labels)

    # print training mean accuracy using 'score'
    #print('Coefficients: \n', classifier.coef_)
    #print "training mean accuracy = " + str(classifier.score(training_features, training_labels))

    time_range = numpy.linspace(-800,0, num = 30).tolist()
    plt.subplot(2,1,1)
    plt.hist(created_days, bins=time_range)
    plt.ylabel('Number of projects')
    plt.xlabel('Days from today since project creation time')

    plt.subplot(2,1,2)
    plt.hist(median_commit_days, bins=time_range)
    plt.ylabel('Number of projects')
    plt.xlabel('Days from today since median commit day')
    plt.show()

    # plot each individual feature and how it relates to the star outcome
    plt.subplot(2,1,1)
    plt.scatter(created_days, training_labels,  color='black')
    plt.ylabel('Stars')
    plt.xlabel('Days elapsed since project creation time')
    plt.ylim(ymin=0,ymax=100)
    plt.xlim(xmin=-800, xmax=0)

    plt.subplot(2,1,2)
    plt.scatter(median_commit_days, training_labels,  color='black')
    plt.ylabel('Stars')
    plt.xlabel('Days elapsed since median commit time')
    plt.ylim(ymin=0,ymax=100)
    plt.xlim(xmin=-800,xmax=0)
    plt.show()

    # calculate average project stars v. time elapsed
    plt.subplot(2,1,1)

    (time_created, avg_stars_created) = calculate_avg_stars(created_day_bins)
    output_csv(created_day_bins, opts.training) # group projects based on the day created and output on the csv
    sorted_mo = sorted(time_created)
    print sorted_mo
    print avg_stars_created
    print sorted_mo[0], sorted_mo[len(sorted_mo)-1]
    plt.scatter(time_created, avg_stars_created, color='black')
    plt.ylim(ymin=0,ymax=45)
    plt.ylabel('Average stars')
    plt.xlabel('Months elapsed since date created')

    plt.subplot(2,1,2)
    (time_commit, avg_stars_commit) = calculate_avg_stars(median_commit_bins)
    plt.scatter(time_commit, avg_stars_commit, color='black')
    plt.ylim(ymin=0,ymax=45)
    plt.ylabel('Average stars')
    plt.xlabel('Months elapsed since median commit time')
    plt.show()

if __name__ == '__main__':
    main()
