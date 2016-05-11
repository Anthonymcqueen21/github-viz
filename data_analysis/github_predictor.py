from __future__ import division
import csv
import argparse
import datetime

import numpy
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

# all features in our linear regression model
all_fork = []			# number of forks
all_pull = []			# number of pull requests
all_day = []			# days since date created
all_languages = {}
all_median_day = []

def load_file(file_path):
    features = []
    languages = []
    global top_languages
    with open(file_path + '_with_scraping.csv', 'r') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            language = row[6]
            if language in all_languages:
                all_languages[language] += 1
            else:
                if language != '':
                    all_languages[language] = 1
    top_languages = find_top_languages(all_languages,2)

    with open(file_path + '_with_scraping.csv', 'r') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            language = row[6]
            if language not in top_languages:
                continue

            fork = int(row[3])
            pull_request = int(row[10])
            language = row[6]
            star = int(row[4])
            created_day = find_days_elapsed(format_time(row[8]))

            all_fork.append(fork)
            all_pull.append(pull_request)

            entry = [fork, pull_request, created_day, star]
            features.append(entry)
            languages.append(language)
    categories = convert_to_numeric(languages, top_languages)
    return [categories, features]

def convert_to_numeric(languages,top_languages):
    output = []
    for l in languages:
        output.append(top_languages.index(l)+1)
    return output

def format_time(time):
    c_time = time.split('T')[0].split('-')
    c_day = int(c_time[2])
    c_mo = int(c_time[1])
    c_yr = int(c_time[0])
    d = datetime.date(c_yr, c_mo, c_day)
    return d

def find_days_elapsed(d0):
    d1 = datetime.date.today()
    delta = d1 - d0
    return delta.days

def find_top_languages(languages,numTop):
    sorted_lang = sorted(languages, key=languages.get, reverse=True)
    return sorted_lang[0:numTop]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-training', required=True, help='Path to training data')
    parser.add_argument('-test', help='Path to test data')
    parser.add_argument('-c', '--classifier', default='nb', help='nb | log | svm')
    parser.add_argument('-top', type=int, help='Number of top features to show')
    parser.add_argument('-p', type=bool, default='', help='If true, prints out information')
    opts = parser.parse_args()
    # Note: anytime the print flag is set to '', you should not print anything out!

    # Load training text and training labels
    train_data = load_file(opts.training)
    training_labels = train_data[0]
    training_features = train_data[1]

    # Initialize the corresponding type of the classifier and train it (using 'fit')
    classifier = LogisticRegression()
    classifier.fit(training_features, training_labels)

    # predict the language best used for today's purpose
    # format = [fork, pull_request, created_day, star]
    print "we suggest you to use = " + top_languages[classifier.predict([100, 100, 0, 100])-1]
    print "coefficients of each weight = " + str(classifier.coef_)

    # print training mean accuracy using 'score'
    print "training mean accuracy = " + str(classifier.score(training_features, training_labels))

    # Perform 5-fold cross validation (cross_validation.cross_val_score) with scoring='accuracy'
    cross_val = cross_validation.cross_val_score(classifier, training_features, training_labels, cv=5)

    # print the mean score and std deviation
    mean_cv = numpy.mean(cross_val)
    std_cv = numpy.std(cross_val)

    print "5-fold cross validation mean accuracy = " + str(mean_cv)
    print "5-fold cross validation std. deviation accuracy = " + str(std_cv)

if __name__ == '__main__':
    main()
