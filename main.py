# Importing the required plugins to make our script work
import requests
import time
from colorama                   import init, Fore, Style
import os
import subprocess
import secrets
import random
from pypresence                 import Presence
import threading

# Variables
genStartTime = int(time.time())
locked = 0

def status():
    global locked  # Declare 'locked' as a global variable
    try:
        client_id = "1205602865754677283"
        RPC = Presence(client_id)
        RPC.connect()

        last_clear_time = time.time()

        def update_discord_presence():
            while True:
                RPC.update(
                    large_image="hi",
                    large_text="Discord Promo gen",
                    details=f"Link generated: {locked}",
                    start=int(genStartTime),
                    buttons=[{"label": "Buy Now!", "url": "https://nitroseller0.mysellix.io"}]
                )
                time.sleep(0.1)  # Wait for 0.1 seconds between updates

        current_time = time.time()

        if current_time - last_clear_time >= 200:
            os.system('cls')
            last_clear_time = current_time

        time.sleep(1)
        discord_presence_thread = threading.Thread(target=update_discord_presence)
        discord_presence_thread.daemon = True
        discord_presence_thread.start()

    except Exception as e:
        print(e)

status()  # Corrected the function call

# Initialize Colorama
init(autoreset=True)

# Functions including random Header and PUID generator
def random_accept_language():
    languages = ['en-US,en;q=0.9', 'fr-FR,fr;q=0.9', 'es-ES,es;q=0.9', 'de-DE,de;q=0.9', 'zh-CN,zh;q=0.9']
    return random.choice(languages)

def random_sec_ch_ua():
    browsers = ['"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"']
    return random.choice(browsers)

def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    ]
    return random.choice(user_agents)
 
def generate_partner_user_id(length=64):
    return secrets.token_hex(length // 2)  # Divided by 2 as each byte is two hex digits

# Clears the cmd for a better and cleaner preview. Supports all OS
os.system('clear' if os.name == 'posix' else 'cls')

# Function to generate the raw string of discord promo link
def generate_discord_url():
    base_url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
    'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': random_accept_language(),
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': random_sec_ch_ua(),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': random_user_agent()
}
    data = {
        'partnerUserId': generate_partner_user_id()
    }

# Prints the PUID (partnerUserId) for debuggig purpose
    dataprint = data['partnerUserId']
    print(f"({Fore.MAGENTA}+{Style.RESET_ALL}) PUID Used: {dataprint}")

# Extract the raw string of the link and adds it into a promo link
    try:
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        token = response.json().get('token')
        return f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

# Saves the links into a file
def save_url_to_file(url, filename):
    with open(filename, 'a') as file:
        file.write(url + "\n")

# Makes the URL shorter in the CMD so it doesn't flood.
def truncate_url(url, max_length=120):
    return url if len(url) <= max_length else url[:max_length] + "..."

# ASCII Art in color that will appear in CMD
print(Fore.CYAN + """
________                                _______  .__  __                  ___________              .__         .__  __   
\_____  \ ______   ________________     \      \ |__|/  |________  ____   \_   _____/__  _________ |  |   ____ |__|/  |_ 
 /   |   \\____ \_/ __ \_  __ \__  \    /   |   \|  \   __\_  __ \/  _ \   |    __)_\  \/  /\____ \|  |  /  _ \|  \   __/
/    |    \  |_> >  ___/|  | \// __ \_ /    |    \  ||  |  |  | \(  <_> )  |        \>    < |  |_> >  |_(  <_> )  ||  |  
\_______  /   __/ \___  >__|  (____  / \____|__  /__||__|  |__|   \____/  /_______  /__/\_ \|   __/|____/\____/|__||__|  
        \/|__|        \/           \/          \/                                 \/      \/|__|                          
""" + Style.RESET_ALL)

# Choice prompt
choice = input(f"{Fore.MAGENTA}Press 1:{Style.RESET_ALL} to generate an infinite amount of codes.\n{Fore.RED}Press 2:{Style.RESET_ALL} to generate a specific amount.\n{Fore.BLUE}Enter your input{Style.RESET_ALL}: ")

# Variables 
filename = 'promos.txt' # Will create a txt file in the directory where the script is ran. Change it for personalized path/name.
retry_delay = 5

# The whole logic of generating the strings, putting all together and saving it
# Modified logic for generating and checking the links
if choice == '1':
    try:
        while True:
            result = generate_discord_url()
            locked += 1
            if result and not result.startswith("Error"):
                save_url_to_file(result, filename)
                print(f"({Fore.GREEN}+{Style.RESET_ALL}) URL: {truncate_url(result)}")
                retry_delay = 5
            else:
                print(f"({Fore.RED}+{Style.RESET_ALL}) {result} Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay += 1
    except KeyboardInterrupt:
        print(f"({Fore.YELLOW}+{Style.RESET_ALL}) Loop stopped by user.")
    subprocess.run(["python", "main.py"])

elif choice == '2':
    num = int(input("Enter the number of codes to generate: "))
    for _ in range(num):
        result = generate_discord_url()
        locked += 1
        if result and not result.startswith("Error"):
            save_url_to_file(result, filename)
            print(f"({Fore.GREEN}+{Style.RESET_ALL}) URL: {truncate_url(result)}")
        else:
            print(f"({Fore.RED}+{Style.RESET_ALL}) {result} Error encountered.")
else:
    print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")
#  Restarts the script doesn't work in exe 
subprocess.run(["python", "main.py"])

