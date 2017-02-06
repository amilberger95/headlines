import feedparser
from flask import Flask, render_template, request
import json
from urllib.request import urlopen
import urllib
import codecs

app = Flask(__name__)

feeds = {
		'cnn': 'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
        'cnbc': 'http://www.cnbc.com/id/100003114/device/rss/rss.xml',
        'freep': 'http://rssfeeds.freep.com/freep/home&x=1',
        'iol': 'http://www.iol.co.za/cmlink/1.640'
        }

DEFAULTS = {
			'publication': 'cnn', 
			'city': 'Ann Arbor, Michigan',
 			'currency_from': 'BTC',
 			'currency_to': 'USD'
 			}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=75959a8f735cfa6cef25bc188999fcab"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=f1b4e64be78b48b1ae73ab2f618bbc4b"

def get_weather(query):
	api_url = WEATHER_URL
	query = urllib.parse.quote(query)
	url = api_url.format(query)
	data = urlopen(url).read().decode('utf-8')
	parsed = json.loads(data)
	weather = None

	if parsed.get('weather'):
		temp = int(parsed["main"]["temp"])/10
		weather = {"description":parsed["weather"][0]["description"],"temperature":temp,"city":parsed["name"]}
	return weather

def get_currency(frm, to):
	all_currency = urlopen(CURRENCY_URL).read().decode('utf-8')
	parsed = json.loads(all_currency).get('rates')
	from_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate/from_rate, parsed.keys())


def get_news(query):
	if not query or query.lower() not in feeds:
		publication = DEFAULTS['publication']
	else:
		publication = query.lower()
	feed = feedparser.parse(feeds[publication])
	return feed['entries']


@app.route('/')
def home():
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)

	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)

	currency_from = request.args.get('currency_from')
	if not currency_from:
		currency_from = DEFAULTS['currency_from']
	currency_to = request.args.get('currency_to')
	if not currency_to:
		currency_to = DEFAULTS['currency_to']
	rate, currencies = get_currency(currency_from, currency_to)

	return render_template("layout.html", articles=articles, n = publication, weather=weather, currency_from = currency_from, currency_to = currency_to, rate = rate, currencies=sorted(currencies))

if __name__ == '__main__':
	app.run(port=5000, debug=True)