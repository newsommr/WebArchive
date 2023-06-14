import requests
from bs4 import BeautifulSoup
import os

# Get the URL(s) or filename from the user
user_input = input("Please enter the URL(s) you wish to archive (separated by commas), or the path to a text file: ")

urls = []
if os.path.isfile(user_input):
    # User input is a file
    with open(user_input, 'r') as f:
        urls = [line.strip() for line in f]
else:
    # Assume user input is a list of URLs separated by commas
    urls = user_input.split(',')

print(urls)

# For the curl command
url1 = 'https://web.archive.org/save'
url2 = 'https://archive.is/submit/'

headers = {
    'Accept': 'application/json',
    'Authorization': 'LOW nyy6S67AkkZuNMm0:dUrK6W4m0HXZM6Mg',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

# Check if the output file exists, create it if not
if not os.path.exists('output.txt'):
    with open('output.txt', 'w') as f:
        f.write('')

# Read the content of the output file
with open('output.txt', 'r') as f:
    output_content = f.read()

# Open the output file for appending
with open('output.txt', 'a') as f:
    # Send a request for each URL
    for user_url in urls:
        # Check if the URL information has already been written to the file
        if user_url.strip() in output_content:
            print(f'Information for {user_url.strip()} already exists in output.txt')
            continue

        data = {
            'url': user_url.strip(),
        }
        
        # Fetch the page
        response0 = requests.get(user_url.strip(), headers=headers)
        soup = BeautifulSoup(response0.content, 'html.parser')
        page_title = soup.title.string if soup.title else 'No title found'

        # Post request to web.archive.org
        print("Wayback Machine: ")
        response1 = requests.post(url1, headers=headers, data=data)
        
        if 'json' in response1.headers.get('Content-Type'):
            json_response1 = response1.json()
            print(json_response1.get('message', 'Done')) 
            wayback_url = f"https://web.archive.org/web/{user_url}"
        else:
            print(response1.text)
            wayback_url = ''

        # Get request to archive.is
        print("Archive.md: ")
        user_url_encoded = requests.utils.quote(user_url.strip(), safe='')
        response2 = requests.get(f"{url2}?url={user_url_encoded}", headers=headers)
        
        if response2.status_code == 200:
            print("Done")
        else:
            print("Possible error")
        
        # Write the URL, title, and archived URLs to the file
        f.write(f'Title: {page_title}\n')
        f.write(f'Original URL: {user_url.strip()}\n')
        f.write(f'Archive.is URL: https://archive.is/newest/{user_url_encoded}\n')
        f.write(f'Wayback Machine URL: {wayback_url}\n')
        f.write('\n')