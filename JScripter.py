import argparse
import requests
from bs4 import BeautifulSoup
import os
import hashlib
import subprocess
import sys
import json
from datetime import datetime
from colorama import Fore, Style, init
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

ASCII_ART = r"""
   ________  ________  ________  ________ 
  ╱    ╱   ╲╱        ╲╱    ╱   ╲╱    ╱   ╲
 ╱         ╱         ╱         ╱         ╱
╱             JScripter       ╱ 
╲__╱_____╱╲___╱____╱  ╲______╱╲__╱_____╱  
This tool is intended only for educational purposes and for testing in
corporate environments. https://twitter.com/nav1n0x/ and https://github.com/ifconfig-me take
no responsibility for the misuse of this code. Use it at your own risk.
Do not attack a target you don't have permission to engage with.
"""

def print_banner():
    print(Fore.CYAN + ASCII_ART + Style.RESET_ALL)

def get_js_urls(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching {page_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    js_urls = [script['src'] for script in soup.find_all('script') if script.get('src')]
    return js_urls

def download_js_file(js_url, save_dir, silent):
    try:
        response = requests.get(js_url)
        response.raise_for_status()
    except requests.RequestException as e:
        if not silent:
            print(f"{Fore.RED}Error downloading {js_url}: {e}")
        return None

    js_content = response.content
    js_hash = hashlib.sha256(js_content).hexdigest()

    save_path = os.path.join(save_dir, f"{js_hash}.js")
    if not os.path.exists(save_path):
        with open(save_path, 'wb') as file:
            file.write(js_content)
        if not silent:
            print(f"{Fore.GREEN}[+] JavaScript file saved: {save_path}")
        return js_hash
    else:
        if not silent:
            print(f"{Fore.YELLOW}Duplicate JavaScript file: {js_url}")
        return None

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Fore.RED}Command failed: {command}\nError: {result.stderr}")
    return result.stdout.strip()

def process_url(url, save_dir, silent):
    js_urls = set()
    if not silent:
        print(f"{Fore.CYAN}[*] Running GAU on {url}")
    gau_output = run_command(f"echo {url} | gau | grep -iE '\\.js$' | sort -u")
    gau_js_urls = gau_output.splitlines()
    js_urls.update(gau_js_urls)
    
    if not silent:
        print(f"{Fore.GREEN}[+] GAU found {len(gau_js_urls)} scripts!")

    if not silent:
        print(f"{Fore.CYAN}[*] Running hakrawler on {url}")
    hakrawler_output = run_command(f"hakrawler -js -url {url} -plain -depth 2 -scope strict -insecure | grep -iE '\\.js$' | sort -u")
    hakrawler_js_urls = hakrawler_output.splitlines()
    js_urls.update(hakrawler_js_urls)

    if not silent:
        print(f"{Fore.GREEN}[+] HAKRAWLER found {len(hakrawler_js_urls)} scripts!")

    downloaded_hashes = set()
    for js_url in js_urls:
        js_hash = download_js_file(js_url, save_dir, silent)
        if js_hash:
            downloaded_hashes.add(js_hash)

    return downloaded_hashes

def process_urls(urls, save_dir, silent, max_threads):
    all_js_hashes = set()
    start_time = datetime.now()
    total_urls = len(urls)

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(process_url, url, save_dir, silent): url for url in urls}
        for idx, future in enumerate(as_completed(futures), 1):
            url = futures[future]
            try:
                js_hashes = future.result()
                all_js_hashes.update(js_hashes)
            except Exception as e:
                print(f"{Fore.RED}Error processing {url}: {e}")
            
            elapsed_time = datetime.now() - start_time
            avg_time_per_url = elapsed_time / idx
            remaining_time = avg_time_per_url * (total_urls - idx)
            print(f"{Fore.BLUE}Processed URLs: {idx}/{total_urls}")
            print(f"{Fore.BLUE}Elapsed Time: {elapsed_time}")
            print(f"{Fore.BLUE}Approx Time Remaining: {remaining_time}")

    if not silent:
        print(f"{Fore.GREEN}[+] All Done!")
        print(f"{Fore.GREEN}[+] Found total of {len(all_js_hashes)} unique scripts!")

def main(url_file, single_url, save_dir, silent, max_threads):
    os.makedirs(save_dir, exist_ok=True)
    urls = []

    if url_file:
        with open(url_file, 'r') as file:
            urls = file.read().splitlines()
    elif single_url:
        urls = [single_url]

    if not urls:
        print(f"{Fore.RED}No URLs provided. Please use -f to provide a list or -u to provide a single URL.")
        sys.exit(1)

    if not silent:
        print_banner()

    process_urls(urls, save_dir, silent, max_threads)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape and save unique JavaScript files.")
    parser.add_argument("-f", "--file", help="File containing list of target URLs.")
    parser.add_argument("-u", "--url", help="Single target URL.")
    parser.add_argument("-d", "--directory", required=True, help="Directory to save unique JavaScript files.")
    parser.add_argument("-s", "--silent", action="store_true", help="Silent mode. No banner, no progress, only URLs.")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads to use for concurrent processing.")

    args = parser.parse_args()

    if not args.file and not args.url:
        print(f"{Fore.RED}You must provide either a file with URLs (-f) or a single URL (-u).")
        sys.exit(1)

    main(args.file, args.url, args.directory, args.silent, args.threads)
