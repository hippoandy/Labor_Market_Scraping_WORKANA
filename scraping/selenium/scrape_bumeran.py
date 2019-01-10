from selenium import webdriver
import time
import csv

from googletrans import Translator
translator = Translator()

# parameters ------------------------------------------------------

URL_main = 'http://www.bumeran.com'

# csv header
header = 'name,country,rating,is_pro,hourly_rate,completed_jobs,hours_worked,skills'
# output file
PATH_output = './r_bumeran.csv'

# time to wait for the page to refresh
TIME_pending = 2
# ------------------------------------------------------ parameters


# element identifiers ---------------------------------------------
ID_country_list = 'menu1'
C_page_selector = 'pagination'
# --------------------------------------------- element identifiers

### Windows
# PATH_chrome_driver = './chrome-driver/chromedriver.exe'
### macOS
PATH_chrome_driver = './chrome-driver/chromedriver'
### load the driver
driver = webdriver.Chrome( PATH_chrome_driver )
# file pointer
f = None
# varaible to hold the country information
LIST_country = []

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
    try:
        # make sure the value is numeric
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
def countries():
    # get the url list
    countries = driver.find_elements_by_css_selector( '#' + ID_country_list + ' > li' )
    for c in countries:
        c = c.find_elements_by_tag_name( 'a' )
        name = str(c[ 0 ].get_attribute( 'title' ))
        link = str(c[ 0 ].get_attribute( 'href' ))
        # handling exception for Chile
        if( 'Chile' in name ): link = 'https://www.laborum.cl/'
        obj = { "name": name, "link": link }
        LIST_country.append( obj )

def scrap( info ):
    # get the country name in english (essentially to match the file name of the webpage)
    country = translator.translate( info[ "name" ], 'en' ).text
    url = info[ "link" ]+ 'empleos-' + str(country).lower()
    print( url )

    # load the new url
    driver.get( url + '.html' ) # open the website
    time.sleep( TIME_pending ) # wait for the website to load

    # # find the last page
    page_selector = driver.find_elements_by_css_selector( 'ul.' + C_page_selector + ' > li' )
    max_pnum = 0
    for e in page_selector:
        if( is_numeric( e.text, 'int' ) ):
            if( int(e.text) > max_pnum ): max_pnum = int(e.text)
    print( max_pnum )

    for i in range( 1, max_pnum + 1 ):
        # load the new url
        driver.get( url + '-pagina-' + str(i) + '.html' ) # open the website
        time.sleep( TIME_pending ) # wait for the website to load

        list_items = driver.find_elements_by_css_selector( 'div.aviso' )
        for e in list_items:
            # get the title of the job
            title = e.find_element_by_css_selector( 'div.wrapper.col-sm-9 > a > h3.titulo-aviso' ).get_attribute( 'title' )
            url_desc = e.find_element_by_css_selector( 'div.wrapper.col-sm-9 > a' ).get_attribute( 'herf' )

            print( "{}, {}".format(title, url_desc) )
        break

# the main function
if __name__ == '__main__':
    try:
        # open the website
        driver.get( URL_main )
        # wait for the website to load
        time.sleep( TIME_pending )
        # find the countries list and corresponding urls
        countries()

        # if successfully obtain url list
        if( len(LIST_country) != 0 ):
            # open the file
            f = open( PATH_output,'w' )
            f.write( header + '\n' )

            for e in LIST_country:
                # start scraping
                scrap( e )
                break

            # safely close the file
            f.close()
        else:
            print( "Failed to load the url list for Bumeran.com" )

    except KeyboardInterrupt: driver.close()
