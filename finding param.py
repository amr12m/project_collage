import requests
import json
from bs4 import BeautifulSoup

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

def main():
    target_url = input("Enter the URL to be tested: ")
    print(f"Testing URL: {target_url}\n")

    # Fetch and parse forms
    forms = fetch_forms(target_url)
    if not forms:
        print("[INFO] No forms found on the page.")
        return

    print(f"[INFO] Found {len(forms)} form(s) on the page.")

    for i, form in enumerate(forms, 1):
        action, method, form_params = parse_form(form)
        form_url = action if action.startswith('http') else target_url + action

        print(f"\n[FORM {i}] URL: {form_url}")
        print(f"[FORM {i}] Method: {method.upper()}")
        print(f"[FORM {i}] Found Parameters: {form_params}")

if __name__ == "__main__":
    main()
