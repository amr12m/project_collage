import os
import time
import datetime


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
def subdomain_enum(subdomain_name):

    file_path = create_or_append_to_domain_directory(subdomain_name)
    com = f"subfinder -silent -d {subdomain_name}>>{subdomain}_subdomain_enum.txt"
    output = run_commend(com)
    run_commend(f"mv {subdomain}_subdomain_enum.txt {file_path}")

while True:

    subdomain_name =input("Enter the domain: ")
    subdomain = subdomain_name.split('.')[0]
    # check that input is entered
    if is_domain_format(subdomain_name) is True:
        subdomain_enum(subdomain_name)
        break
    else:
        print("please enter vaild domain name ex:'example.com' or 'example.co.io")

    # make param to out of while
        


    


