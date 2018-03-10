#!/usr/bin/python
import csv
import re
import string
import numpy as np
from scipy import spatial
from PorterStemmer import PorterStemmer
from flask import Flask

class Chatbot:
	def __init__(self):
		# ratings for each company:[truck driver, food, cashier, tech, hotel, assistant, no experience] 1 = no 2 = yes
		self.ratings = [[1, 2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 2],  [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 1, 1, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 2, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 1], [2, 1, 1, 1, 1, 1, 2], [1, 1, 2, 1, 1, 2, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 2, 1, 2], [1, 2, 2, 1, 1, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [1, 1, 2, 1, 1, 1, 2], [2, 1, 1, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 2, 1, 2], [2, 1, 1, 2, 1, 2, 1], [1, 1, 1, 2, 1, 2, 1], [1, 2, 2, 1, 1, 1, 2], [1, 1, 2, 1, 1, 1, 2], [1, 2, 2, 1, 1, 1, 2], [1, 1, 1, 2, 1, 2, 1], [2, 1, 2, 1, 1, 1, 2],  [2, 1, 1, 2, 1, 2, 1]]
		self.company_titles = ['Albertson', 'American Orange Trucking', 'Atlas Van Lines', 'Baskin-Robbins', 'CalArk International Trucking', 'Campbell Soup Company',  'Chipotle Mexican Grill', 'Coca-Cola Company', 'Comcast', 'Dairy Queen', 'Davis Transport Inc', 'Dunkin Donuts', 'Facebook', 'Five Guys Burgers and Fries', 'Genentech', 'Goodwill Industries', 'Google', 'Hampton Inn', 'Hilton Hotels', 'Home Depot', 'IBM', 'IHOP', 'In-N-Out Burger', 'Kohls', 'Landstar Trucking', 'Lowes', 'Lyft', 'Marriott Hotels', 'McDonalds', 'Mobil Oil', 'New York Times', 'Olive Garden', 'Outback Steakhouse', 'Party City', 'Pepsi-Co', 'PetSmart', 'PGT Trucking', 'Red Lobster', 'Red Robin', 'Residence Inn', 'Shell Oil', 'Sony', 'Starbucks', 'Target Stores', 'TGI Friday', 'Uber', 'United Parcel Service', 'Valvoline Instant Oil Change']
		self.user_ratings = np.zeros(len(self.ratings))
		self.tips = ['Address any concerns an employer might have about your past.', 'Steer the interview to your skills and the positive traits that you bring to the job.', 'Avoid talking about negative issues at the very beginning or the end of an interview.', 'Use every opportunity to talk about your current activities and future plans.', 'Emphasize the education and job training, community work, and other activities you have done since your release.', 'Talk about your career goals, how you chose them, and how the job you are applying for fits those goals.', 'Don\'t lie to an interviewer or put false information on your resume or application.']
		self.p = PorterStemmer()
		self.negWords = ["not", "isn't", "didn't", "never", "no", "neither", "none", "wasn't", "can't", "won't"]
		self.conjunct = ["for", "and", "nor", "but", "or", "yet", "so", "however", "while", "since"]
		reader = csv.reader(open('data/sentiment.txt', 'rb'))
		self.sentiment = dict(reader)
		self.main()
	
	def main(self):
		# all companies are known to hire ex-convicts
		
		# given past experience & using sentiment analysis, return list of 3 companies based on item to item collaborative filtering
		self.recommend('I worked at American Orange Trucking and I loved it.')
		
		# given list of areas open to work in, [truck driver, food, cashier, tech, hotel, assistant, no experience] 1 = no 2 = yes, recommend
		self.recommendSpecified([2, 1, 1, 1, 1, 1, 1])
		
		# given area to work in [truck driver, food, cashier, tech, hotel, assistant, no experience] with indexes [0, 1, 2, 3, 4, 5, 6], recommend
		self.findJobs(0)
		
		# find companies with jobs that require no experience
		self.noExperience()
		
		# give out tips for ex-convicts when interviewing
		self.giveTips()
		
		# given an interview answer, use stemmer and sentiment analysis to determine if it's positive enough
		self.rate('I am willing to put in my all into your company.')
		self.rate('I didn\'t really do well, and was not a good employee.')
		
		#self.bestMatch() needs user information
	
	def findJobs(self, field):
		recommendations = []
		for i in xrange(0, len(self.ratings)):
			rate = self.ratings[i]
			if rate[field] == 2:
				recommendations.append(self.company_titles[i])
		print(recommendations)
	
	def noExperience(self):
		return self.findJobs(6)
		
	def binarize(self):
		for i in range(len(self.ratings)):
			self.ratings[i] = np.where(np.logical_and(0 < self.ratings[i], self.ratings[i] < 3.0), -1.0, self.ratings[i])
			self.ratings[i] = np.where(self.ratings[i] > 3.0, 1.0, self.ratings[i])
			self.ratings[i] = np.where(self.ratings[i] == 3.0, 0.0, self.ratings[i])

	def distance(self, u, v):
		return 1 - spatial.distance.cosine(u, v)

	def recommendSpecified(self, job):
			guessed_scores = np.zeros(len(self.ratings))
			for i in range(len(self.ratings)):
				rating = self.distance(self.ratings[i], job)
				guessed_scores[i] = rating
			
			sorted_idx = np.argsort(guessed_scores)[::-1]
			self.recommendations = [self.company_titles[sorted_idx[i]] for i in range(3)]
			print(self.recommendations)
	
	def recommend(self, input):
		curr_company = ''
		for company in self.company_titles:
			if company in input:
				curr_company = company
		print(curr_company)
		for i in xrange(0, len(self.company_titles)):
			if curr_company == self.company_titles[i]:
					self.user_ratings[i] = self.rate(input)
		
		self.binarize()
		guessed_scores = np.zeros(len(self.ratings))
		user_rated = np.where(self.user_ratings != 0)[0] # indices of companies the user has provided a rating for
		for i in range(len(self.ratings)):
			rating = 0.0
			if i not in user_rated:
				for j in user_rated:
					rating += self.user_ratings[j] * self.distance(self.ratings[j], self.ratings[i])
			guessed_scores[i] = rating
		
		sorted_idx = np.argsort(guessed_scores)[::-1]
		self.recommendations = [self.company_titles[sorted_idx[i]] for i in range(3)]
		print(self.recommendations)
	
	# [year in prison, years ago in prison, age, type of felon]	
	def bestMatch(self, currUser, allUsers):
		bestScore = distance(currUser, allUsers[0])
		bestMatch = allUsers[0]
		for user in allUsers:
			currScore = distance(currUser, user)
			if currScore > bestScore:
				bestScore = currScore
				bestMatch = user
		return bestMatch
		
	def giveTips(self):
		if len(self.tips) != 0:
			print(self.tips[0])
			self.tips = self.tips[1:]
		else:
			print('Be yourself!')
			
	def rate(self, input):
		processed = re.sub(r'[^A-Za-z\s\']', r'', re.sub(r'"[^"]*?"', r'', input.lower())).split(' ')
		for i in range(len(processed)):
			processed[i] = self.p.stem(processed[i])
		neg_score, pos_score = 0, 0
		notFlag = False
		for word in processed:
			lambda_ = 1
			if notFlag and (word in string.punctuation or word in self.conjunct):
				notFlag = False
			if word in self.sentiment:
				if self.sentiment[word] == 'neg':
					neg_score += lambda_ * 1 * (-1 if notFlag else 1)
				elif self.sentiment[word] == 'pos':
					pos_score += lambda_ * 1 * (-1 if notFlag else 1)
			if word in self.negWords:
				notFlag = not notFlag
		if neg_score > pos_score:
			print('This answer is a little too negative for a job interivew.')
			return -1.0
		else:
			print("This answer sounds good!")
			return 1.0

	
if __name__ == '__main__':
	Chatbot()