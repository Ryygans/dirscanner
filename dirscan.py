#!/usr/bin/env python3
import requests
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def scan_url(target_url, path):
    url = target_url.rstrip("/") + "/" + path.strip("/")
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return f"{GREEN}[200 OK]{RESET} {url}"
        elif r.status_code in [301, 302]:
            return f"{YELLOW}[{r.status_code} REDIRECT]{RESET} {url}"
        elif r.status_code == 403:
            return f"{RED}[403 FORBIDDEN]{RESET} {url}"
    except requests.RequestException:
        pass
    return None

def dir_bruteforce(target_url, wordlist, threads):
    try:
        with open(wordlist, "r") as f:
            dirlist = f.read().splitlines()
    except FileNotFoundError:
        print(f"{RED}[!] Wordlist '{wordlist}' not found.{RESET}")
        sys.exit(1)

    ascii_art = GREEN + r"""
                 __  __             ______                                                              
      /  |/  |           /      \                                                             
  ____$$ |$$/   ______  /$$$$$$  |  _______   ______   _______   _______    ______    ______  
 /    $$ |/  | /      \ $$ \__$$/  /       | /      \ /       \ /       \  /      \  /      \ 
/$$$$$$$ |$$ |/$$$$$$  |$$      \ /$$$$$$$/  $$$$$$  |$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
$$ |  $$ |$$ |$$ |  $$/  $$$$$$  |$$ |       /    $$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
$$ \__$$ |$$ |$$ |      /  \__$$ |$$ \_____ /$$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$/ $$ |      
$$    $$ |$$ |$$ |      $$    $$/ $$       |$$    $$ |$$ |  $$ |$$ |  $$ |$$       |$$ |      
 $$$$$$$/ $$/ $$/        $$$$$$/   $$$$$$$/  $$$$$$$/ $$/   $$/ $$/   $$/  $$$$$$$/ $$/       
                                                                                            
""" + RESET

    print(ascii_art)
    print(f"{CYAN}Powered By Ryygans{RESET}")
    print(f"{CYAN}github: https://github.com/ryygans{RESET}\n")
    print(f"[+] Start Scanning {target_url} with {len(dirlist)} words (threads={threads})...\n")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_url, target_url, d): d for d in dirlist}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Directory Scanner (Python)")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Threads count")
    args = parser.parse_args()
    dir_bruteforce(args.url, args.wordlist, args.threads)
