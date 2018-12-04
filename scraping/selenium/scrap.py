from selenium import webdriver
import time
import csv
### Windows
PATH_chrome_driver = './chrome-driver/chromedriver.exe'
### macOS
#PATH_chrome_driver = './chrome-driver/chromedriver'
### load the driver
driver = webdriver.Chrome( PATH_chrome_driver )

URL_target = 'https://www.workana.com/freelancers'
# output file
PATH_output = './result.csv'
# time to wait for the page to refresh
TIME_pending = 2


header = ''