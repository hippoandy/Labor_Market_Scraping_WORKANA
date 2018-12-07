from selenium import webdriver
import time
import csv

# search options --------------------------------------------------

# the keyword which to perform a search
KEY_search = 'SQL'

# -------------------------------------------------- search options

URL_target = 'https://www.workana.com/freelancers'
# output file
PATH_output = './r_workana_freelancers.csv'
# time to wait for the page to refresh
TIME_pending = 2

### Windows
PATH_chrome_driver = './chrome-driver/chromedriver.exe'
### macOS
#PATH_chrome_driver = './chrome-driver/chromedriver'
### load the driver
driver = webdriver.Chrome( PATH_chrome_driver )

# csv header
header = 'name,country,rating,is_pro,hourly_rate,completed_jobs,hours_worked,skills'
# file pointer
f = None

# a large number to cover all the page number
limit = 3

# self-defined functions -------------------------------------------
def invalid_val(): return 'N/A'
# make sure there is no special char in a value
def clear_str( text ):
    text = str(text).replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' )
    return text
# replace ',' in the value
def clear_comma( text ):
    return str(text).replace( ',', '-' )
# make sure the value is numeric, otherwise return invalid_val()
def numeric( val, type='float' ):
    val = str(val) # make sure it is not 'NoneType'
    try:
        # make sure the value is numeric
        if( type == 'int' ): val = int(val)
        else: val = float(val)
        return str(val)
    except: return invalid_val()
# ------------------------------------------- self-defined functions

# workana.com using input boxes and inputting text.
def keyword_search():
    driver.get( URL_target )
    time.sleep( TIME_pending )

    box_input = driver.find_element_by_id( 'Query' )
    box_input.send_keys( KEY_search )
    
    # Using brower's css selector
    btn_search = driver.find_element_by_css_selector( '#search-form > div > div.col-sm-8.col-md-9.col-full-left > button' )

    # Using xpath
    #btn_search = driver.find_element_by_xpath('//*[@id="search-form"]/div/div[2]/button')

    # Using css selector
    #btn_search = driver.find_element_by_css_selector('button.search.icon')

    # perform the search
    btn_search.click()

    # wait for the query to be done
    time.sleep( TIME_pending )

def scrap():
    res = None
    try:
        res = driver.find_elements_by_css_selector( '#workers > div.js-worker' )
    except: return # the page is empty
    for e in res:
        # get the name of the applicant
        name = e.find_element_by_css_selector( 'div.row > div.col-sm-7 > div.row > div.worker-details > h3 > a' ).text
        name = clear_comma( clear_str( name ) )

        # get the nationality information
        country = e.find_element_by_css_selector( 'div.row > div.col-sm-7 > div.row > div.worker-details > div.row > div > span.country > span > a' ).text
        country = clear_comma( clear_str( country ) )

        # if a applicant is tagged as 'Pro'
        is_pro = 0
        try:
            e.find_element_by_css_selector( 'div.row > div.col-sm-7 > div.row > div.worker-details > h3 > span.pro-label' )
            is_pro = 1
        except: pass
        is_pro = str(is_pro)

        # the applicant rating
        rating = e.find_element_by_css_selector( 'div.row > div.col-sm-7 > div.row > div.worker-details > label > span.profile-stars > span.stars-bg' ).get_attribute( 'title' )
        rating = str(rating).replace( ' of 5.00', '' )
        rating = str(numeric( clear_comma( rating ) ))

        # get the set of skills
        skills = e.find_elements_by_css_selector( 'div.row > div.col-sm-7 > div.row.hidden-xs > div.col-sm-12 > div.skills > div.expander > a' )
        collection = []
        for s in skills: collection.append( clear_comma( s.text ) )
        skills = '|'.join( collection )

        # hourly rate information
        hourly_rate = 'N/A'
        try:
            hourly_rate = e.find_element_by_css_selector( 'div.row > div.col-sm-5 > div.row > div.worker-details > h4 > span > span' )
            # make sure the value is numeric
            hourly_rate = str(numeric( clear_comma( clear_str( str(hourly_rate.text) ) ) ))
        except: pass
        
        # completed_projects and hour_worked
        exp = e.find_elements_by_css_selector( 'div.row > div.col-sm-5 > div.row > div.worker-details > p > span' )
        c = 0
        projects = hours = invalid_val()
        for e in exp:
            if( 'Completed' in e.text ): projects = str(numeric( clear_comma( clear_str( str(e.text).replace( 'Completed projects: ', '' ) ) ), 'int' ))
            else: hours = str(numeric( clear_comma( clear_str( str(e.text).replace( 'Hours worked in hourly projects: ', '' ) ) ), 'int' ))
            c += 1
            if( c == 2 ): break

        # commit the result
        f.write( '{},{},{},{},{},{},{},{}\n'.format( name, country, rating, is_pro, hourly_rate, projects, hours, skills ) )

# the main function
if __name__ == '__main__':
    try:
        # open the webpage
        keyword_search()

        # open the file
        f = open( PATH_output,'w' )
        f.write( header + '\n' )

        # start scraping
        # the first page is already loaded, scrap first
        scrap()
        # get the modified url and append parameter
        cur = driver.current_url
        cur += '?page='
        for i in range( 2, limit ):
            driver.get( cur + str(i) )
            time.sleep( TIME_pending )
            scrap()
    except KeyboardInterrupt: driver.close()
    # safely close the file
    f.close()
