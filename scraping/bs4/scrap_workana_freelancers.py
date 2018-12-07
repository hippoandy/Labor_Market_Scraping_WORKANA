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
header = 'name,country,rating,is_pro,hourly_rate,completed_jobs,hours_worked,skills'
# the website url
base_url = 'https://www.workana.com/en/freelancers?page='
# a large number to cover all the page number
limit = 100
# ------------------------------------------------------- parameters

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

# file output
f = open( result_file, 'w' )
f.write( header + '\n' )

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
        soup = BeautifulSoup( str(workers), 'html.parser' )

        # get the name of the applicant
        name = ''
        for e in soup.find_all( 'span' ):
            if( e.parent.name == 'a' and e.parent.parent.name == 'h3' ):
                name = clear_str( e.text )
                continue # only one element will contain this information

        # get the nationality of the applicant
        e = soup.find( country_element, class_=country_class )
        # temporary soup parser
        t_soup = BeautifulSoup( str(e), 'html.parser' )
        e = t_soup.find( 'a' )
        country = clear_str( e.text )

        # rating
        e = soup.find( rating_element, class_=rating_class )
        res =  str(e[ 'title' ]).replace( ' of 5.00', '' )
        res = clear_str( res )
        res = float(res)
        rating = clear_str( res )

        # if this applicant is tagged as 'pro'
        e = soup.find( pro_element, class_=pro_class )
        is_pro = 0
        if( e != None ): is_pro = 1

        # find hourly rate
        e = soup.find( hrrate_element, class_=hrrate_class )
        hourly_rate = invalid_val()
        if( e != None ): hourly_rate = numeric( e[ 'data-amount' ], type='float' )

        # get the completed_jobs & hours_worked
        e = soup.find( experience_element, class_=experience_class )
        # temporary soup parser
        t_soup = BeautifulSoup( str(e), 'html.parser' )
        projects = hours = invalid_val()
        for e in t_soup.find_all( 'span' ):
            res = ''
            try:  # make sure the soup find the element
                # remove the text heading

                if( 'Completed' in e.text ): projects = numeric( str(e.text).replace( 'Completed projects: ', '' ), type='int' )
                else: hours = numeric( str(e.text).replace( 'Hours worked in hourly projects: ', '' ), type='int' )
            except: pass

        # get all the skills the applicant has
        skills = []
        e = soup.find_all( skill_element, class_=skill_class )
        for s in e:
            res = clear_comma( str(s.text).encode( 'ascii', 'ignore' ) )
            skills.append( res )
        skills = "|".join( skills )

        # commit the result
        f.write( '{},{},{},{},{},{},{},{}\n'.format( name, country, rating, is_pro, hourly_rate, projects, hours, skills ) )
# safely close the file
f.close()