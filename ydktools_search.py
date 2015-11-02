#!/usr/bin/env python
"""
A command line application for viewing information about individual cards.
"""

import yugioh
import sys, locale, re

ACTIONS = {}

def action(v):
	def decorator(f):
		ACTIONS[v] = f
		return f
	return decorator

def _money_fmt(usd):
	# in the future, do price conversions from usd to locale currency.
	return locale.currency(usd)

def get_quickprice(cardname, verbose = False):
	price_data = yugioh.yugiohprices.get_price_data(cardname)
	low = min(version.price.low for version in price_data if version.price)
	return _money_fmt(low)

def get_info(cardname, verbose = False):
	card = yugioh.ygopro.load_card(cardname)
	return card.description()

def get_prints(cardname, verbose = False):
	printruns = []
	price_data = yugioh.yugiohprices.get_price_data(cardname)
	for version in price_data:
		if version.price:
			text = '({}) {} (~{}) from "{}"'.format(version.print_tag, version.rarity, _money_fmt(version.price.low), version.set_name)
		else:		
			text = '({}) {} from "{}"'.format(version.print_tag, version.rarity, version.set_name)
		printruns.append(text)
	return str(cardname) + '\n' + ('\n'.join(printruns))

def find_cards(expr, verbose = False):
	with yugioh.ygopro.database() as db:
		cards = db.search(expr, by='sql')
		if verbose:
			return '----------------'.join(card.description() for card in cards)
		else:
			return '\n'.join(card.name for card in cards)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Get information about a yugioh card.")
	parser.add_argument('cardname', help='The full name of the card. Spelling and punctuation is important. Alternately can be the Card Number or Card ID (printed on the lower left hand corner of most cards).')
	parser.add_argument('-v', '--verbose', help='Show more information than normal', action='store_true')
	parser.add_argument('-q', '--quickprice', help='Get a quick price check summary of all the releases of the card.', action='store_true')
	parser.add_argument('-p', '--prints', help='Get all the print runs of the card.', action='store_true')
	parser.add_argument('-i', '--info', help='Get the text and stats of the card.', action='store_true')

	parser.add_argument('-f', '--find', help='Find a card using sql expressions.', action='store_true')
	
	
	args = parser.parse_args()
	locale.setlocale(locale.LC_ALL, '')
	
	verbosity = args.verbose
	
	cardname = args.cardname
		
	if args.quickprice:
		sys.stdout.write(get_quickprice(cardname, verbosity) + '\n')
	else:
		if args.prints:
			sys.stdout.write(get_prints(cardname, verbosity) + '\n')
		if args.info:
			sys.stdout.write(get_info(cardname, verbosity) + '\n')
		if args.find:
			sys.stdout.write(find_cards(cardname, verbosity) + '\n')