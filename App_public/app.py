import requests
import json
import os
import subprocess, platform
from urllib.parse import urlparse
from datetime import date

from flask import Flask, render_template
app = Flask(__name__, static_folder='static', static_url_path='')

# Thanks for all the code hints Über, could not pull this through otherwise: https://github.com/uber/Python-Sample-Application

with open('config.json') as f:
    config = json.load(f)

with open('results.json') as r:
    result = json.load(r)

def error_http():
    """Check the HTTP errors, return True/False"""
    # Get Scoring uri from config.json file, check for request error
    # Checking only one ML webservice container to save time to avoid Azure web service probe timeout in 31s, sometimes catches, most of times not
    uri1 = config.get('scoring_uri1')      
    try:
        requests.get(uri1)        
    except requests.exceptions.RequestException:
        return True        
    return False

def error_ping():
    """Check the connectivity with ping, return True/False"""
    # Get Hostname from config.json file. Checking only one ML webservice container to save time. Number of pings, for Linux -c, for Windows -n.
    hostname = config.get('hostname')
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + hostname
    need_sh = False if  platform.system().lower()=="windows" else True
    response = subprocess.call(args, shell=need_sh)
    if response == 0:
        return False
    else:
        return True


def headers():
    """Header object for API requests"""    
    return {'Content-Type': 'application/json'}

def get_week():
    """Input ISO Calendar week as ww"""
    return str(date.today().isocalendar()[1])

def get_year():
    """Input ISO Calendar year as yyyy"""
    return str(date.today().isocalendar()[0])

def primary1():
    """Request Primary1 from ML model webservice"""
    # Data to score for Primary1
    data1 = {"data":
            [
                [
                    get_week(),
                    get_year()
                ]
            ]
            }
    # Convert to JSON string
    input_data1 = json.dumps(data1)
    # Get Scoring uri from config.json file, check for request error
    uri1 = config.get('scoring_uri1')
    # Make the request and return Primary1
    resp1 = requests.post(uri1, input_data1, headers=headers())
    #First check if container is online. Then check if response has only one digit and hack trailing \ away, otherwise return two digits.
    if  resp1.status_code != 200:
        return "Larvaus1 sleeping"
    elif resp1.text[18] == "\\":
        return resp1.text[17]
    return resp1.text[17:19]

def primary2():
    """Request Primary2 from ML model webservice"""
    data2 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1()
                ]
            ]
            }
    input_data2 = json.dumps(data2)
    uri2 = config.get('scoring_uri2')
    resp2 = requests.post(uri2, input_data2, headers=headers())
    if  resp2.status_code != 200:
        return "Larvaus2 sleeping"
    elif resp2.text[18] == "\\":
        return resp2.text[17]
    return resp2.text[17:19]

def primary3():
    """Request Primary3 from ML model webservice"""
    data3 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1(),
                    primary2()
                ]
            ]
            }
    input_data3 = json.dumps(data3)
    uri3 = config.get('scoring_uri3')
    resp3 = requests.post(uri3, input_data3, headers=headers())
    if  resp3.status_code != 200:
        return "Larvaus3 sleeping"
    elif resp3.text[18] == "\\":
        return resp3.text[17]
    return resp3.text[17:19]

def primary4():
    """Request Primary4 from ML model webservice"""
    data4 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1(),
                    primary2(),
                    primary3()
                ]
            ]
            }
    input_data4 = json.dumps(data4)
    uri4 = config.get('scoring_uri4')
    resp4 = requests.post(uri4, input_data4, headers=headers())
    if  resp4.status_code != 200:
        return "Larvaus4 sleeping"
    elif resp4.text[18] == "\\":
        return resp4.text[17]
    return resp4.text[17:19]

def primary5():
    """Request Primary5 from ML model webservice"""
    data5 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1(),
                    primary2(),
                    primary3(),
                    primary4()
                ]
            ]
            }
    input_data5 = json.dumps(data5)
    uri5 = config.get('scoring_uri5')
    resp5 = requests.post(uri5, input_data5, headers=headers())
    if  resp5.status_code != 200:
        return "Larvaus5 sleeping"
    elif resp5.text[18] == "\\":
        return resp5.text[17]
    return resp5.text[17:19]

def primary6():
    """Request Primary6 from ML model webservice"""
    data6 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1(),
                    primary2(),
                    primary3(),
                    primary4(),
                    primary5()
                ]
            ]
            }
    input_data6 = json.dumps(data6)
    uri6 = config.get('scoring_uri6')
    resp6 = requests.post(uri6, input_data6, headers=headers())
    if  resp6.status_code != 200:
        return "Larvaus6 sleeping"
    elif resp6.text[18] == "\\":
        return resp6.text[17]
    return resp6.text[17:19]

def primary7():
    """Request Primary7 from ML model webservice"""
    data7 = {"data":
            [
                [
                    get_week(),
                    get_year(),
                    primary1(),
                    primary2(),
                    primary3(),
                    primary4(),
                    primary5(),
                    primary6()
                ]
            ]
            }
    input_data7 = json.dumps(data7)
    uri7 = config.get('scoring_uri7')
    resp7 = requests.post(uri7, input_data7, headers=headers())
    if  resp7.status_code != 200:
        return "Larvaus7 sleeping"
    elif resp7.text[18] == "\\":
        return resp7.text[17]
    return resp7.text[17:19]

@app.route("/", methods=['GET', 'POST'])
def index():
    """Return the index.html or error.html"""
    # If ping error, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)
    if error_ping() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render index.html to introduce Larvaus
        picture = config.get('pic3')
        return render_template('index.html', pic=picture)

# Due to Azure web service probe timeout in 31s if calling all the Primary results, splitting the Primary results to each individual page first
@app.route("/larvaus1/", methods=['GET', 'POST'])
def larvaus1():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus1.html',
            pic=picture,
            round=rnd,
            data=primary1()        
        )

@app.route("/larvaus2/", methods=['GET', 'POST'])
def larvaus2():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus2.html',
            pic=picture,
            round=rnd,
            data=primary2()        
        )

@app.route("/larvaus3/", methods=['GET', 'POST'])
def larvaus3():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus3.html',
            pic=picture,
            round=rnd,
            data=primary3()        
        )

@app.route("/larvaus4/", methods=['GET', 'POST'])
def larvaus4():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus4.html',
            pic=picture,
            round=rnd,
            data=primary4()        
        )

@app.route("/larvaus5/", methods=['GET', 'POST'])
def larvaus5():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus5.html',
            pic=picture,
            round=rnd,
            data=primary5()        
        )

@app.route("/larvaus6/", methods=['GET', 'POST'])
def larvaus6():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus6.html',
            pic=picture,
            round=rnd,
            data=primary6()        
        )

@app.route("/larvaus7/", methods=['GET', 'POST'])
def larvaus7():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        return render_template('larvaus7.html',
            pic=picture,
            round=rnd,
            data=primary7()        
        )

@app.route("/larvaus/", methods=['GET', 'POST'])
def larvaus():
    """Return the results to be shown as webservice output"""
    # If HTTP errors out, render error.html
    picture = config.get('pic2')
    rnd = get_week() + " - " + get_year()
    results = result.get(rnd)    
    if error_http() == True:
        return render_template('error.html', 
        pic=picture, 
        round=rnd,
        data=results
        )
    else:
        # Render larvaus.html
        picture = config.get('pic1')
        rnd = get_week() + " - " + get_year()
        results = primary1() + " - " + primary2() + " - " + primary3() + " - " +primary4() + " - " + primary5() + " - " + primary6() + " - " + primary7()
        return render_template('larvaus.html',
            pic=picture,
            round=rnd,
            data=results        
        )

if __name__ == '__main__':
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=7000)
