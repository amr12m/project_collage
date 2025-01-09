import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

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

        print(f"\n[FORM {i}] URL: {form_url}")
        print(f"[FORM {i}] Method: {method.upper()}")
        print(f"[FORM {i}] Found Parameters: {form_params}")

if __name__ == "__main__":
    choice = input("Do you want to provide a single URL or a file containing URLs? (single/file): ").strip().lower()

    if choice == "single":
        target_url = input("Enter the URL to be tested: ").strip()
        process_url(target_url)
    elif choice == "file":
        file_path = input("Enter the file path containing URLs: ").strip()
        try:
            with open(file_path, 'r') as file:
                urls = file.readlines()
                for url in urls:
                    process_url(url.strip())
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
        except Exception as e:
            print(f"[ERROR] An error occurred while reading the file: {e}")
    else:
        print("[ERROR] Invalid choice. Please select 'single' or 'file'.")
