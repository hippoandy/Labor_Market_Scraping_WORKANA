from bs4 import BeautifulSoup
import requests
import time
import csv

import utils

# parameters ------------------------------------------------------
base_url = 'https://www.mercadolibre.com'

# csv header
header = 'name,country,rating,is_pro,hourly_rate,completed_jobs,hours_worked,skills'
# output file
path_output = './r_bumeran.csv'

# time to wait for the page to refresh
time_pending = 2
# ------------------------------------------------------ parameters

# element identifiers ---------------------------------------------
category_page = 'categories.html'
# --------------------------------------------- element identifiers

# file pointer
f = None

# self-defined functions -------------------------------------------
def invalid_val(): return 'N/A'
# make sure there is no special char in a value
def clear_str( text ):
    text = str(text).replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' )
    return text
# replace ',' in the value
def clear_comma( text ):
    return str(text).replace( ',', '-' )
def is_numeric( val, type='float' ):
    val = str(val) # make sure it is not 'NoneType'
    try: # make sure the value is numeric
        if( type == 'int' ): val = int(val)
        else: val = float(val)
        return True
    except: return False
# make sure the value is numeric, otherwise return invalid_val()
def numeric( val, type='float' ):
    if( is_numeric( val, type ) ): return str(val)
    else: return invalid_val()
# ------------------------------------------- self-defined functions

# finding the country list and scraping the urls
def country_portals():
    c_links = [] # varaible to hold the country information
    try:
        r = requests.get( base_url, timeout=10 ) # get web code
    except:
        print( "Failed to load portal list of countries!" )
        return []

    soup = BeautifulSoup( r.text, 'html.parser' ) # Beautiful Soup parser
    t = soup.find_all( 'a', class_='ml-site-link' )
    for e in t:
        soup = BeautifulSoup( str(e), 'html.parser' )
        c_links.append( { 'name': e.text, 'link': e[ 'href' ] } )

    return c_links

# finding the list of categories within department in interests
def categories( url ):
    global groups
    # basic department in interest
    category_interest = [ 'camera', 'computer', 'computing', 'celluar', 'phone', 'console', 'electronics' ]

    try:
        r = requests.get( url, timeout=10 ) # get web code
    except:
        print( "Failed to load portal list of countries!" )
        return []
    
    soup = BeautifulSoup( r.text, 'html.parser' ) # Beautiful Soup parser
    anchors = [h2.find('a') for h2 in soup.findAll( 'h2' )]

    groups = []
    for a in anchors: groups.append( { "original": a.text, "link": a[ 'href' ], "translated": "" } )

    utils.Translate( name="translate_groups", concurrent=30 ).input( groups ).run()

    # deleting groups without interests
    groups = [e for e in groups if any( word in str(e[ 'translated' ]).lower() for word in category_interest )]

    print( groups )


def scrape( info ):
    print( 'hello' )


# the main function
if __name__ == '__main__':
    # find the countries list and corresponding urls
    portals = country_portals()
    c_dept_failed = []
    for c in portals:
        # get the list of departments and categories
        url = c[ 'link' ] + '/{}'.format( category_page )
        print( url )
        categories( url )
        break

