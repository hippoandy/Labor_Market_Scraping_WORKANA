
import pandas as pd

## get csv data

url.request( "URL", "file.csv" )
pd.read_csv( "file.csv", index_col='', parse_dates=True )