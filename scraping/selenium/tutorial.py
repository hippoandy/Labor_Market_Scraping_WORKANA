from selenium import webdriver
import time
import csv

URL_target = 'https://www.workana.com/jobs'
PATH_chrome_driver = '../chrome-driver/chromedriver'
PATH_output = ''

### MAC
driver = webdriver.Chrome( PATH_chrome_driver )

# workana.com using input boxes and inputting text.
def getToWorkAnaDotCom():
    driver.get( URL_target )
    time.sleep(1)
    inputBox = driver.find_element_by_id('Query')

    inputBox.send_keys('search query')
    
    # Using brower's css selector
    searchButton = driver.find_element_by_css_selector('#search-form > div > div.col-sm-8.col-md-9.col-full-left > button')

    # Using xpath
    #searchButton = driver.find_element_by_xpath('//*[@id="search-form"]/div/div[2]/button')

    # Using css selector
    #searchButton = driver.find_element_by_css_selector('button.search.icon')

    searchButton.click()

### workana.com using url query
### Print all the hyperlinks 
def getToWorkAnaDotComQuery():
    driver.get('https://www.workana.com/jobs?query=query+here&publication=any&language=en')

    time.sleep(2)
    listOfResults = driver.find_elements_by_css_selector('div.listing.wrapper-project.js-project ')

    for elementItem in listOfResults:
        linkText = elementItem.find_element_by_css_selector('span').text

        ### Finds name and href associated with that item. Tells browser to click that name.
        #driver.find_element_by_link_text(linkText).click()

        ### Chain functions to dive deeper into the DOM
        hrefLink = driver.find_element_by_css_selector('h2.h2.project-title').find_element_by_css_selector('a').get_attribute('href')

        print(linkText)
        print(hrefLink)

def writeToCsv():
    csvFile = open('/Users/billyliu/Desktop/testfile.csv','w')
    csvFile.write('Healthy' + ',')
    csvFile.write('\n')
    csvFile.write('nextline' + ',' + 'next entry')
    csvFile.close()

if __name__ == '__main__':
    try:
        #getToWorkAnaDotCom()
        #getToWorkAnaDotComQuery()
        writeToCsv()
    except KeyboardInterrupt:
        driver.close()
