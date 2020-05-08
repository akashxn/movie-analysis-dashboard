############################################################
'''
author: Akash Negi

'''

#IMPORTING LIBRARIES
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

dict = {'The Funeral' : 'https://brooklyn99.fandom.com/wiki/The_Funeral/Transcript',
		'Pilot' : 'https://brooklyn99.fandom.com/wiki/Pilot/Transcript',
		'New Captain' : 'https://brooklyn99.fandom.com/wiki/New_Captain/Transcript'
		}

for key in dict:


	#SPECIFY THE URL
	b99 = dict[key]

	#GET HTML FROM THE WEBPAGE
	page = urlopen(b99)

	#PARSE THE HTML USING BEAUTIFULSOUP
	soup = BeautifulSoup(page, 'lxml')

	text_file = open(str(key)+'.txt','a')

	#GETTING ALL THE PARAGRAPH TEXT IN  A TEXT FILE
	for paragraph in soup.find_all('p'):
		text_file.write(paragraph.text)

	text_file.close()
	print('1/2 | Text File Created!')

	################################################################

	#CLEANING THE DATA AND GENERATING A CSV DATASET
	with open(str(key)+'.txt', 'r') as tf:
		all_lines = tf.readlines()


	for line in all_lines:
		if line[:1] == '[':
			pass
		else:
			line = line.replace('[','')
			line = line.replace(']','')
			with open (str(key)+'.csv','a') as csv_file:
				writer = csv.writer(csv_file)
				if ':' in line:
					details = line.strip().split(':')
					writer.writerow([details[0], details[1]])
	tf.close()

	print('2/2 | CSV Dataset Created!')

	################################################################

	print('===========================\nExtracting next episode\n===========================')




