"""
A frontend for the yugiohprices api. Gets price data on a card.

May eventually create a more in-depth query library that uses this api.
"""

import json
import sys
from . import core, price

if sys.version_info.major == 2:
	from urllib import urlopen, quote_plus
elif sys.version_info.major == 3:
	from urllib.request import urlopen
	from urllib.parse import quote_plus
else:
	svi = sys.version_info
	raise NotImplementedError('Python version {0}.{1}.{3} not supported'.format(svi.major, svi.minor, svi.micro))
	
class APIError(RuntimeError): pass

def get_price_data(card):
	"""get_price_data(string cardname OR core.card.YugiohCard card)
	-> price.CardVersion list
	
	get all price information available for a single card from the YugiohPrices api.
	"""
	if isinstance(card, core.card.YugiohCard):
		cardname = card.name
	else:
		cardname = card
		
	cname = quote_plus(cardname)
	url = 'http://yugiohprices.com/api/get_card_prices/{0}'.format(cname)
	
	fl = urlopen(url)
	if sys.version_info.major == 3:
		text = fl.readall().decode('utf-8')
	else:
		text = fl.read()
	
	info = json.loads(text)
	
	fl.close()
	if info['status'] == 'fail':
		raise APIError(info['message'])
	else:
		versions = []
		for version in info['data']:
			set_name = version['name']
			print_tag = version['print_tag']
			rarity = version['rarity']
			price_data = None
			if version['price_data']['status'] == 'success':
				price_info = version['price_data']['data']['prices']
				price_data = price.PriceHistory(
					price_info['high'],
					price_info['average'],
					price_info['low'],
					{
						  1 : price_info['shift'],
						  3 : price_info['shift_3'],
						  7 : price_info['shift_7'],
						 21 : price_info['shift_21'],
						 30 : price_info['shift_30'],
						 90 : price_info['shift_90'],
						180 : price_info['shift_180'],
						365 : price_info['shift_365']
					}
				)
			release = price.CardVersion(set_name, print_tag, rarity, price_data)
			
			versions.append(release)
		return versions

def rarities(card):
	"""rarities(core.card.YugiohCard) -> string list
	Return a list of all rarities the card is available in"""
	data = get_price_data(card)
	releases = set()
	for version in data:
		releases.add(version.rarity)
	return list(releases)

def get_price(card):
	"""get_price(core.card.YugiohCard) -> int (dollars)
get the minimum expected price for the given card"""
	card_data = get_price_data(card)
	return min([version.price.low for version in card_data])

def get_prices(cards):
	"""get_prices(core.card.YugiohCard iterable) -> int (dollars) list
get the minimum expected price for the given cards"""
	return [get_price(card) for card in cards]
