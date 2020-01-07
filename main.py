import sys
import requests
import hashlib
import json
from pathlib import Path

url_file = 'urls.json'
previous_hash_file = 'previous.json'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def load_urls():
    try:
        with open(url_file) as json_file:
            urls = json.load(json_file)
    except FileNotFoundError:
        Path(url_file).touch()
    except UnicodeDecodeError:
        sys.exit('Invalid URL file detected. Exiting...')
    except json.decoder.JSONDecodeError:
        sys.exit(f'{bcolors.HEADER}Malformed URL file detected. Add some URLS first...{bcolors.ENDC}')
    else:
        return urls

def load_previous_hashes():
    previous_hashes = {}
    try:
        with open(previous_hash_file) as json_file:
            previous_hashes = json.load(json_file)
    except FileNotFoundError:
        Path(previous_hash_file).touch()
    except UnicodeDecodeError:
        sys.exit('Invalid previous hash file detected. Exiting...')
    except json.decoder.JSONDecodeError:
        pass
    finally:
        return previous_hashes

def hash_urls(urls):
    current_hashes = {}
    for page_url in urls:
        current_hashes[page_url] = hash_page_url(page_url)
    return current_hashes

def hash_page_url(page_url):
    r = requests.get(page_url)
    m = hashlib.md5()
    m.update(r.content)
    page_url_hash = m.hexdigest()
    
    return page_url_hash

def check_for_changes(current_hashes, previous_hashes):
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

def write_current_hashes(current_hashes):
    with open(previous_hash_file, 'w') as outfile:
        json.dump(current_hashes, outfile)

def main(): 
    urls = load_urls()
    if urls:
        previous_hashes = load_previous_hashes()
        current_hashes = hash_urls(urls)
        check_for_changes(current_hashes, previous_hashes)
        write_current_hashes(current_hashes)
    else:
        print(f'{bcolors.WARNING}Add some URLS in urls.json first.{bcolors.ENDC}')

main()
