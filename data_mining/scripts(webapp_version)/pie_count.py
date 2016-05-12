""" Counting # languages in a year for each keyword."""
"""pie chart -- different languages over time (when you hover on a certain language, have the breakdown of how many stars the projects using that language receives."""

import operator,sys
import csv
from datetime import datetime


def main():
	
	year_language = {} # dict mapping the year and a dict of language :: star counts for that year 
	languages = set()
	with open('Phase1Output/phase1_output.csv', 'rb') as data: # initialize year dict 
    		reader =  csv.reader(data)
    		next(reader);
    		next(reader);
		for line in reader:
			year = line[8][:4]
			if year not in year_language.keys(): 
				year_language[year] = {} 
			
		
			language = line[6]
			if language == "":
				language = "Not Reported"
			languages.add(language)
			stargazers = int(line[4])

			if language not in year_language[year].keys():
				year_language[year][language] = 0

			year_language[year][language]  += stargazers 
	
	# sorted the dict
	top_10_dict = {}
	for year in year_language.keys(): 
		temp = year_language[year]
		sorted_temp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
		if len(sorted_temp) < 10: 
			top_10_dict[year] = sorted_temp 
		else: 
			top_10_dict[year] = sorted_temp[:10] 

	for year in top_10_dict.keys(): 
		file_name = "year_" + year + ".csv" 
		csv_writer = csv.writer(open('../../src/main/resources/static/' + file_name, 'wb'))
		csv_writer.writerow (["language", "stars"])
		for item in top_10_dict[year]: 
			csv_writer.writerow([item[0], item[1]])
			#csv_writer.writerow ([lang, year_language[year][lang]])
	
	# count total stars over the entire range of years : 
	language_count_total = {} 
	languages_list = list(languages)
	for item in languages_list: 
		language_count_total[item] = 0 

	for year in year_language.keys(): 
		for lang in year_language[year].keys(): 
			language_count_total[lang] += year_language[year][lang]
	sorted_language = sorted(language_count_total.items(), key=operator.itemgetter(1), reverse=True)
	if len(sorted_language) < 10: 
		total = sorted_language
	else: 
		total = sorted_language[:10] 


	csv_writer = csv.writer(open('../../src/main/resources/static/' + 'total.csv', 'wb'))
	csv_writer.writerow (["language", "stars"])
	for item in total: 
		csv_writer.writerow([item[0], item[1]])
	

	
	# file that contains an array of csv file ['total.csv', 'year_2009', 'year_2010']

	csv_writer1 = csv.writer(open('../../src/main/resources/static/' + 'names.csv', 'wb'))
	csv_writer1.writerow(['total.csv', 'total']) # because there is always a total.csv 
	for year in top_10_dict.keys():
		csv_name = "year_" + year + ".csv"
		print csv_name + " " + year
		csv_writer1.writerow([csv_name, year])
	
if __name__ == '__main__':
	main()

