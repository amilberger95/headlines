import feedparser
from flask import Flask, render_template, request

app = Flask(__name__)

feeds = {
		'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'cnbc': 'http://www.cnbc.com/id/100003114/device/rss/rss.xml',
        'freep': 'http://rssfeeds.freep.com/freep/home&x=1',
        'iol': 'http://www.iol.co.za/cmlink/1.640'
        }


# @app.route("/")
# def nav():
# 	return render_template("layout.html")

# @app.route("/<publication>")
# def get_news(publication='bbc', params=['title', 'published', 'summary']):
# 	feed = feedparser.parse(feeds[publication])
# 	return render_template("layout.html", articles=feed['entries'], n = publication)

@app.route('/')
def get_news():
	query = request.args.get('publication')
	if not query or query.lower() not in feeds:
		publication = 'bbc'
	else:
		publication = query.lower()
	feed = feedparser.parse(feeds[publication])
	return render_template("layout.html", articles=feed['entries'], n = publication)

if __name__ == '__main__':
	app.run(port=5000, debug=True)