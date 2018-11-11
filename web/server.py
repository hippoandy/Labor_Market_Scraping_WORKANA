from flask import Flask, render_template

import pandas as pd
import numpy as np
import json
import sys

app = Flask(__name__)

dataset = 'dataset/workana.csv'

metadata = {}

@app.route('/')
def homePage():

    title = "WORKANA Analysis"
    paragraph = "This is the analytic result toward the 'Freelancer' section of the website WORKANA."

    df = pd.read_csv( dataset )
    # print( df.groupby('country').groups, file=sys.stderr )

    metadata[ "total_person" ] = len( df.index )
    metadata[ "avg_hourly_r" ] = df[ 'hourly_rate' ].mean()
    # calculate the country distribution
    d = df.groupby( 'country' ).groups
    # nationality distribution
    country_dist = {}
    # country hourly rate avg.
    country_avg = {}
    max_country = ( "", 0 )
    for k in d:
        v = int(len( d[ k ] ))
        country_dist[ k ] = v
        if( v > max_country[ 1 ] ): max_country = ( k, v )

        s = 0
        c = 0
        for e in d[ k ]:
            cur = df.loc[ int(e) ][ "hourly_rate" ]
            if( pd.isnull(cur) ): continue
            s += cur
            c += 1
        if( c == 0 ): country_avg[ k ] = 0
        else: country_avg[ k ] = s/c

    metadata[ "country_dist" ] = country_dist
    metadata[ "max_country" ] = max_country
    metadata[ "country_avg" ] = country_avg

    try:
        return render_template( "index.html",
            title = title,
            paragraph = paragraph,
            metadata = metadata
        )
    except Exception as e: return str(e)

@app.route('/about')
def aboutPage():

    title = "About this site"
    paragraph = "UN Webscraping"

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)

if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)