import feedparser
from flask import Flask, render_template

app = Flask(__name__)

feeds = {'marketwatch' :'http://feeds.marketwatch.com/marketwatch/stockstowatch?format=xml',
		'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml'}


@app.route("/")
def nav():
	return render_template("layout.html")

@app.route("/<publication>")
def get_news(publication='bbc', params=['title', 'published', 'summary']):
	if publication == "marketwatch":
		params = ['title', 'link', 'description']
	feed = feedparser.parse(feeds[publication])
	first_article = feed['entries'][0]
	return render_template("layout.html", title = first_article[params[0]], pub = first_article[params[1]], sum = first_article[params[2]], n = publication )#.format(first_article.get(params[0]), first_article.get(params[1]), first_article.get(params[2]), publication)
	#return first_article[params[1]]
if __name__ == '__main__':
	app.run(port=5000, debug=True)