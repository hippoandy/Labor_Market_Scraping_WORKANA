from flask import Flask, jsonify, render_template, request, Response, Blueprint

import base64
import json
import sys
import io
import random
import math
import pandas as pd
import numpy as np
import seaborn
import scipy
# ref. https://github.com/palantir/python-language-server/issues/217
import matplotlib
matplotlib.use('TkAgg')
matplotlib.style.use( 'seaborn' )
import matplotlib.pyplot as plt

app = Flask(__name__)

bp = Blueprint( 'frontend', __name__,
                static_folder='static',
                template_folder='templates',
                url_prefix='/labormarketvis' )

# parameters ------------------------------
hr_range = 10
dataset = 'dataset/workana.csv'
# ------------------------------ parameters

metadata = {}
df = {}
skip_col = [ 'name', 'country', 'rating', 'hourly_rate', 'project_completed', 'hours_worked']

def round_up(x, divisor):
    return int(math.ceil(x / divisor)) * divisor

def round_down(x, divisor):
    return x - (x%divisor)

def is_numeric( x ):
    if( str(x).isnumeric() ): return True
    else: return False

# index page
@bp.route('/')
def homePage():
    global df

    title = "WORKANA Analysis"
    paragraph = "This is the analytic result toward the 'Freelancer' section of the website WORKANA."

    df = pd.read_csv( dataset )
    # delete non-numeric data row
    df['hourly_rate'] = pd.to_numeric( df['hourly_rate'], errors='coerce' )

    metadata[ "total_person" ] = len( df.index )
    metadata[ "avg_hourly_r" ] = df[ 'hourly_rate' ].mean()
    metadata[ 'max_hr' ] = df[ 'hourly_rate' ].max()
    # the group of the max_hr
    metadata[ 'max_hr_g_top' ] = round_up( df[ 'hourly_rate' ].max(), 10 )
    metadata[ 'hr_range' ] = hr_range
    metadata[ 'max_hr_country' ] = df.loc[df['hourly_rate'].idxmax()][ 'country' ]
    # calculate the country distribution
    d = df.groupby( 'country' ).groups
    # nationality distribution
    # country_dist = {}
    country_dist = []
    # country hourly rate avg.
    country_avg = {}
    max_country = ( "", 0 )
    for k in d:
        v = int(len( d[ k ] ))
        # country_dist[ k ] = v
        country_dist.append( { 'label': k, 'value': v } )
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

# about page
@bp.route('/about')
@bp.route('/about.html')
def aboutPage():
    title = "About this site"
    paragraph = "UN Webscraping"

    return render_template("index.html", title=title, paragraph=paragraph, pageType='about')


### data APIs --------------------------------------------------
# hourly rate by country
@bp.route( '/_country_hr_dist' )
def countryDetail():
    global df
    nation_df = df[(df['country'] == request.args.get('country', '', type=str))]
    data = {}
    result = []

    for i, r in nation_df.iterrows():
        hr = r[ 'hourly_rate' ]
        if( pd.isnull(hr) ):
            if( 'N/A' not in data ): data[ 'N/A' ] = 1
            else: data[ 'N/A' ] += 1
        else:
            low = int(round_down( hr, 10 ))
            high = int(round_up( hr, 10 ))
            k = str(low) + '-' + str(high)
            if( k not in data ): data[ k ] = 1
            else: data[ k ] += 1

    for k in data.keys():
        result.append( { "name": k, "val": data[ k ] } )

    return jsonify( result )

# hourly rate with skills by country
@bp.route( '/_country_hr_skills' )
def countryHRSkills():
    global df
    global metadata
    global skip_col

    d = df.groupby( 'country' ).groups

    nation_df = None

    opt = request.args.get('option', 'default', type=str)

    result = {}
    count = {}
    for k in d:
        # change the nation_df based on condition
        if( 'Latin America' in opt ):
            # above Latin America average
            nation_df = df[(df['country'] == k) & (df['hourly_rate'] > metadata[ "avg_hourly_r" ])]
        elif( 'Country' in opt ):
            nation_df = df[(df['country'] == k) & (df['hourly_rate'] > metadata[ "country_avg" ][ k ])]
        else:
            tmp = opt.split( '-' )
            nation_df = df[(df['country'] == k) & (df['hourly_rate'] >= int(tmp[0])) & (df['hourly_rate'] < int(tmp[1]))]

        count[ k ] = len(nation_df)
        if( nation_df.empty ):
            result[ k ] = [{ "name": "NO DATA!", "val": 10 }]
        else:
            for c in nation_df:
                # skip the non-skill col.
                if( c in skip_col ): continue
                if( not (nation_df[c] == 1).any() ): continue
                # ref. https://datascience.stackexchange.com/questions/29671/how-to-count-occurrences-of-values-within-specific-range-by-row
                e = { "name": c, "val": int((nation_df[c] == 1).sum()) }
                if( k not in result ): result[ k ] = [ e ]
                else: result[ k ].append( e )
    return jsonify( { "r": result, "c": count } )

# plot example
# ref: https://fionahurley.wordpress.com/2015/11/13/generating-a-correlation-coefficient/
# flask render
# ref: https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
# ref: http://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask013.html
@bp.route( '/_hr_v_pc' )
def HRvsPC():
# def create_plot():

    tmp_df = df[['hourly_rate', 'project_completed']].copy()
    # clear the data with empty value
    # axis: 0 for rows, axis: 1 for columns
    tmp_df = tmp_df.dropna( axis=0, how='any' )

    plt.figure(figsize=(6, 10))
    plt.subplot( 211 )
    # plot
    scat1 = seaborn.regplot(x="hourly_rate", y="project_completed", data=tmp_df)
    plt.xlabel( 'Hourly Rate Required' )
    plt.ylabel( 'Num. of Project a Seeker Completed' )
    plt.title('Hourly Rate vs. Num. of Projects Completed')

    tmp_df = df[['hourly_rate', 'hours_worked']].copy()
    # clear the data with empty value
    # axis: 0 for rows, axis: 1 for columns
    tmp_df = tmp_df.dropna( axis=0, how='any' )

    plt.subplot( 212 )
    # plot
    scat1 = seaborn.regplot(x="hourly_rate", y="hours_worked", data=tmp_df)
    plt.xlabel( 'Hourly Rate Required' )
    plt.ylabel( 'Num. of Hours a Seeker Worked' )
    plt.title('Hourly Rate vs. Num. of Hours Worked')

    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)

    return Response(figfile.getvalue(), mimetype='image/png')
### -------------------------------------------------- data APIs

app.register_blueprint( bp )

# the main function
if __name__ == "__main__":
	app.run(
        debug=False,
        host='0.0.0.0',
        port=8804,
        passthrough_errors=True )