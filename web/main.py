import os, json ,crochet
from flask import Flask, render_template, jsonify, request, redirect, url_for
from scrapy.crawler import CrawlerRunner
from flask_executor import Executor

# Importing our Scraping Function from the scraping file
from scanner.scanner.spiders.SecretsScraper import SecretsScraper

# Creating Flask App Variable
app = Flask(__name__)

#Flask Executor
executor = Executor(app)
crochet.setup()
crawl_runner = CrawlerRunner()

# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
	return render_template("index.html") # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['url'] # Getting the Input URL
        global baseURL
        baseURL = s

        # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
        if os.path.exists("output.json"): 
            os.remove("output.json")
        
        scrape(baseURL) #Start scraping
    #render_template("index.html", submit=True) #Todo: Improve app by showing results on the main page itself
    return redirect(url_for('results')) # Passing to the Scrape function


def scrape(baseURL):
    executor.submit(crawl_runner.crawl(SecretsScraper, baseURL = baseURL))


@app.route("/results")
def results():
    crawl_results_file = "output.json"
    headings = ['URL', 'leaked secrets', 'artifacts']

    if os.path.exists(crawl_results_file) and os.path.getsize(crawl_results_file) > 0:
        try:
            f = open(crawl_results_file)    
            data = json.load(f)
            return render_template("table.html", headings=headings, data=data)
        except Exception as ex:
            return """Formatting results <img src="https://cutewallpaper.org/21/loading-gif-transparent-background/Tag-For-Loading-Bar-Gif-Transparent-Loading-Gif-.gif" height="10" width="10">   <meta http-equiv="refresh" content="5">"""
    else:
        return """Waiting for the results <img src="https://cutewallpaper.org/21/loading-gif-transparent-background/Tag-For-Loading-Bar-Gif-Transparent-Loading-Gif-.gif" height="10" width="10">   <meta http-equiv="refresh" content="5">"""



if __name__== "__main__":
    app.run(debug=True)
