import os
import sys
import requests
import hashlib
import json
from pathlib import Path

previous_hash_file = 'previous.hash'
previous_hashes = {}
current_hashes = {}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def load_previous_hashes():
    global previous_hashes
    try:
        with open(previous_hash_file) as json_file:
            previous_hashes = json.load(json_file)
    except FileNotFoundError as e:
        Path(previous_hash_file).touch()
    except UnicodeDecodeError as e:
        sys.exit('Invalid previous hash file detected. Exiting...')
    except json.decoder.JSONDecodeError as e:
        sys.exit('Malformed hash file detected. Exiting...')

def write_current_hashes():
    with open(previous_hash_file, 'w') as outfile:
        json.dump(current_hashes, outfile)

def hash_urls(urls):
    for page_url in urls:
        current_hashes[page_url] = hash_page_url(page_url)

def hash_page_url(page_url):
    r = requests.get(page_url)
    m = hashlib.md5()
    m.update(r.content)
    page_url_hash = m.hexdigest()
    
    return page_url_hash

def check_for_changes():
    detected_changes = False
    for page_url in current_hashes:
        print(f'{bcolors.BOLD}Checking ' + page_url + f'...{bcolors.ENDC}')
        if page_url in previous_hashes:
            if current_hashes[page_url] != previous_hashes[page_url]:
                detected_changes = True
                print(f'\t{bcolors.OKGREEN}Change detected!{bcolors.ENDC}')
            else:
                print(f'\t{bcolors.OKBLUE}No Change{bcolors.ENDC}')
        else:
            print(f'\t{bcolors.WARNING}Page checked for first time.{bcolors.ENDC}')
    
    if not detected_changes:
            print(f'\n{bcolors.HEADER}No changes detected at this time.{bcolors.ENDC}')

def main():
    load_previous_hashes()

    urls = [
        "https://www.lopp.net/bitcoin-information/getting-started.html",
        "https://aantonop.com/books/",
        "https://www.freebsd.org/news/",
    ]
 
    hash_urls(urls)
    check_for_changes()
    write_current_hashes()

main()
