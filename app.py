#!/usr/bin/python
import csv
import re
import string
import random
import numpy as np
from scipy import spatial
from PorterStemmer import PorterStemmer
from flask import Flask, request, jsonify

app = Flask(__name__)
	
@app.route('/vhacks/findjobs/<int:field>', methods=['GET', 'POST'])
def findJobs(field):
	ratings = [[1, 2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 2],  [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 1, 1, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 1], [2, 1, 1, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 2, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [2, 1, 2, 1, 1, 1, 2],  [2, 1, 1, 2, 1, 2, 1]]
	company_titles = ['Albertson', 'American Orange Trucking', 'Atlas Van Lines', 'Baskin-Robbins', 'CalArk International Trucking', 'Campbell Soup Company',  'Chipotle Mexican Grill', 'Coca-Cola Company', 'Comcast', 'Dairy Queen', 'Davis Transport Inc', 'Dunkin Donuts', 'Facebook', 'Five Guys Burgers and Fries', 'Genentech', 'Goodwill Industries', 'Google', 'Hampton Inn', 'Hilton Hotels', 'Home Depot', 'IBM', 'IHOP', 'In-N-Out Burger', 'Kohls', 'Landstar Trucking', 'Lowes', 'Lyft', 'Marriott Hotels', 'McDonalds', 'Mobil Oil', 'New York Times', 'Olive Garden', 'Outback Steakhouse', 'Party City', 'Pepsi-Co', 'PetSmart', 'PGT Trucking', 'Red Lobster', 'Red Robin', 'Residence Inn', 'Shell Oil', 'Sony', 'Starbucks', 'Target Stores', 'TGI Friday', 'Uber', 'United Parcel Service', 'Valvoline Instant Oil Change']
	recommendations = []
	for i in xrange(0, len(ratings)):
		rate = ratings[i]
		if rate[field] == 2:
			recommendations.append(company_titles[i])
	print(recommendations)
	return jsonify(results=recommendations)
	
@app.route('/vhacks/noExperience', methods=['GET', 'POST'])
def noExperience():
	return findJobs(6)
		
def binarize():
	for i in range(len(self.ratings)):
		self.ratings[i] = np.where(np.logical_and(0 < self.ratings[i], self.ratings[i] < 3.0), -1.0, self.ratings[i])
		self.ratings[i] = np.where(self.ratings[i] > 3.0, 1.0, self.ratings[i])
		self.ratings[i] = np.where(self.ratings[i] == 3.0, 0.0, self.ratings[i])

def distance(u, v):
	return 1 - spatial.distance.cosine(u, v)

@app.route('/vhacks/findjobsarray/<string:input>', methods=['GET', 'POST'])
def recommendSpecified(input):
	ratings = [[1, 2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 2],  [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 1, 1, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 1], [2, 1, 1, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 2, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [2, 1, 2, 1, 1, 1, 2],  [2, 1, 1, 2, 1, 2, 1]]
	company_titles = ['Albertson', 'American Orange Trucking', 'Atlas Van Lines', 'Baskin-Robbins', 'CalArk International Trucking', 'Campbell Soup Company',  'Chipotle Mexican Grill', 'Coca-Cola Company', 'Comcast', 'Dairy Queen', 'Davis Transport Inc', 'Dunkin Donuts', 'Facebook', 'Five Guys Burgers and Fries', 'Genentech', 'Goodwill Industries', 'Google', 'Hampton Inn', 'Hilton Hotels', 'Home Depot', 'IBM', 'IHOP', 'In-N-Out Burger', 'Kohls', 'Landstar Trucking', 'Lowes', 'Lyft', 'Marriott Hotels', 'McDonalds', 'Mobil Oil', 'New York Times', 'Olive Garden', 'Outback Steakhouse', 'Party City', 'Pepsi-Co', 'PetSmart', 'PGT Trucking', 'Red Lobster', 'Red Robin', 'Residence Inn', 'Shell Oil', 'Sony', 'Starbucks', 'Target Stores', 'TGI Friday', 'Uber', 'United Parcel Service', 'Valvoline Instant Oil Change']
	#job = request.form.getlist('job_ids', type=int)
	job = []
	temp = input.split(' ')
	for val in temp:
		if val == 'no':
			job.append(1)
		else:
			job.append(2)
	guessed_scores = np.zeros(len(ratings))
	for i in range(len(ratings)):
		#rating = 1 - spatial.distance.cosine(ratings[i], job)
		rating = distance(ratings[i], job)
		guessed_scores[i] = rating
		
	sorted_idx = np.argsort(guessed_scores)[::-1]
	recommendations = [company_titles[sorted_idx[i]] for i in range(3)]
	print(recommendations)
	return jsonify(results=recommendations)
	
@app.route('/vhacks/recommend/<string:input>', methods=['GET', 'POST'])
def recommend(input):
	ratings = [[1, 2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 2],  [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 1, 1, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 1], [2, 1, 1, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 2, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [2, 1, 2, 1, 1, 1, 2],  [2, 1, 1, 2, 1, 2, 1]]
	company_titles = ['Albertson', 'American Orange Trucking', 'Atlas Van Lines', 'Baskin-Robbins', 'CalArk International Trucking', 'Campbell Soup Company',  'Chipotle Mexican Grill', 'Coca-Cola Company', 'Comcast', 'Dairy Queen', 'Davis Transport Inc', 'Dunkin Donuts', 'Facebook', 'Five Guys Burgers and Fries', 'Genentech', 'Goodwill Industries', 'Google', 'Hampton Inn', 'Hilton Hotels', 'Home Depot', 'IBM', 'IHOP', 'In-N-Out Burger', 'Kohls', 'Landstar Trucking', 'Lowes', 'Lyft', 'Marriott Hotels', 'McDonalds', 'Mobil Oil', 'New York Times', 'Olive Garden', 'Outback Steakhouse', 'Party City', 'Pepsi-Co', 'PetSmart', 'PGT Trucking', 'Red Lobster', 'Red Robin', 'Residence Inn', 'Shell Oil', 'Sony', 'Starbucks', 'Target Stores', 'TGI Friday', 'Uber', 'United Parcel Service', 'Valvoline Instant Oil Change']
	user_ratings = np.zeros(len(ratings))
	
	curr_company = ''
	for company in company_titles:
		if company in input:
			curr_company = company
	print(curr_company)
	for i in xrange(0, len(company_titles)):
		if curr_company == company_titles[i]:
			user_ratings[i] = rateNum(input)
	#self.binarize()
	guessed_scores = np.zeros(len(ratings))
	user_rated = np.where(user_ratings != 0)[0] # indices of companies the user has provided a rating for
	for i in range(len(ratings)):
		rating = 0.0
		if i not in user_rated:
			for j in user_rated:
				rating += user_ratings[j] * distance(ratings[j], ratings[i])
		guessed_scores[i] = rating
	sorted_idx = np.argsort(guessed_scores)[::-1]
	recommendations = [company_titles[sorted_idx[i]] for i in range(3)]
	print(recommendations)
	return jsonify(results=recommendations)
	
# [year in prison, years ago in prison, age, type of felon]	
@app.route('/vhacks/findMatch', methods=['GET', 'POST'])
def bestMatch(allUsers):
	currUser = request.form.getlist('info_ids', type=int)
	bestScore = distance(currUser, allUsers[0])
	bestMatch = allUsers[0]
	for user in allUsers:
		currScore = distance(currUser, user)
		if currScore > bestScore:
			bestScore = currScore
			bestMatch = user
	return bestMatch
	
@app.route('/vhacks/givetips', methods=['GET', 'POST'])
def giveTips():
	tips = ['Address any concerns an employer might have about your past.', 'Steer the interview to your skills and the positive traits that you bring to the job.', 'Avoid talking about negative issues at the very beginning or the end of an interview.', 'Use every opportunity to talk about your current activities and future plans.', 'Emphasize the education and job training, community work, and other activities you have done since your release.', 'Talk about your career goals, how you chose them, and how the job you are applying for fits those goals.', 'Don\'t lie to an interviewer or put false information on your resume or application.']
	if len(tips) != 0:
		#print(tips[0])
		#tips = tips[1:]
		print(random.choice(tips))
		return random.choice(tips)
	else:
		print('Be yourself!')
		return 'Be yourself!'
		
@app.route('/vhacks/rate/<string:input>', methods=['GET', 'POST'])
def rate(input):
	p = PorterStemmer()
	negWords = ["not", "isn't", "didn't", "never", "no", "neither", "none", "wasn't", "can't", "won't"]
	conjunct = ["for", "and", "nor", "but", "or", "yet", "so", "however", "while", "since"]
	reader = csv.reader(open('data/sentiment.txt', 'rb'))
	sentiment = dict(reader)

	processed = re.sub(r'[^A-Za-z\s\']', r'', re.sub(r'"[^"]*?"', r'', input.lower())).split(' ')
	for i in range(len(processed)):
		processed[i] = p.stem(processed[i])
	neg_score, pos_score = 0, 0
	notFlag = False
	for word in processed:
		lambda_ = 1
		if notFlag and (word in string.punctuation or word in conjunct):
			notFlag = False
		if word in sentiment:
			if sentiment[word] == 'neg':
				neg_score += lambda_ * 1 * (-1 if notFlag else 1)
			elif sentiment[word] == 'pos':
				pos_score += lambda_ * 1 * (-1 if notFlag else 1)
		if word in negWords:
			notFlag = not notFlag
	if neg_score > pos_score:
		return 'This answer is a little too negative for a job interivew.'
		#return -1.0
	else:
		return 'This answer sounds good!'
		#return 1.0

def rateNum(input):
	p = PorterStemmer()
	negWords = ["not", "isn't", "didn't", "never", "no", "neither", "none", "wasn't", "can't", "won't"]
	conjunct = ["for", "and", "nor", "but", "or", "yet", "so", "however", "while", "since"]
	reader = csv.reader(open('data/sentiment.txt', 'rb'))
	sentiment = dict(reader)

	processed = re.sub(r'[^A-Za-z\s\']', r'', re.sub(r'"[^"]*?"', r'', input.lower())).split(' ')
	for i in range(len(processed)):
		processed[i] = p.stem(processed[i])
	neg_score, pos_score = 0, 0
	notFlag = False
	for word in processed:
		lambda_ = 1
		if notFlag and (word in string.punctuation or word in conjunct):
			notFlag = False
		if word in sentiment:
			if sentiment[word] == 'neg':
				neg_score += lambda_ * 1 * (-1 if notFlag else 1)
			elif sentiment[word] == 'pos':
				pos_score += lambda_ * 1 * (-1 if notFlag else 1)
		if word in negWords:
			notFlag = not notFlag
	if neg_score > pos_score:
		return -1.0
	else:
		return 1.0

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)
