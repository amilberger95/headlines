import feedparser
from flask import Flask, render_template, request, make_response
import json
from urllib.request import urlopen
import urllib
import datetime
import ssl

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
	gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	all_currency = urlopen(CURRENCY_URL, context=gcontext).read().decode('utf-8')
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

def get_values_with_fallback(key):
	if request.args.get(key):
		return request.args.get(key)
	if request.cookies.get(key):
		return request.cookies.get(key)
	return DEFAULTS[key]



@app.route('/')
def home():
	#customised headlines, based on user input or default
	publication = get_values_with_fallback("publication")
	articles = get_news(publication)
	#customised weather based on user input or default
	city = get_values_with_fallback("city")
	weather = get_weather(city)
	#customised currency based on user input or default
	currency_from = get_values_with_fallback("currency_from")
	currency_to = get_values_with_fallback("currency_to")
	rate, currencies = get_currency(currency_from, currency_to)

	# save cookies and return template
	response = make_response(render_template("layout.html",
				n = publication,
				articles = articles,
				weather = weather,
				currency_from = currency_from,
				rate = rate,
				currencies=sorted(currencies)))
	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	response.set_cookie("publication", publication, expires=expires)
	response.set_cookie("city", city, expires=expires)
	response.set_cookie("currency_from", currency_from, expires = expires)
	response.set_cookie("currency_to", currency_to, expires = expires)
	return response

if __name__ == '__main__':
	app.run(port=5000, debug=True)