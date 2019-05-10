from flask import Flask,url_for,render_template,request

# NLP Pkgs
from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
#from gensim.summarization import summarize

import spacy
nlp = spacy.load('en')
import time
#Web scrapping pkg
from bs4 import BeautifulSoup
# from urllib import urlopen
from urllib.request import urlopen

application = app = Flask(__name__)

# Home[2]

#Function
def readingTime(mytext):
	total_words = len([token.text for token in nlp(mytext)])
	estimated_time = total_words/265.0
	return estimated_time

#Fetch data from url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page,"lxml")
	#fetch all p tags and put them together
	fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		#Summarization
		final_summary = text_summarizer(rawtext)
		# Time to read
		summ_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end - start
	return render_template('index.html',
		ctext = rawtext,
		final_summary = final_summary, 
		final_time = final_time,
		final_reading_time = final_reading_time,
		summary_reading_time = summ_reading_time)

@app.route('/analyze_url', methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		#Summarization
		final_summary = text_summarizer(rawtext)
		# Time to read
		summ_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end - start
	return render_template('index.html',
		ctext = rawtext,
		final_summary = final_summary, 
		final_time = final_time,
		final_reading_time = final_reading_time,
		summary_reading_time = summ_reading_time)


@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

if __name__ == '__main__':
	app.run(debug=True)
