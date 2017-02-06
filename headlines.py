import feedparser
from flask import Flask, render_template

app = Flask(__name__)

feeds = {
		'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'cnbc': 'http://www.cnbc.com/id/100003114/device/rss/rss.xml'}


@app.route("/")
def nav():
	return render_template("layout.html")

@app.route("/<publication>")
def get_news(publication='bbc', params=['title', 'published', 'summary']):
	feed = feedparser.parse(feeds[publication])
	return render_template("layout.html", articles=feed['entries'], n = publication)

if __name__ == '__main__':
	app.run(port=5000, debug=True)