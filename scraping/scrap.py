from bs4 import BeautifulSoup
import requests


target_class = 'js-worker'

# the website url
url = 'https://www.workana.com/en/freelancers?page='

# get web code
r = requests.get( url )

# Beautiful Soup parser
soup = BeautifulSoup( r.text, 'html.parser' )

t = soup.find_all( 'div', class_=target_class )
soup = BeautifulSoup( str(t[ 0 ]), 'html.parser' )
