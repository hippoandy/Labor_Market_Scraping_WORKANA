from selenium import webdriver
import time
import csv

# the keyword which to perform a search
KEY_search = 'SQL'

URL_target = 'https://www.workana.com/freelancers'
# output file
PATH_output = './result.csv'
# time to wait for the page to refresh
TIME_pending = 2

PATH_chrome_driver = './chrome-driver/chromedriver'
### load the driver
driver = webdriver.Chrome( PATH_chrome_driver )

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


def write_file():
    f = open( PATH_output,'w' )
    f.write( 'Healthy' + ',' )
    f.write( '\n' )
    f.write( 'nextline' + ',' + 'next entry' )
    f.close()

if __name__ == '__main__':
    try:
        keyword_search()
        # write_file()
    except KeyboardInterrupt: driver.close()
