from __future__ import division
import csv
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
    ret = {}
    maxVal = float(max(stars.values()))
    minVal = float(min(stars.values()))
    for k in stars:
        ret[k] = ((float(stars[k])-minVal)/(maxVal-minVal))
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

def output_avg_stars_csv(input):
    output = {}
    dates = []
    avg_stars = []

    for k in input:
        vals = input[k]
        output[k] = (numpy.mean(vals))

    with open('../../src/main/resources/static/avg_stars.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['time', 'avg_stars']);
        for k in sorted(output, key=lambda x: datetime.datetime.strptime(x, '%Y/%m')):
            w.writerow([str(k), output[k]])
            date_split = k.split('/')
            avg_stars.append(output[k])
            dates.append(datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=1))

    # best fit line to determine the star potential rating
    numdate = mdates.date2num(dates)
    z = numpy.polyfit(numdate, avg_stars, 1)
    p = numpy.poly1d(z)
    print "best fit line for star potential = {0}x + {1}".format(*z)

    # return the value of best fit line for recommendation purpose
    return z[0], max(output.values())

def output_dates_csv(input):
    output = {}
    for k in input:
        num_project = len(input[k])
        output[k] = num_project

    output = normalize_stars(output)

    dates = []
    num_project = []
    with open('../../src/main/resources/static/day_created.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['time', 'quantity']);
        for k in sorted(output, key=lambda x: datetime.datetime.strptime(x, '%Y/%m')):
            w.writerow([str(k), output[k]])
            date_split = k.split('/')
            num_project.append(output[k])
            dates.append(datetime.datetime(year=int(date_split[0]), month=int(date_split[1]), day=1))

    # generate chart of popularity
    numdate = mdates.date2num(dates)
    z = numpy.polyfit(numdate, num_project, 1)
    p = numpy.poly1d(z)
    print "best fit line for project popularity = {0}x + {1}".format(*z)

    # return the value of best fit line for recommendation purpose
    return z[0]

def main():
    # Load training text and training labels
    train_data = load_file('Phase1Output/phase1_output.csv')
    training_labels = train_data[0]
    training_features = train_data[1]

    # group projects based on the month created, output to csv and visualize the plot
    coef_trend = output_dates_csv(created_day_bins)
    if coef_trend >= 0.003:
        trend = 'rising star'
    elif coef_trend <= -0.001:
        trend = 'once-famous'
    else:
        trend = 'the classic'

    # calculate average stars over time and output the files as csv
    [coef_stars, max_stars] = output_avg_stars_csv(created_day_bins)
    if coef_stars > -0.001:
        sign = '+'
    else:
        sign = '-'

    if max_stars < 10:
        star = 'C'
    elif max_stars < 50:
        star = 'B'
    else:
        star = 'A'
    
    with open('../../src/main/resources/static/rating.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['type', 'rating'])
        w.writerow(['popularity', trend])
        w.writerow(['star magnet', ''.join([star,sign])])

if __name__ == '__main__':
    main()