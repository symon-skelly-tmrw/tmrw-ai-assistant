import requests
import re

def find_js_file_url(main_page_url):
    # Step 1: Fetch the main page HTML
    response = requests.get(main_page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve main page: {response.status_code}")
        return None

    match = re.search(r'(/_next/static/chunks/pages/_app-[^"]+\.js)', response.text)
    if match:
        js_file_url = main_page_url.split('/login')[0] + match.group(1)
        print("Found JS file URL:", js_file_url)
        return js_file_url
    else:
        print("JavaScript file URL with pattern '/next/static/chunks/pages/_app-' not found.")
        return None

def fetch_specific_api_url(js_file_url):
    response = requests.get(js_file_url)
    if response.status_code != 200:
        print(f"Failed to retrieve JS file: {response.status_code}")
        return None

    # Search for the URL following `httpUrl:`
    match = re.search(r'httpUrl:\s*"([^"]+)"', response.text)
    if match:
        found_url = match.group(1)
        print("Found httpUrl:", found_url)
        return found_url
    else:
        print("httpUrl not found in the JS file.")
        return None

def get_api_url(base_url: str):
    main_page_url = base_url + "/login"
    js_file_url = find_js_file_url(main_page_url)
    if js_file_url:
        api_url = fetch_specific_api_url(js_file_url)
        if api_url:
            return api_url

