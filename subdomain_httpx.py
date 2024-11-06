import os
import time
import datetime
import re

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

def httpx_fun(file_path,subdomain):
    
    com = f"httpx -l {file_path}/{subdomain}_subdomain_enum.txt -mc 200,302,301 -silent  >>live_subdomain_enum.txt"
    output = run_commend(com)
    run_commend(f"mv live_subdomain_enum.txt {file_path}")

# subfinder --> example_subdomain_enum.txt --> httpx --> live_subdomain_enum.txt

while True:

    subdomain_name =input("Enter the domain: ")
    subdomain = subdomain_name.split('.')[0]
    file_path = create_or_append_to_domain_directory(subdomain_name)
    # check that input is entered
    if is_domain_format(subdomain_name) is True:
        subdomain_enum(subdomain_name,subdomain,file_path)
        #print(file_path+'/example_subdomain_enum.txt')
        httpx_fun(file_path,subdomain)
        break
    else:
        print("please enter vaild domain name ex:'example.com' or 'example.co.io")
    
    # make param to out of while
        


    
