import os
import time
import datetime
import re

import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from fuzzer import main

def fetch_forms(url):
    """Fetch forms from the target webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        return forms
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch forms: {e}")
        return []

def parse_form(form):
    """Parse a form to extract its inputs."""
    action = form.get('action') or ""
    method = form.get('method', 'get').lower()
    inputs = form.find_all('input')
    form_params = []

    for input_tag in inputs:
        name = input_tag.get('name')
        if name:
            form_params.append(name)

    return action, method, form_params

def fetch_url_params(url):
    """Fetch parameters included in the URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return list(query_params.keys()), query_params

def construct_get_url(url, params):
    """Construct a URL with its GET parameters."""
    parsed_url = urlparse(url)
    query_string = urlencode(params, doseq=True)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query_string, parsed_url.fragment))
    return new_url

def process_url(url):
    """Process a single URL to fetch and display parameters and forms."""
    print(f"\nTesting URL: {url}\n")

    # Fetch parameters from the URL
    url_params, param_values = fetch_url_params(url)
    if url_params:
        full_url = construct_get_url(url, param_values)
        print(f"{{{full_url}}}")
    else:
        print("[INFO] No URL parameters found.")

    # Fetch and parse forms
    forms = fetch_forms(url)
    if not forms:
        print("[INFO] No forms found on the page.")
        return

    print(f"[INFO] Found {len(forms)} form(s) on the page.")

    for i, form in enumerate(forms, 1):
        action, method, form_params = parse_form(form)
        form_url = action if action.startswith('http') else url + action
        print(method.upper())
        if method.upper() == "GET":
            for y in form_params:
                get_method_param = form_url + '?' + y + '='
                with open('Get_param.txt','a') as f:
                    f.write(get_method_param +'\n')
        elif method.upper() == "POST":
            #post_method = form_url , form_params
            #rint(post_method)
            with open('POST_method_param.txt','a') as f:
                     f.write(form_url +','+ str(form_params) +'\n')

def run_commend(commend):
    com = os.system(commend)
    return com

def log(message):
    """Log messages with timestamps."""
    print(f"{datetime.datetime.now()} - {message}")

# check the valid domain fun
def is_domain_format(input_string):
    if not input_string:
        return False

    # Regular expression pattern for domain with TLD
    pattern = r"^[a-zA-Z0-9-]+\.+[a-zA-Z]{2,}$"
    
    # Check if the input string matches the domain format
    return bool(re.match(pattern, input_string))

def create_or_append_to_domain_directory(domain_name):

    # Get the absolute path of the directory
    directory_path = os.path.abspath(domain_name)

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory path is: {directory_path}")

    return directory_path

# func for subdomain enum
def subdomain_enum(subdomain_name,subdomain,file_path):

    print(file_path+'/example_subdomain_enum.txt')
    com = f"subfinder -silent -d {subdomain_name}>>{subdomain}_subdomain_enum.txt"
    output = run_commend(com)
    run_commend(f"mv {subdomain}_subdomain_enum.txt {file_path}")

# httpx function -> get the urls with code 200,301,302 : https://github.com/projectdiscovery/httpx
def httpx_fun(file_path,subdomain):
    
    com = f"httpx -l {file_path}/{subdomain}_subdomain_enum.txt -mc 200,302,301 -silent  >>live_subdomain_enum.txt"
    output = run_commend(com)
    run_commend(f"mv live_subdomain_enum.txt {file_path}")

# subfinder --> example_subdomain_enum.txt --> httpx --> live_subdomain_enum.txt

# katana function--> it's crawling tool : https://github.com/projectdiscovery/katana
def katana_fun(file_path):
    com = f"katana -u {file_path}/live_subdomain_enum.txt -silent -fx >> crawlling_output.txt"
    output = run_commend(com)
    run_commend(f"mv crawlling_output.txt {file_path}")

# subzy function --> testing subdomain take over
def subzy_fun(file_pass):
    com = f"subzy run --targets {file_path}/live_subdomain_enum.txt --hide_fails --vuln --concurrency 100 | grep -v -E 'Akamai|xyz|available|-' >> subdomain_takeover_report.txt"
    output = run_commend(com)
    run_commend(f"mv subdomain_takeover_report.txt {file_path}")

# finding parameter function
def finding_param_fun(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            for url in urls:
                 process_url(url.strip())
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] An error occurred while reading the file: {e}") 

# Fuzzing function
def fuzzing_fun(domain_name):
    com = f'python fuzzer.py "ffuf -w ./fuzz.txt -u http://{domain_name}/FUZZ"'
    output = run_commend(com)
    run_commend(f"mv {file_path}/fuzz.txt {file_path}")


# ffuf func ---> to do []

while True:

    subdomain_name =input("Enter the domain: ")
    subdomain = subdomain_name.split('.')[0]
    file_path = create_or_append_to_domain_directory(subdomain_name)
    # check that input is entered
    if is_domain_format(subdomain_name) is True:
        subdomain_enum(subdomain_name,subdomain,file_path)
        httpx_fun(file_path,subdomain)
        subzy_fun(file_path)
        katana_fun(file_path)
        finding_param_fun(f"{file_path}/crawlling_output.txt")
        # amass_fun(file_path, subdomain)
        fuzzing_fun(subdomain_name)


        break
    else:
        print("please enter valid domain name ex:'example.com' or 'example.co.io")
    
    # make param to out of while
        

