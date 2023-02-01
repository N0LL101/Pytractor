from requests import get
from bs4 import BeautifulSoup
import re
from json import loads
import urllib.request
import os
from urllib.parse import urlparse

def design():
    # clearing terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    ____        _                  _             
 |  _ \ _   _| |_ _ __ __ _  ___| |_ ___  _ __ 
 | |_) | | | | __| '__/ _` |/ __| __/ _ \| '__|
 |  __/| |_| | |_| | | (_| | (__| || (_) | |   
 |_|    \__, |\__|_|  \__,_|\___|\__\___/|_|   
        |___/                                  
        
        Coded BY : Ziead Ebrahim
    """)


def choose():
    ch = eval(input("""

    1) Robots.txt

    2) JS files

    3) Page source 

    4) waybackurl
    
    5) VirusTotal
    
    6) ALL

    Enter the Choose : """))
    return ch


def is_valid_url(url):
    regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None




def robots(url):
    if "robots.txt" in url:
        pass
    else:
        url = base_url + "/robots.txt"

    with urllib.request.urlopen(url) as result:
        page = result.read().decode('utf-8')


    paths = re.findall("\/\/?.*", page)
    for path in paths:
        print(url+path)








def js_files(url):
    # Fetch the HTML content
    response = get(url)
    html_content = response.text

    # Extract the URLs of the JavaScript files
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the URLs of the JavaScript files
    js_files = [script.get('src') for script in soup.find_all('script') if
                script.get('src') and '.js' in script.get('src')]

    for i in js_files:
        print(i)



links = []
def page_source(url):
    response = get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('script'):
        if link.get('src'):
            links.append(link.get('src'))

    for link in soup.find_all('link'):
        if link.get('href'):
            links.append(link.get('href'))

    for link in soup.find_all('a'):
        if link.get('href'):
            links.append(link.get('href'))

    for i in links:
        if is_valid_url(i):
            print(i)
        else:
            print(url+i)

def web_arch(url):
    try:

        x = loads(
            get("https://web.archive.org/cdx/search?url=" + url + "%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=100000&_=1547318148315").text)

        for i in x:
            print(i[0])
    except:
        pass
def virus_total(url):
    api_key="a95257d54fb4d08d1d9db3dbde92a7129b7f4736ec8223296367e0cd6cc198e7"

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]

    req = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains?apikey={api_key}"
    header ={
        "X-Apikey":api_key
    }
    response = get(req,headers=header)

    if response.status_code == 200:
        data = loads(response.text)
        subdomains = [subdomain['id'] for subdomain in data['data']]
        for i in subdomains:
            print(i)

    else:
        print("Failed to retrieve subdomains.")

if __name__ == '__main__':
    design()
    url = input("enter the url with (http/s) : ").lower()


    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc



    x = choose()
    if is_valid_url(url):
        if x == 1:
            robots(base_url)
        elif  x == 2:
            js_files(url)
        elif x == 3:
            page_source(url)

        elif x ==4:
            web_arch(url)

        elif x ==5:
            virus_total(url)
        elif x == 6:
            robots(base_url)
            js_files(url)
            page_source(url)
        else:
            print("please Enter correcr value : ")
            exit()
    else:
        url = input("please enter the url with (http/s) : ").lower()



