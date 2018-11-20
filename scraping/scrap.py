from bs4 import BeautifulSoup
import requests

# parameters -------------------------------------------------------
target_class = 'js-worker'      # the frame containing worker info.
country_element = 'span'        # the element containing nationality
country_class = 'country-name'
rating_element = 'span'         # the element containing rating
rating_class = 'stars-bg'
pro_element = 'span'            # the element containing pro tag
pro_class = 'pro-label'
hrrate_element = 'span'         # the element containing hr_rate
hrrate_class = 'monetary-amount'
experience_element = 'p'        # the element containing experience info.
experience_class = 'hidden-xs'
skill_element = 'a'             # the element containing skills
skill_class = 'skill'

result_file = './result.csv'

# csv header
header = 'name,country,is_pro,rating,hourly_rate,completed_jobs,hours_worked,skills'
# the website url
base_url = 'https://www.workana.com/en/freelancers?page='
# a very large number
limit = 100
# ------------------------------------------------------- parameters

# self-defined functions -------------------------------------------
def invalid_val(): return 'N/A'
# make sure there is no special char in a value
def clear_str( text ):
    text = str(text).replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' )
    return text
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

# file output
f = open( result_file, 'w' )
f.write( header )
f.write( '\n' )

# there are pages to show the result
for i in range( 1, (limit + 1) ):
    url = base_url + str(i)
    # get web code
    r = requests.get( url )

    # Beautiful Soup parser
    soup = BeautifulSoup( r.text, 'html.parser' )

    t = soup.find_all( 'div', class_=target_class )
    # if the result is empty
    if( len( t ) == 0 ): break

    for workers in t:
        row = ''
        soup = BeautifulSoup( str(workers), 'html.parser' )

        # get the name of the applicant
        for e in soup.find_all( 'span' ):
            if( e.parent.name == 'a' and e.parent.parent.name == 'h3' ):
                row += clear_str( e.text ) + ','
                continue # only one element will contain this information

        # get the nationality of the applicant
        e = soup.find( country_element, class_=country_class )
        # temporary soup parser
        t_soup = BeautifulSoup( str(e), 'html.parser' )
        e = t_soup.find( 'a' )
        row += clear_str( e.text ) + ','

        # rating
        e = soup.find( rating_element, class_=rating_class )
        res =  str(e[ 'title' ]).replace( ' of 5.00', '' )
        res = clear_str( res )
        res = float(res)
        row += clear_str( res ) + ','

        # if this applicant is tagged as 'pro'
        e = soup.find( pro_element, class_=pro_class )
        if( e == None ): row += str(0) + ','
        else: row += str(1) + ','

        # find hourly rate
        e = soup.find( hrrate_element, class_=hrrate_class )
        if( e == None ): row += invalid_val() + ','
        else: row += numeric( e[ 'data-amount' ], type='float' ) + ','

        # get the completed_jobs & hours_worked
        e = soup.find( experience_element, class_=experience_class )
        # temporary soup parser
        t_soup = BeautifulSoup( str(e), 'html.parser' )
        for e in t_soup.find_all( 'span' ):
            res = ''
            try:  # make sure the soup find the element
                # remove the text heading
                res = str(e.text).replace( 'Completed projects: ', '' ).replace( 'Hours worked in hourly projects: ', '' )
                res = numeric( res, type='int' )
            except: res = invalid_val()
            row += res + ','

        # get all the skills the applicant has
        skills = []
        e = soup.find_all( skill_element, class_=skill_class )
        for s in e: skills.append( s.text )
        skills = "|".join( skills )
        row += skills

        # commit the result
        f.write( str(row.encode( 'utf-8' )) )
        f.write( '\n' )
# safely close the file
f.close()